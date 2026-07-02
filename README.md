# ❤️ Theory-Driven Heart Attack Risk Predictor

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![SAS Viya](https://img.shields.io/badge/SAS-Viya-005CAB)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4+-F7931E?logo=scikitlearn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?logo=streamlit&logoColor=white)

---

## Overview

The **Theory-Driven Heart Attack Risk Predictor** is a machine learning application developed using the **CDC Behavioral Risk Factor Surveillance System (BRFSS) 2022** dataset containing **444,975 U.S. adults**.

Unlike traditional cardiovascular prediction models that rely primarily on clinical risk factors, this project integrates **behavioral science and public health theory** into feature selection. Variables were organized according to four established theoretical frameworks before training the predictive model.

The champion model was developed and validated in **SAS Viya Model Studio** and deployed as an interactive **Streamlit** web application for preventive cardiovascular risk assessment.

---

# Behavioral Frameworks

This study is the first known BRFSS 2022 cardiovascular machine learning project to simultaneously incorporate variables representing:

- 🟢 Health Belief Model (HBM)
- 🔵 Theory of Planned Behavior (TPB)
- 🔴 Social Ecological Model (SEM)
- 🟣 Allostatic Load Theory (ALT)

These frameworks improve model interpretability by organizing predictors according to behavioral and public health theory rather than relying solely on statistical feature selection.

---

# Dataset

**Source**

CDC Behavioral Risk Factor Surveillance System (BRFSS) 2022

**Sample Size**

444,975 U.S. adults

**Target Variable**

HadHeartAttack (Binary Classification)

---

# Champion Model

| Metric | Validation |
|---------|-----------:|
| Algorithm | Logistic Regression |
| Validation AUC | **0.8381** |
| Recall | **81.51%** |
| Operating Threshold | **0.05 (KS Optimized)** |
| Framework | HBM + TPB + SEM + ALT |

The model was trained and validated using **SAS Viya Model Studio**.

---

# Business Impact

By targeting the highest-risk **30%** of insured members, the model identifies approximately **79.95%** of heart attack cases.

For a hypothetical **2-million-member health insurer**, this targeted preventive strategy could substantially improve outreach efficiency while reducing unnecessary interventions.

Based on the 2025 AHRQ average inpatient hospitalization cost of **$21,560**, this approach represents an estimated **$56 million** in avoidable healthcare expenditures through earlier identification of high-risk individuals.

---

# Risk Stratification

The model demonstrates excellent population-level risk stratification.

| Decile | Observed Heart Attack Rate |
|-------:|---------------------------:|
| 1 | **24.99%** |
| 2 | 13.45% |
| 3 | 8.31% |
| 4 | 5.37% |
| 5 | 3.52% |
| 6 | 2.39% |
| 7 | 1.62% |
| 8 | 0.98% |
| 9 | 0.45% |
| 10 | **0.20%** |

This represents approximately a **125-fold difference** between the highest- and lowest-risk populations.

---

# Application Features

- Interactive Streamlit interface
- Individualized heart attack risk prediction
- Risk decile assignment
- Framework-based risk explanation
- Population benchmark comparison
- Preventive healthcare recommendations
- Explainable AI interpretation

---

# Technology Stack

- SAS Viya Model Studio
- Python
- Streamlit
- scikit-learn
- Pandas
- NumPy

---

# Repository Structure

```
heart-attack-risk-predictor/

│── app.py
│── requirements.txt
│── AGENTS.md
│── README.md
│
├── src/
│ ├── preprocess.py
│ ├── model.py
│ └── init.py
│
├── data/
│ └── README.md
│
└── images/
```

---

# Research Contributions

This project contributes to cardiovascular risk prediction by:

- Integrating behavioral science with machine learning
- Developing a theory-driven feature selection framework
- Deploying a validated SAS Viya champion model
- Supporting explainable preventive healthcare
- Demonstrating practical population health decision support

---

# Medical Disclaimer

This application is intended for **research and educational purposes only**.

Predictions are generated from population-level survey data and should **not** replace professional medical evaluation, diagnosis, or treatment decisions.

---

# Author

**Lilian Njeri Wanjiku**

Master of Science in Business Analytics

University of Central Oklahoma

2026

---

⭐ If you find this project useful, please consider starring the repository.
