# heart-attack-risk-predictor

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4+-F7931E?logo=scikitlearn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?logo=streamlit&logoColor=white)

## Business Impact

By targeting the top **30%** of members ranked by predicted risk, the model captures **79.95%** of heart attack cases. For a **2M-member insurer**, this translates to an estimated **$56M in avoided costs**, based on an average inpatient stay cost of **$21,560** (AHRQ 2025).

### Risk Concentration by Decile

The model shows strong risk stratification: event rates decline from **24.99%** in Decile 1 to **0.20%** in Decile 10, a **125x** difference.

| Decile (1 = highest risk) | Event Rate |
| --- | ---: |
| 1 | 24.99% |
| 2 | 13.45% |
| 3 | 8.31% |
| 4 | 5.37% |
| 5 | 3.52% |
| 6 | 2.39% |
| 7 | 1.62% |
| 8 | 0.98% |
| 9 | 0.45% |
| 10 | 0.20% |
