# Heart Attack Risk Predictor – Project Specification

## Project Overview

This repository contains the implementation of a **theory-driven machine learning application** for predicting heart attack risk using the **CDC Behavioral Risk Factor Surveillance System (BRFSS) 2022** dataset.

The application supports preventive cardiovascular risk assessment by estimating an individual's probability of reporting a previous heart attack based on demographic, behavioral, health, and social determinants.

---

# Research Objective

Develop an interpretable machine learning model capable of identifying individuals at elevated cardiovascular risk before a heart attack occurs.

The project emphasizes:

- Early risk identification
- Preventive healthcare
- Explainable AI
- Population health management
- Theory-driven feature engineering

---

# Dataset

**Source**

CDC Behavioral Risk Factor Surveillance System (BRFSS) 2022

**Sample Size**

444,975 U.S. adults

**Target Variable**

HadHeartAttack

Binary Classification

- Yes = 1
- No = 0

---

# Theoretical Frameworks

Variables were selected according to four established behavioral and public health theories.

## Health Belief Model (HBM)

Examples

- General Health
- Preventive Screening
- Healthcare Utilization

---

## Theory of Planned Behavior (TPB)

Examples

- Smoking
- Alcohol Consumption
- Physical Activity
- Nutrition

---

## Social Ecological Model (SEM)

Examples

- Chronic Diseases
- Income
- Race/Ethnicity
- Structural Factors

---

## Allostatic Load Theory (ALT)

Examples

- Physical Health
- Mental Health
- Functional Limitations
- Chronic Stress Indicators

---

# Champion Model

Algorithm

Logistic Regression

Developed using

SAS Viya Model Studio

Validation Performance

- AUC = 0.8381
- Recall = 81.51%
- KS Optimized Threshold = 0.05

The deployed application should reproduce the validated SAS Viya champion model as closely as possible.

---

# Modeling Principles

The implementation should follow these principles.

✅ Theory-driven feature selection

✅ Explainable predictions

✅ Population-level risk estimation

✅ Preventive healthcare decision support

✅ No target leakage

Leakage variables such as **HadAngina** should never be used for prediction.

---

# Deployment Principles

The Streamlit application should:

- Produce individualized heart attack risk estimates
- Display population risk deciles
- Explain major risk contributors
- Present framework-level interpretation
- Support healthcare decision-making
- Maintain consistency with the validated SAS Viya model

---

# Repository Structure

```
heart-attack-risk-predictor/

app.py

README.md

requirements.txt

AGENTS.md

src/
    preprocess.py
    model.py

data/
    README.md

images/
```

---

# Development Guidelines

Future code changes should:

- Preserve the theory-driven methodology
- Maintain compatibility with SAS Viya preprocessing
- Avoid introducing target leakage
- Keep predictions interpretable
- Clearly distinguish research findings from deployment assumptions

---

# Medical Disclaimer

This application supports research and educational use only.

Predictions should not replace clinical judgment or professional medical advice.
