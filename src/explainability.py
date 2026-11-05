import joblib
import pandas as pd
import numpy as np
import shap


# Load the trained model pipeline
failure_pipeline = joblib.load(
    "models/indupredict_failure_pipeline.pkl"
)

# Get the preprocessor and classifier
failure_preprocessor = failure_pipeline.named_steps["preprocessor"]
random_forest_model = failure_pipeline.named_steps["classifier"]

# Create SHAP explainer
shap_explainer = shap.TreeExplainer(
    random_forest_model
)


# Feature names after preprocessing
feature_names = [
    "Machine Type H",
    "Machine Type L",
    "Machine Type M",
    "Air Temperature",
    "Process Temperature",
    "Rotational Speed",
    "Torque",
    "Tool Wear",
    "Temperature Difference",
    "Mechanical Power",
    "Tool Wear × Torque"
]


def explain_machine(
    machine_type,
    air_temperature,
    process_temperature,
    rotational_speed,
    torque,
    tool_wear
):
    """
    Generate SHAP-based explanation for one machine prediction.
    """

    # Create machine input
    machine_data = pd.DataFrame([{
        "Type": machine_type,
        "Air temperature [K]": air_temperature,
        "Process temperature [K]": process_temperature,
        "Rotational speed [rpm]": rotational_speed,
        "Torque [Nm]": torque,
        "Tool wear [min]": tool_wear
    }])

    # Feature engineering
    machine_data["Temperature Difference [K]"] = (
        machine_data["Process temperature [K]"] -
        machine_data["Air temperature [K]"]
    )

    machine_data["Mechanical Power [W]"] = (
        machine_data["Torque [Nm]"] *
        machine_data["Rotational speed [rpm]"] *
        (2 * np.pi / 60)
    )

    machine_data["Tool Wear Torque Interaction"] = (
        machine_data["Tool wear [min]"] *
        machine_data["Torque [Nm]"]
    )

    # Transform input using the same preprocessing used during training
    processed_data = failure_preprocessor.transform(
        machine_data
    )

    # Generate SHAP values
    shap_values = shap_explainer.shap_values(
        processed_data
    )

    # Handle SHAP output format
    if isinstance(shap_values, list):
        shap_single = shap_values[1][0]
    else:
        shap_single = shap_values[0, :, 1]

    # Create explanation table
    explanation = pd.DataFrame({
        "Feature": feature_names,
        "SHAP Value": shap_single
    })

    explanation["Absolute SHAP"] = (
        explanation["SHAP Value"].abs()
    )

    explanation["Direction"] = explanation[
        "SHAP Value"
    ].apply(
        lambda value:
        "Increases failure prediction"
        if value > 0
        else "Decreases failure prediction"
    )

    # Most influential features first
    explanation = explanation.sort_values(
        "Absolute SHAP",
        ascending=False
    )

    return explanation.reset_index(drop=True)