import joblib
import pandas as pd
import numpy as np

from src.explainability import explain_machine
from src.diagnosis import diagnose_failure
from src.maintenance import get_maintenance_recommendations


# ============================================================
# LOAD TRAINED PRODUCTION PIPELINE
# ============================================================

failure_pipeline = joblib.load(
    "models/indupredict_failure_pipeline.pkl"
)


# ============================================================
# OBSERVED DATASET RANGES
# ============================================================
#
# These are the minimum and maximum values observed
# in the AI4I dataset used for this project.
#
# These are NOT universal limits for industrial machines.
# They are only used to identify inputs outside the
# conditions represented in our training dataset.
# ============================================================

DATASET_RANGES = {

    "Air temperature [K]": {
        "min": 295.3,
        "max": 304.5
    },

    "Process temperature [K]": {
        "min": 305.7,
        "max": 313.8
    },

    "Rotational speed [rpm]": {
        "min": 1168,
        "max": 2886
    },

    "Torque [Nm]": {
        "min": 3.8,
        "max": 76.6
    },

    "Tool wear [min]": {
        "min": 0,
        "max": 253
    }
}


def check_input_coverage(machine_data):
    """
    Check whether input values fall within the
    ranges observed in the AI4I dataset.

    This does NOT block prediction.
    It only identifies inputs outside the
    observed training-data range.
    """

    out_of_range = []

    for feature, limits in DATASET_RANGES.items():

        value = float(
            machine_data[feature].iloc[0]
        )

        minimum = limits["min"]
        maximum = limits["max"]

        if value < minimum or value > maximum:

            out_of_range.append({

                "feature": feature,

                "value": value,

                "observed_min": minimum,

                "observed_max": maximum
            })

    return out_of_range


def predict_machine(
    machine_type,
    air_temperature,
    process_temperature,
    rotational_speed,
    torque,
    tool_wear
):
    """
    Run the complete InduPredict prediction workflow.
    """

    # ========================================================
    # CREATE INPUT DATA
    # ========================================================

    machine_data = pd.DataFrame([{

        "Type": machine_type,

        "Air temperature [K]":
            air_temperature,

        "Process temperature [K]":
            process_temperature,

        "Rotational speed [rpm]":
            rotational_speed,

        "Torque [Nm]":
            torque,

        "Tool wear [min]":
            tool_wear
    }])


    # ========================================================
    # CHECK DATASET COVERAGE
    # ========================================================

    out_of_range = check_input_coverage(
        machine_data
    )


    if out_of_range:

        coverage_status = (
            "outside_observed_range"
        )

        coverage_warning = (
            "One or more input values are outside "
            "the range observed in the dataset used "
            "for this project. The model can still "
            "generate a prediction, but the result "
            "may be less reliable for these conditions."
        )

    else:

        coverage_status = (
            "within_observed_range"
        )

        coverage_warning = (
            "All sensor inputs are within the range "
            "observed in the dataset used for this project."
        )


    # ========================================================
    # ENGINEERED FEATURES
    # ========================================================

    machine_data[
        "Temperature Difference [K]"
    ] = (
        machine_data[
            "Process temperature [K]"
        ]
        -
        machine_data[
            "Air temperature [K]"
        ]
    )


    machine_data[
        "Mechanical Power [W]"
    ] = (
        machine_data[
            "Torque [Nm]"
        ]
        *
        machine_data[
            "Rotational speed [rpm]"
        ]
        *
        (2 * np.pi / 60)
    )


    machine_data[
        "Tool Wear Torque Interaction"
    ] = (
        machine_data[
            "Tool wear [min]"
        ]
        *
        machine_data[
            "Torque [Nm]"
        ]
    )


    # ========================================================
    # MACHINE FAILURE PREDICTION
    # ========================================================

    prediction = failure_pipeline.predict(
        machine_data
    )[0]


    probability = failure_pipeline.predict_proba(
        machine_data
    )[0][1]


    # ========================================================
    # FAILURE DIAGNOSIS
    # ========================================================

    diagnosis = diagnose_failure(

        machine_type=machine_type,

        air_temperature=air_temperature,

        process_temperature=process_temperature,

        rotational_speed=rotational_speed,

        torque=torque,

        tool_wear=tool_wear
    )


    detected_modes = diagnosis[
        "detected_failure_modes"
    ]


    # ========================================================
    # MAINTENANCE RECOMMENDATIONS
    # ========================================================

    recommendations = (
        get_maintenance_recommendations(
            detected_modes
        )
    )


    # ========================================================
    # SHAP EXPLANATION
    # ========================================================

    explanation = explain_machine(

        machine_type=machine_type,

        air_temperature=air_temperature,

        process_temperature=process_temperature,

        rotational_speed=rotational_speed,

        torque=torque,

        tool_wear=tool_wear
    )


    # ========================================================
    # CONVERT SHAP DATA TO JSON-FRIENDLY FORMAT
    # ========================================================

    explanation_records = []


    for _, row in explanation.iterrows():

        explanation_records.append({

            "feature":
                row["Feature"],

            "shap_value":
                round(
                    float(
                        row["SHAP Value"]
                    ),
                    6
                ),

            "absolute_shap":
                round(
                    float(
                        row["Absolute SHAP"]
                    ),
                    6
                ),

            "direction":
                row["Direction"]
        })


    # ========================================================
    # FINAL API RESPONSE
    # ========================================================

    return {

        "prediction":
            int(prediction),

        "failure_probability":
            round(
                float(probability),
                4
            ),

        "coverage": {

            "status":
                coverage_status,

            "warning":
                coverage_warning,

            "out_of_range_inputs":
                out_of_range
        },

        "diagnosis":
            diagnosis,

        "maintenance_recommendations":
            recommendations,

        "explanation":
            explanation_records
    }