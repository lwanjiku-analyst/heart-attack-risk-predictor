# ❤️ Heart Attack Risk Predictor

A theory-driven machine learning application that predicts individual heart attack risk using the **CDC BRFSS 2022** dataset and deploys the champion **Logistic Regression** model through an interactive Streamlit application.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4+-F7931E?logo=scikitlearn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?logo=streamlit&logoColor=white)
![SAS Viya](https://img.shields.io/badge/SAS-Viya-005CAB)

---

# Project Overview

This project develops and deploys a cardiovascular risk prediction model using **444,975 U.S. adults** from the **CDC Behavioral Risk Factor Surveillance System (BRFSS) 2022**.

Unlike traditional prediction models, the predictor uses a **theory-driven feature selection approach** integrating variables from four behavioral and public health frameworks:

- Health Belief Model (HBM)
- Theory of Planned Behavior (TPB)
- Social Ecological Model (SEM)
- Allostatic Load Theory (ALT)

The champion Logistic Regression model was developed and validated in **SAS Viya Model Studio** and deployed as an interactive **Streamlit** application.

---

# Model Performance

| Metric | Value |
|---------|------:|
| Validation AUC | **0.8381** |
| Recall | **81.51%** |
| KS Statistic | **0.5288** |
| Operating Threshold | **0.05 (KS Optimized)** |
| Dataset Size | **444,975 adults** |

---

# Business Impact

By targeting the highest-risk **30%** of insured members, the model identifies approximately **79.95%** of future heart attack cases.

For a hypothetical **2-million-member health insurer**, this targeted preventive strategy could substantially reduce unnecessary outreach while improving early intervention efficiency. Based on an average inpatient hospitalization cost of **$21,560 (AHRQ)**, the projected cost avoidance exceeds **$56 million** through more effective preventive care allocation.

---

# Risk Stratification

The model demonstrates excellent population stratification.

| Risk Decile | Observed Event Rate |
|-------------|-------------------:|
| 1 (Highest Risk) | **24.99%** |
| 2 | 13.45% |
| 3 | 8.31% |
| 4 | 5.37% |
| 5 | 3.52% |
| 6 | 2.39% |
| 7 | 1.62% |
| 8 | 0.98% |
| 9 | 0.45% |
| 10 (Lowest Risk) | **0.20%** |

This represents a **125-fold difference** between the highest- and lowest-risk populations.

---

# Features

- Interactive Streamlit interface
- Personalized heart attack risk prediction
- Risk decile assignment
- Clinical interpretation of predicted risk
- Theory-driven predictor selection
- SAS Viya Logistic Regression deployment

---

# Technology Stack

- SAS Viya Model Studio
- Python
- Streamlit
- scikit-learn
- Pandas
- NumPy

---

# Dataset

CDC Behavioral Risk Factor Surveillance System (BRFSS) 2022

- 444,975 adults
- Nationally representative U.S. health survey
- Binary target:
  - HadHeartAttack (Yes/No)

---

# Research Highlights

- Theory-driven machine learning framework
- Leakage-aware feature engineering
- KS-optimized decision threshold
- Preventive healthcare decision support
- Explainable risk stratification for insurers and healthcare providers

---

# Disclaimer

This application is intended for **research and educational purposes** and supports preventive risk assessment. It is **not** a substitute for professional medical diagnosis or clinical judgment.
