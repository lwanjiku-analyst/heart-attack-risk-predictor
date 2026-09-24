# ❤️ Theory-Driven Heart Attack Classification

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![SAS Viya](https://img.shields.io/badge/SAS-Viya-005CAB)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4+-F7931E?logo=scikitlearn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?logo=streamlit&logoColor=white)

---

## Overview

This project uses the **CDC Behavioral Risk Factor Surveillance System (BRFSS) 2022** dataset of **444,975 U.S. adults** to study characteristics associated with **previously reported heart attack status**.

Predictors were organized using behavioral and public health theory. The champion model was developed and validated in **SAS Viya Model Studio**, and the findings are presented in an interactive **Streamlit** application.

---

## Behavioral Frameworks

- 🟢 Health Belief Model (HBM)
- 🔵 Theory of Planned Behavior (TPB)
- 🔴 Social Ecological Model (SEM)
- 🟣 Allostatic Load Theory (ALT)

These frameworks help organize and explain the survey characteristics used by the model.

---

## Dataset

- **Source:** CDC BRFSS 2022
- **Modeling sample:** 444,975 U.S. adults
- **Target:** `HadHeartAttack` — previously reported heart attack status

---

## Champion Model

The champion model is a **Logistic Regression** model combining variables from all four frameworks.

| Validation AUC | Recall |
| ---: | ---: |
| **0.8391** | **81.53%** |

The model was evaluated using a stratified training–validation split.

---

## Population Findings

The highest-scoring **30%** of respondents included **79.95%** of those who reported a prior heart attack in the study dataset.

The observed prior-heart-attack rate was **24.99%** in the highest score decile and **0.20%** in the lowest. These figures describe patterns in the dataset, not future heart attack probabilities.

---

## Application Features

- Interactive Streamlit interface
- Survey-based classification score and score decile
- Population benchmark comparison
- Behavioral framework explanations
- Visualizations of population patterns

---

## Technology Stack

- SAS Viya Model Studio
- Python
- Streamlit
- scikit-learn
- Pandas
- NumPy

---

## Repository Structure

```text
heart-attack-risk-predictor/
├── app.py
├── requirements.txt
├── AGENTS.md
├── README.md
├── src/
│   ├── preprocess.py
│   ├── model.py
│   └── init.py
├── data/
│   └── README.md
└── images/
```

---

## Research Contributions

- Integrates behavioral science with machine learning
- Organizes predictors using four theoretical frameworks
- Makes population-level findings accessible through an interactive app

---

## Medical Disclaimer

This application is for **research and educational purposes only**. It examines **past, self-reported heart attack status**. It does **not** predict future heart attacks or replace professional medical evaluation.

---

## Author

**Lilian Njeri Wanjiku**  
Master of Science in Business Analytics  
University of Central Oklahoma · 2026

---

⭐ If you find this project useful, please consider starring the repository.
