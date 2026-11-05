const predictionForm =
    document.getElementById("predictionForm");


predictionForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();


        const machineData = {

            machine_type:
                document.getElementById(
                    "machineType"
                ).value,

            air_temperature:
                Number(
                    document.getElementById(
                        "airTemperature"
                    ).value
                ),

            process_temperature:
                Number(
                    document.getElementById(
                        "processTemperature"
                    ).value
                ),

            rotational_speed:
                Number(
                    document.getElementById(
                        "rotationalSpeed"
                    ).value
                ),

            torque:
                Number(
                    document.getElementById(
                        "torque"
                    ).value
                ),

            tool_wear:
                Number(
                    document.getElementById(
                        "toolWear"
                    ).value
                )
        };


        try {

            const response =
                await fetch(
                    "/predict",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(
                                machineData
                            )
                    }
                );


            if (!response.ok) {

                throw new Error(
                    "Prediction request failed."
                );
            }


            const result =
                await response.json();


            console.log(
                "InduPredict Result:",
                result
            );


            // =========================
            // SHOW RESULT
            // =========================

            document
                .getElementById("result")
                .classList
                .remove("hidden");


            // =========================
            // MACHINE STATUS
            // =========================

            const predictionElement =
                document.getElementById(
                    "prediction"
                );


            predictionElement.textContent =
                result.prediction === 1
                    ? "FAILURE DETECTED"
                    : "NO FAILURE DETECTED";


            predictionElement.className =
                result.prediction === 1
                    ? "status-failure"
                    : "status-healthy";


            // =========================
            // FAILURE PROBABILITY
            // =========================

            const probabilityElement =
                document.getElementById(
                    "probability"
                );


            probabilityElement.textContent =
                (
                    result.failure_probability * 100
                ).toFixed(1) + "%";


            probabilityElement.className =
                result.failure_probability >= 0.5
                    ? "probability-high"
                    : "probability-low";


            // =========================
            // FAILURE MODE
            // =========================

            const failureModes =
                result.diagnosis
                    .detected_failure_modes;


            const failureModeElement =
                document.getElementById(
                    "failureMode"
                );


            failureModeElement.textContent =
                failureModes.length > 0
                    ? failureModes.join(", ")
                    : "None";


            if (failureModes.length > 0) {

                failureModeElement.className =
                    "failure-mode-badge";

            } else {

                failureModeElement.className = "";

            }


            // =========================
            // MODEL COVERAGE WARNING
            // =========================

            const coverageWarning =
                document.getElementById(
                    "coverageWarning"
                );


            const coverageMessage =
                document.getElementById(
                    "coverageMessage"
                );


            const outOfRangeInputs =
                document.getElementById(
                    "outOfRangeInputs"
                );


            outOfRangeInputs.innerHTML = "";


            if (
                result.coverage &&
                result.coverage.status ===
                    "outside_observed_range"
            ) {

                coverageWarning.classList
                    .remove("hidden");


                coverageMessage.textContent =
                    result.coverage.warning;


                result.coverage
                    .out_of_range_inputs
                    .forEach(function (item) {

                        const rangeItem =
                            document.createElement(
                                "div"
                            );


                        rangeItem.className =
                            "range-item";


                        rangeItem.textContent =
                            item.feature +
                            ": " +
                            item.value +
                            " (observed " +
                            item.observed_min +
                            "–" +
                            item.observed_max +
                            ")";


                        outOfRangeInputs
                            .appendChild(
                                rangeItem
                            );

                    });


            } else {

                coverageWarning.classList
                    .add("hidden");

            }


            // =========================
            // MAINTENANCE
            // =========================

            const recommendations =
                result.maintenance_recommendations;


            document.getElementById(
                "maintenance"
            ).textContent =
                recommendations.length > 0
                    ? recommendations
                        .map(
                            item => item.action
                        )
                        .join(" ")
                    : "No maintenance recommendation available.";


            // =========================
            // SHAP EXPLANATION
            // =========================

            const explanationContainer =
                document.getElementById(
                    "explanation"
                );


            explanationContainer.innerHTML =
                "";


            // Get top 5 features

            const topFeatures =
                result.explanation.slice(
                    0,
                    5
                );


            console.log(
                "Top SHAP features:",
                topFeatures
            );


            if (topFeatures.length === 0) {

                explanationContainer.textContent =
                    "No explanation available.";

                return;
            }


            // =================================================
            // CALCULATE TOTAL ABSOLUTE SHAP IMPACT
            // =================================================
            //
            // This is used only to show a user-friendly
            // relative influence percentage.
            //
            // Example:
            // If one feature contributes 0.20 and the total
            // absolute contribution is 0.60:
            //
            // 0.20 / 0.60 * 100 = 33.3%
            //
            // This percentage is NOT a probability.
            // =================================================

            const totalAbsoluteImpact =
                topFeatures.reduce(
                    function (total, item) {

                        return total +
                            Math.abs(
                                Number(
                                    item.shap_value
                                )
                            );

                    },
                    0
                );


            // Find largest SHAP value
            // for proportional bar width.

            const maximumImpact =
                Math.max(
                    ...topFeatures.map(
                        item =>
                            Math.abs(
                                Number(
                                    item.shap_value
                                )
                            )
                    )
                );


            // =========================
            // CREATE SHAP BARS
            // =========================

            topFeatures.forEach(
                function (item) {

                    const shapValue =
                        Number(
                            item.shap_value
                        );


                    // =========================
                    // RELATIVE INFLUENCE %
                    // =========================

                    const relativeInfluence =
                        totalAbsoluteImpact === 0
                            ? 0
                            : (
                                Math.abs(
                                    shapValue
                                ) /
                                totalAbsoluteImpact
                            ) * 100;


                    // =========================
                    // MAIN ROW
                    // =========================

                    const shapRow =
                        document.createElement(
                            "div"
                        );


                    shapRow.style.marginBottom =
                        "20px";


                    // =========================
                    // HEADER
                    // =========================

                    const shapHeader =
                        document.createElement(
                            "div"
                        );


                    shapHeader.style.display =
                        "flex";


                    shapHeader.style.justifyContent =
                        "space-between";


                    shapHeader.style.alignItems =
                        "center";


                    shapHeader.style.marginBottom =
                        "7px";


                    // =========================
                    // FEATURE NAME
                    // =========================

                    const featureName =
                        document.createElement(
                            "span"
                        );


                    featureName.textContent =
                        item.feature;


                    featureName.style.fontSize =
                        "14px";


                    featureName.style.fontWeight =
                        "600";


                    // =========================
                    // RELATIVE INFLUENCE
                    // =========================

                    const shapValueElement =
                        document.createElement(
                            "span"
                        );


                    const arrow =
                        shapValue >= 0
                            ? " ↑"
                            : " ↓";


                    shapValueElement.textContent =
                        relativeInfluence.toFixed(1) +
                        "%" +
                        arrow;


                    shapValueElement.style.fontSize =
                        "13px";


                    shapValueElement.style.fontWeight =
                        "700";


                    shapValueElement.style.color =
                        shapValue >= 0
                            ? "#dc2626"
                            : "#16a34a";


                    shapHeader.appendChild(
                        featureName
                    );


                    shapHeader.appendChild(
                        shapValueElement
                    );


                    // =========================
                    // BAR BACKGROUND
                    // =========================

                    const barContainer =
                        document.createElement(
                            "div"
                        );


                    barContainer.style.width =
                        "100%";


                    barContainer.style.height =
                        "12px";


                    barContainer.style.background =
                        "#e2e8f0";


                    barContainer.style.borderRadius =
                        "20px";


                    barContainer.style.overflow =
                        "hidden";


                    // =========================
                    // ACTUAL BAR
                    // =========================

                    const bar =
                        document.createElement(
                            "div"
                        );


                    const impact =
                        Math.abs(
                            shapValue
                        );


                    const width =
                        maximumImpact === 0
                            ? 0
                            : (
                                impact /
                                maximumImpact
                            ) * 100;


                    bar.style.width =
                        width + "%";


                    bar.style.height =
                        "100%";


                    bar.style.minWidth =
                        "4px";


                    bar.style.borderRadius =
                        "20px";


                    bar.style.background =
                        shapValue >= 0
                            ? "#dc2626"
                            : "#16a34a";


                    bar.style.transition =
                        "width 0.5s ease";


                    barContainer.appendChild(
                        bar
                    );


                    // =========================
                    // DIRECTION
                    // =========================

                    const direction =
                        document.createElement(
                            "div"
                        );


                    direction.textContent =
                        item.direction;


                    direction.style.fontSize =
                        "12px";


                    direction.style.color =
                        "#64748b";


                    direction.style.marginTop =
                        "5px";


                    // =========================
                    // ASSEMBLE
                    // =========================

                    shapRow.appendChild(
                        shapHeader
                    );


                    shapRow.appendChild(
                        barContainer
                    );


                    shapRow.appendChild(
                        direction
                    );


                    explanationContainer.appendChild(
                        shapRow
                    );

                }
            );


        }


        catch (error) {

            console.error(
                "InduPredict Error:",
                error
            );


            document
                .getElementById("result")
                .classList
                .remove("hidden");


            document.getElementById(
                "prediction"
            ).textContent =
                "Error while analyzing machine.";


            document.getElementById(
                "probability"
            ).textContent = "";


            document.getElementById(
                "failureMode"
            ).textContent = "";


            document.getElementById(
                "maintenance"
            ).textContent = "";


            document.getElementById(
                "explanation"
            ).innerHTML = "";


            document
                .getElementById(
                    "coverageWarning"
                )
                .classList
                .add("hidden");

        }

    }
);