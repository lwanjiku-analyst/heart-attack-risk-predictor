# Heart Attack Risk Predictor - Agent Notes

## Project objective
This project predicts `HadHeartAttack` as a binary classification target.

## Champion model
- Algorithm: Logistic Regression
- Training scope: all 4 frameworks combined (`HBM + TPB + SEM + ALT`)
- Validation AUC: `0.8381`
- Validation Recall: `0.8151`
- Operating threshold: `KS cutoff = 0.05`

## Dataset
- Source: CDC BRFSS 2022
- Observations: `444,975`
