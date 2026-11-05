# 🚀 InduPredict – AI-Based Industrial Predictive Maintenance System

InduPredict is a machine learning-based predictive maintenance application designed to predict potential machine failures, identify possible failure modes, and provide maintenance recommendations using machine sensor data.

The project demonstrates how machine learning and explainable AI can help support proactive maintenance decisions in industrial environments.

## 🎯 Project Overview

Traditional maintenance approaches often depend on fixed schedules or respond only after equipment failure. InduPredict explores a predictive approach by analysing machine operating conditions and identifying potential failure risks before breakdowns occur.

The application uses a trained Random Forest model to predict machine failure and provides additional insights through failure diagnosis, maintenance recommendations, and SHAP-based explainability.

## ✨ Key Features

- **Machine Failure Prediction:** Predicts the possibility of machine failure using sensor parameters.
- **Failure Diagnosis:** Identifies possible failure modes based on machine operating conditions.
- **Maintenance Recommendations:** Provides actionable suggestions based on diagnosed failure conditions.
- **Explainable AI:** Uses SHAP to explain the influence of input features on model predictions.
- **Input Range Awareness:** Identifies sensor inputs outside the observed training data ranges.
- **Interactive Dashboard:** Provides a user-friendly interface to enter machine parameters and view prediction results.

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn, Random Forest |
| Explainable AI | SHAP |
| Backend | FastAPI |
| Frontend | HTML, CSS, JavaScript |
| Dataset | AI4I 2020 Predictive Maintenance Dataset |
| Development Tools | VS Code, Jupyter Notebook, Git, GitHub |

## 📊 Machine Learning Approach

The project uses the AI4I 2020 Predictive Maintenance Dataset for model development.

The workflow includes:

1. Data understanding and exploration.
2. Data preprocessing and feature engineering.
3. Training a Random Forest classification model.
4. Evaluating model performance.
5. Saving the trained model pipeline.
6. Integrating predictions into the application.
7. Using SHAP to explain model predictions.

### Engineered Features

- Temperature Difference
- Mechanical Power
- Tool Wear × Torque

## 🏗️ Project Structure

```text
InduPredict/
│
├── app/
│   ├── main.py
│   └── static/
│       ├── index.html
│       ├── styles.css
│       └── script.js
│
├── data/
│   └── raw/
│       └── ai4i2020.csv
│
├── models/
│   ├── indupredict_failure_pipeline.pkl
│   └── indupredict_random_forest.pkl
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   └── 02_failure_diagnosis.ipynb
│
├── src/
│   ├── diagnosis.py
│   ├── explainability.py
│   ├── maintenance.py
│   └── predictor.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or above
- pip
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/lakshmivasista/InduPredict.git
```

### 2. Navigate to the Project Directory

```bash
cd InduPredict
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
uvicorn app.main:app --reload
```

Open your browser and navigate to:

```text
http://127.0.0.1:8000
```

## 📌 Project Objective

The primary objective of InduPredict is to demonstrate the application of machine learning in industrial predictive maintenance by combining failure prediction, diagnosis, maintenance recommendations, and model explainability in a single application.

## 🎓 Learning Outcomes

Through this project, I gained practical experience in:

- Machine learning model development and evaluation.
- Data preprocessing and feature engineering.
- Integrating trained ML models with a backend application.
- Implementing explainable AI using SHAP.
- Developing an interactive web application.
- Building an end-to-end machine learning project.

## ⚠️ Disclaimer

InduPredict is an educational project developed using the AI4I 2020 dataset. Its predictions are intended for demonstration and learning purposes and should not be treated as a substitute for industrial safety systems or professional maintenance assessments.

## 👩‍💻 Author

**Lakshmi**

GitHub: [@lakshmivasista](https://github.com/lakshmivasista)

---

⭐ If you find this project interesting, feel free to explore the repository!
