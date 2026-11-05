def get_maintenance_recommendations(detected_modes):
    """
    Generate maintenance recommendations based on
    detected failure modes.
    """

    recommendations = []

    if "HDF" in detected_modes:
        recommendations.append({
            "failure_mode": "HDF",
            "action": "Inspect cooling and heat-dissipation conditions."
        })

    if "PWF" in detected_modes:
        recommendations.append({
            "failure_mode": "PWF",
            "action": "Inspect power/load conditions and operating range."
        })

    if "OSF" in detected_modes:
        recommendations.append({
            "failure_mode": "OSF",
            "action": "Inspect tool wear and excessive mechanical load."
        })

    if "TWF" in detected_modes:
        recommendations.append({
            "failure_mode": "TWF",
            "action": "Inspect tool condition and tool-wear status."
        })

    if "RNF" in detected_modes:
        recommendations.append({
            "failure_mode": "RNF",
            "action": "Review sensor readings and machine operating history."
        })

    if not recommendations:
        recommendations.append({
            "failure_mode": "None",
            "action": "No verified failure-mode condition detected."
        })

    return recommendations