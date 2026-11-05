import numpy as np


def diagnose_failure(
    machine_type,
    air_temperature,
    process_temperature,
    rotational_speed,
    torque,
    tool_wear
):
    """
    Diagnose verified failure conditions using
    the AI4I 2020 failure-mode rules.
    """

    temperature_difference = (
        process_temperature - air_temperature
    )

    mechanical_power = (
        torque *
        rotational_speed *
        (2 * np.pi / 60)
    )

    tool_wear_torque = (
        tool_wear * torque
    )

    detected_modes = []

    # Heat Dissipation Failure
    if (
        temperature_difference < 8.6
        and rotational_speed < 1380
    ):
        detected_modes.append("HDF")

    # Power Failure
    if (
        mechanical_power < 3500
        or mechanical_power > 9000
    ):
        detected_modes.append("PWF")

    # Overstrain Failure
    osf_thresholds = {
        "L": 11000,
        "M": 12000,
        "H": 13000
    }

    if (
        machine_type in osf_thresholds
        and tool_wear_torque > osf_thresholds[machine_type]
    ):
        detected_modes.append("OSF")

    return {
        "detected_failure_modes": detected_modes,
        "temperature_difference": round(
            temperature_difference, 2
        ),
        "mechanical_power": round(
            mechanical_power, 2
        ),
        "tool_wear_torque": round(
            tool_wear_torque, 2
        )
    }