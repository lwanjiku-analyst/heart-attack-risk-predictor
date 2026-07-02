# Heart Attack Risk Predictor – Agent Notes

## Project Objective
Predict the probability of a future heart attack (`HadHeartAttack`) using a theory-driven machine learning approach based on CDC BRFSS 2022 data.

## Champion Model
- Algorithm: Logistic Regression
- Framework: Combined theory-based predictors from
  - Health Belief Model (HBM)
  - Theory of Planned Behavior (TPB)
  - Social Ecological Model (SEM)
  - Allostatic Load Theory (ALT)
- Validation AUC: 0.8381
- Validation Recall: 81.51%
- Operating Threshold: KS-optimized cutoff = 0.05

## Dataset
- Source: CDC BRFSS 2022
- Sample Size: 444,975 U.S. adults
- Binary Target: HadHeartAttack (Yes/No)

## Modeling Principles
- Theory-driven variable selection
- Leakage variables (e.g., HadAngina) excluded
- Missing values handled using SAS Viya imputation
- Champion model developed and validated in SAS Viya Model Studio

## Deployment
The Streamlit application reproduces the validated SAS Viya champion model and provides individualized heart attack risk estimates for preventive screening and decision support.
