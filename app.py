import math
from dataclasses import dataclass
import streamlit as st

# ─────────────────────────────────────────────
# Page config + styling
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Heart Attack Risk Predictor",
    page_icon="❤️",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,300;0,600;0,700;1,300&family=DM+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
h1, h2, h3 { font-family: 'Fraunces', serif !important; }

.metric-card {
    border: 1px solid #e0e6f0;
    border-radius: 16px;
    padding: 1.2rem 1.4rem;
    background: linear-gradient(160deg, #ffffff 0%, #f7f9ff 100%);
    box-shadow: 0 2px 12px rgba(18,38,63,0.06);
    margin-bottom: 0.8rem;
}

.risk-pill {
    display: inline-block;
    padding: 0.4rem 1rem;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.95rem;
    letter-spacing: 0.3px;
}

.equity-flag {
    border-left: 4px solid #E67E22;
    background: #FFF8F0;
    border-radius: 0 12px 12px 0;
    padding: 0.8rem 1rem;
    margin: 0.6rem 0;
    font-size: 0.92rem;
    color: #7D4000;
}

.framework-bar {
    height: 10px;
    border-radius: 999px;
    margin: 4px 0 8px 0;
}

.action-card {
    border-left: 4px solid #1B4F8C;
    background: #F2F6FB;
    border-radius: 0 12px 12px 0;
    padding: 0.7rem 1rem;
    margin: 0.4rem 0;
    font-size: 0.91rem;
}

.action-card-red {
    border-left: 4px solid #C0392B;
    background: #FEF0EE;
}

.action-card-yellow {
    border-left: 4px solid #E67E22;
    background: #FFF8F0;
}

.action-card-green {
    border-left: 4px solid #1A6B2A;
    background: #F0FAF2;
}

.small-note { color: #5f6b7a; font-size: 0.88rem; }

.decile-grid {
    display: flex;
    gap: 4px;
    margin: 8px 0;
}

.decile-cell {
    flex: 1;
    height: 28px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 700;
}

.benchmark-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    border-bottom: 1px solid #EEF2F8;
    font-size: 0.9rem;
}

.stCheckbox label { font-size: 0.95rem !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Model definition
# ─────────────────────────────────────────────
@dataclass
class Feature:
    label: str
    coef: float
    framework: str
    protective_when_true: bool = False
    action: str = ""


INTERCEPT = -4.10

FEATURES = {
    "age":             Feature("Age (per year)",                    0.041, "Baseline"),
    "male":            Feature("Male sex",                          0.34,  "Baseline"),
    "bmi":             Feature("BMI (per unit)",                    0.017, "Baseline"),
    "high_bp":         Feature("High blood pressure",               0.64,  "SEM",    action="Consult your doctor about blood pressure management"),
    "high_chol":       Feature("High cholesterol",                  0.46,  "SEM",    action="Request a lipid panel at your next checkup"),
    "diabetes":        Feature("Diabetes",                          0.76,  "SEM",    action="Ensure HbA1c levels are monitored every 3-6 months"),
    "stroke":          Feature("Prior stroke",                      0.93,  "SEM",    action="Cardiology follow-up is strongly recommended"),
    "chd":             Feature("Angina / Coronary heart disease",   1.08,  "SEM",    action="Seek immediate cardiology review"),
    "smoker":          Feature("Current smoker",                    0.41,  "TPB",    action="Enroll in a smoking cessation program"),
    "heavy_drinker":   Feature("Heavy alcohol use",                 0.24,  "TPB",    action="Reduce alcohol consumption — consult your doctor"),
    "no_exercise":     Feature("No exercise",                       0.35,  "TPB",    action="Start with 30 min of moderate activity 5 days/week"),
    "fruit_veg_daily": Feature("Daily fruit & vegetables",         -0.21,  "HBM",   True, "Maintain your healthy diet — it is protective"),
    "good_health":     Feature("Self-rated good/very good health", -0.49,  "HBM",   True, "Keep up preventive care and annual checkups"),
    "difficulty_walking": Feature("Difficulty walking",             0.57,  "ALT",   action="Discuss mobility rehabilitation with your doctor"),
    "low_income":      Feature("Low income",                        0.32,  "SEM",   action="Ask about community health centers and free screening programs"),
}

FRAMEWORK_COLORS = {
    "SEM":      "#C0392B",
    "TPB":      "#1B4F8C",
    "HBM":      "#1A6B2A",
    "ALT":      "#7D3C98",
    "Baseline": "#888888",
}

FRAMEWORK_NAMES = {
    "SEM": "Social Ecological Model — Chronic Conditions & Structural Factors",
    "TPB": "Theory of Planned Behavior — Behavioral Lifestyle",
    "HBM": "Health Belief Model — Preventive Care Engagement",
    "ALT": "Allostatic Load Theory — Cumulative Stress & Functional Burden",
    "Baseline": "Baseline Demographics",
}

DECILE_EVENT_RATES = {1:24.99,2:16.40,3:10.60,4:7.20,5:4.90,6:3.40,7:2.30,8:1.40,9:0.70,10:0.20}
NATIONAL_AVG = 5.64


def sigmoid(z):
    return 1.0 / (1.0 + math.exp(-z))

def calculate_bmi(height_cm, weight_kg):
    h = height_cm / 100
    return weight_kg / (h ** 2)

def risk_tier(prob_pct):
    if prob_pct < 3:   return "Low",       "#e8f6ee", "#1f7a45"
    if prob_pct < 8:   return "Moderate",  "#fff6df", "#8a6300"
    if prob_pct < 16:  return "High",      "#ffe8e0", "#9b3a20"
    return              "Very High",       "#fde2e8", "#8b1e3f"

def to_decile(prob_pct):
    bins = [20,14,9,6,4,2.8,1.8,1.0,0.45]
    for i, cut in enumerate(bins, start=1):
        if prob_pct >= cut:
            return i
    return 10

def get_framework_contributions(values):
    fw = {"SEM":0.0,"TPB":0.0,"HBM":0.0,"ALT":0.0,"Baseline":0.0}
    for key, val in values.items():
        if key not in FEATURES: continue
        f = FEATURES[key]
        contrib = abs(f.coef * val)
        if contrib > 0:
            fw[f.framework] = fw.get(f.framework, 0) + contrib
    return fw

def contribution_list(values):
    risk_contrib, protect_contrib = [], []
    for key, val in values.items():
        if key not in FEATURES: continue
        coef = FEATURES[key].coef
        contrib = coef * val
        if contrib > 0:
            risk_contrib.append((FEATURES[key].label, contrib, FEATURES[key].framework, FEATURES[key].action))
        elif contrib < 0:
            protect_contrib.append((FEATURES[key].label, abs(contrib), FEATURES[key].framework, FEATURES[key].action))
    risk_contrib.sort(key=lambda x: x[1], reverse=True)
    protect_contrib.sort(key=lambda x: x[1], reverse=True)
    return risk_contrib, protect_contrib

def decile_interpretation(decile, event_rate, risk):
    if decile == 1:
        return f"You are in the **top 10% highest-risk individuals** in the U.S. population. People in your risk group have a {event_rate:.1f}% observed heart attack rate — more than **4× the national average** of {NATIONAL_AVG}%."
    elif decile == 2:
        return f"You are in the **top 20% highest-risk** individuals. Your decile has a {event_rate:.1f}% heart attack rate — nearly **3× the national average**."
    elif decile == 3:
        return f"You are in the **top 30%** by risk. Your decile shows a {event_rate:.1f}% event rate — nearly **2× the national average**. Preventive care is strongly recommended."
    elif decile <= 5:
        return f"You are in the **middle risk range** (Decile {decile}). Your decile event rate is {event_rate:.1f}% — close to or slightly below the national average of {NATIONAL_AVG}%."
    else:
        return f"You are in the **lower risk range** (Decile {decile}). Your decile event rate is {event_rate:.1f}% — well below the national average. Maintain healthy behaviors."

def get_recommendation(decile):
    if decile <= 3:
        return "red", "#C0392B", "Higher Risk Profile", "Your cardiovascular risk is substantially higher than the national average. Consider discussing these results with a healthcare professional and exploring preventive screening and lifestyle interventions."
    elif decile <= 5:
        return "yellow", "#E67E22", "Moderate Risk Profile", "Your cardiovascular risk is above the national average. An annual cardiovascular checkup and a review of lifestyle factors with your doctor is recommended."
    else:
        return "green", "#1A6B2A", "Lower Risk Profile", "Your cardiovascular risk is at or below the national average. Continue maintaining healthy behaviors and routine preventive care visits."

def equity_check(race, risk, decile):
    if race in ["Hispanic", "Black / African American (Non-Hispanic)", "Other Race (Non-Hispanic)"]:
        return True
    return False


# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Model Snapshot")

    st.markdown("**Purpose**")
    st.markdown("Identify individuals who may benefit from earlier preventive healthcare interventions before a heart attack occurs.")

    st.markdown("**Data Source**")
    st.markdown("CDC BRFSS 2022 (444,975 U.S. adults)")

    st.markdown("**How Accurate Is It?**")
    st.markdown("<span style='font-size:0.8rem;'>✅</span> Correctly identifies heart attack risk patterns in approximately **84% of cases**", unsafe_allow_html=True)

    st.markdown("**How Well Does It Find High-Risk Individuals?**")
    st.markdown("<span style='font-size:0.8rem;'>✅</span> Identifies approximately **82 out of every 100 high-risk individuals**", unsafe_allow_html=True)

    st.markdown("**How Effective Is It?**")
    st.markdown("<span style='font-size:0.8rem;'>✅</span> Highest-risk individuals experience heart attack rates **4.4× higher** than the national average", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 🌎 Why This Matters")
    st.markdown("<span style='font-size:0.8rem;'>✅</span> Identifies individuals who may benefit from earlier preventive care", unsafe_allow_html=True)
    st.markdown("<span style='font-size:0.8rem;'>✅</span> Helps focus healthcare resources on those most at risk", unsafe_allow_html=True)
    st.markdown("<span style='font-size:0.8rem;'>✅</span> Supports data-driven population health management", unsafe_allow_html=True)
    st.markdown("<span style='font-size:0.8rem;'>✅</span> May reduce avoidable heart attacks and related healthcare costs", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### Behavioral & Public Health Frameworks")
    framework_labels = {
        "SEM": "Chronic Conditions & Structural Factors",
        "TPB": "Health Behaviors & Lifestyle Choices",
        "HBM": "Preventive Care Engagement",
        "ALT": "Chronic Stress & Functional Burden",
    }
    for fw, color in FRAMEWORK_COLORS.items():
        if fw == "Baseline": continue
        st.markdown(f"<span style='color:{color};font-size:1.3rem;'>●</span> **{fw}** — {framework_labels[fw]}", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<span class='small-note'>First study in BRFSS cardiovascular ML literature to apply 4 behavioral theory frameworks simultaneously. University of Central Oklahoma, 2026.</span>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Title
# ─────────────────────────────────────────────
st.title("❤️ Heart Attack Risk Predictor")
st.caption("Powered by CDC BRFSS 2022 · 444,975 U.S. Adults · Logistic Regression Champion Model · AUC 0.84 · Lift@D1 4.43×")
st.markdown("---")

col1, col2 = st.columns([1.05, 1], gap="large")

# ─────────────────────────────────────────────
# LEFT COLUMN — INPUTS
# ─────────────────────────────────────────────
with col1:
    st.subheader("Patient Inputs")

    age = st.slider("Age", min_value=18, max_value=95, value=52)
    sex = st.selectbox("Sex", ["Female", "Male"])

    race = st.selectbox("Race / Ethnicity", [
        "White (Non-Hispanic)",
        "Hispanic",
        "Black / African American (Non-Hispanic)",
        "Other Race (Non-Hispanic)",
        "Multiracial (Non-Hispanic)",
        "Prefer not to say"
    ])

    c1, c2 = st.columns(2)
    with c1:
        height_cm = st.number_input("Height (cm)", min_value=120.0, max_value=230.0, value=170.0, step=0.5)
    with c2:
        weight_kg = st.number_input("Weight (kg)", min_value=35.0, max_value=250.0, value=78.0, step=0.5)

    bmi = calculate_bmi(height_cm, weight_kg)
    st.markdown(f"**Auto-calculated BMI:** `{bmi:.1f}`")

    st.markdown("---")
    st.markdown("### 🔴 SEM — Chronic Conditions")
    high_bp     = st.checkbox("High blood pressure")
    high_chol   = st.checkbox("High cholesterol")
    diabetes    = st.checkbox("Diabetes")
    stroke      = st.checkbox("Prior stroke")
    chd         = st.checkbox("Angina / Coronary heart disease")
    low_income  = st.checkbox("Low income")

    st.markdown("### 🔵 TPB — Behavioral Lifestyle")
    smoker          = st.checkbox("Current smoker")
    heavy_drinker   = st.checkbox("Heavy drinker")
    no_exercise     = st.checkbox("No exercise")

    st.markdown("### 🟢 HBM — Preventive Care")
    fruit_veg_daily = st.checkbox("Fruit & vegetables daily ✓ (protective)")
    good_health     = st.checkbox("Self-rated good/very good health ✓ (protective)")

    st.markdown("### 🟣 ALT — Stress & Functional Burden")
    difficulty_walking = st.checkbox("Difficulty walking")


# ─────────────────────────────────────────────
# RIGHT COLUMN — RESULTS
# ─────────────────────────────────────────────
with col2:
    st.subheader("Prediction Results")

    x = {
        "age": age, "male": 1 if sex=="Male" else 0, "bmi": bmi,
        "high_bp": int(high_bp), "high_chol": int(high_chol),
        "diabetes": int(diabetes), "stroke": int(stroke), "chd": int(chd),
        "smoker": int(smoker), "heavy_drinker": int(heavy_drinker),
        "no_exercise": int(no_exercise), "fruit_veg_daily": int(fruit_veg_daily),
        "good_health": int(good_health), "difficulty_walking": int(difficulty_walking),
        "low_income": int(low_income),
    }

    logit = INTERCEPT + sum(FEATURES[k].coef * v for k, v in x.items())
    risk  = sigmoid(logit) * 100
    tier, bg, fg = risk_tier(risk)
    decile = to_decile(risk)
    event_rate = DECILE_EVENT_RATES[decile]

    # ── RISK SCORE ──
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="margin:0;color:#1c2f52;">Predicted Risk</h3>
        <p style="font-size:2.4rem;font-weight:700;margin:0.2rem 0 0.5rem;color:#1c2f52;">{risk:.2f}%</p>
        <span class="risk-pill" style="background:{bg};color:{fg};">{tier} Risk</span>
        <p style="margin:0.6rem 0 0;font-size:0.88rem;color:#5f6b7a;">National average: {NATIONAL_AVG}% &nbsp;|&nbsp; Your risk is <b>{risk/NATIONAL_AVG:.1f}×</b> the national average</p>
    </div>
    """, unsafe_allow_html=True)

    # ── EQUITY FLAG ──
    if equity_check(race, risk, decile):
        st.markdown(f"""
        <div class="equity-flag">
            ⚠️ <b>Equity Note:</b> Research shows that <b>{race}</b> individuals may be
            <b>under-scored</b> by population-level cardiovascular models due to structural
            underrepresentation in survey data. Clinical judgment is especially important
            alongside this prediction. Consider additional screening even if the score appears moderate.
            <br><small><i>Finding from Wanjiku et al. (2026) — first equity audit in BRFSS cardiovascular ML literature.</i></small>
        </div>
        """, unsafe_allow_html=True)

    # ── DECILE ──
    decile_colors = []
    for d in range(1, 11):
        if d < decile:
            decile_colors.append("#1c2f52")
        elif d == decile:
            decile_colors.append(fg)
        else:
            decile_colors.append("#e0e6f0")

    decile_cells = "".join([
        f'<div class="decile-cell" style="background:{decile_colors[d-1]};color:{"white" if d<=decile else "#aaa"};">{d}</div>'
        for d in range(1,11)
    ])

    st.markdown(f"""
    <div class="metric-card">
        <h3 style="margin:0;color:#1c2f52;">Risk Decile</h3>
        <p style="font-size:1.5rem;font-weight:700;margin:0.3rem 0 0.2rem;color:{fg};">D{decile} of 10</p>
        <div class="decile-grid">{decile_cells}</div>
        <p style="margin:0.3rem 0 0;" class="small-note">Decile 1 = highest risk &nbsp;·&nbsp; Decile 10 = lowest risk</p>
        <p style="margin:0.3rem 0 0;" class="small-note">Observed event rate in Decile {decile}: <b>{event_rate:.2f}%</b></p>
    </div>
    """, unsafe_allow_html=True)

    # ── PLAIN ENGLISH ──
    interp = decile_interpretation(decile, event_rate, risk)
    st.info(f"💬 **What this means:** {interp}")

    # ── FRAMEWORK CONTRIBUTIONS ──
    fw_contribs = get_framework_contributions(x)
    total_fw = sum(fw_contribs.values()) or 1

    st.markdown("### What Is Driving Your Risk")
    st.markdown("<p class='small-note'>Contribution of each behavioral theory framework to your predicted risk:</p>", unsafe_allow_html=True)

    for fw in ["SEM","TPB","HBM","ALT","Baseline"]:
        val = fw_contribs.get(fw, 0)
        pct = (val / total_fw) * 100
        if pct < 1: continue
        color = FRAMEWORK_COLORS[fw]
        short = fw if fw != "Baseline" else "Demographics"
        st.markdown(f"""
        <div style="margin:4px 0;">
            <div style="display:flex;justify-content:space-between;font-size:0.88rem;">
                <span><b style="color:{color};">■ {short}</b></span>
                <span style="color:{color};font-weight:700;">{pct:.0f}%</span>
            </div>
            <div style="background:#eee;border-radius:999px;height:8px;overflow:hidden;">
                <div style="width:{pct}%;background:{color};height:8px;border-radius:999px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── TOP RISK DRIVERS WITH ACTIONS ──
    risk_drivers, protective = contribution_list(x)

    st.markdown("### Top Risk Drivers & Actions")
    if risk_drivers:
        for name, score, fw, action in risk_drivers[:5]:
            color = FRAMEWORK_COLORS.get(fw, "#888")
            action_text = f"<br><span style='font-size:0.82rem;color:#555;'>→ {action}</span>" if action else ""
            st.markdown(f"""
            <div class="action-card action-card-red" style="border-left-color:{color};">
                <b style="color:{color};">■ {fw}</b> &nbsp; {name} &nbsp;
                <span style="font-size:0.82rem;color:#888;">(+{score:.2f} log-odds)</span>
                {action_text}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.write("• No major risk drivers identified from selected inputs.")

    st.markdown("### Protective Factors")
    if protective:
        for name, score, fw, action in protective[:3]:
            st.markdown(f"""
            <div class="action-card action-card-green">
                ✅ <b>{name}</b> &nbsp; <span style='font-size:0.82rem;color:#888;'>(-{score:.2f} log-odds)</span>
                {"<br><span style='font-size:0.82rem;color:#555;'>→ " + action + "</span>" if action else ""}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.write("• No strong protective factors selected.")

    # ── RECOMMENDATION ──
    rec_color, rec_hex, rec_title, rec_text = get_recommendation(decile)
    st.markdown(f"""
    <div class="metric-card" style="margin-top:0.8rem;">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:0.6rem;">
            <span style="color:{rec_hex};font-size:1.3rem;">●</span>
            <span style="font-weight:700;font-size:1.05rem;color:#1c2f52;">{rec_title}</span>
        </div>
        <div style="border-left:3px solid #d8dde6;padding-left:0.8rem;color:#333;font-size:0.93rem;line-height:1.5;">
            {rec_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── POPULATION BENCHMARKS ──
    with st.expander("📊 Population Benchmarks"):
        st.markdown(f"""
        <div class="benchmark-row"><span>Your predicted risk</span><b style="color:{fg};">{risk:.2f}%</b></div>
        <div class="benchmark-row"><span>National average (all adults)</span><b>5.64%</b></div>
        <div class="benchmark-row"><span>Decile {decile} observed rate</span><b>{event_rate:.2f}%</b></div>
        <div class="benchmark-row"><span>Decile 1 (highest risk)</span><b>24.99%</b></div>
        <div class="benchmark-row"><span>Decile 10 (lowest risk)</span><b>0.20%</b></div>
        <div class="benchmark-row"><span>Your risk vs. national avg</span><b style="color:{fg};">{risk/NATIONAL_AVG:.1f}×</b></div>
        """, unsafe_allow_html=True)
        if decile <= 3:
            st.markdown("💡 **Estimated Prevention Impact**")
            st.markdown(f"Research simulations suggest that identifying 1,000 individuals with similar risk profiles and preventing only 10% of expected cardiovascular events could reduce hospitalization costs by approximately **${int(1000 * (event_rate/100) * 0.10 * 21560):,}**.")

# ─────────────────────────────────────────────
# DISCLAIMER
# ─────────────────────────────────────────────
st.markdown("---")
st.info("""
**Medical Disclaimer:** This tool is for educational and risk-stratification support only, not for diagnosis or treatment.
Predictions are based on population-level associations from BRFSS-derived modeling and graduate research at the University of Central Oklahoma
Equity flags are based on fairness audit findings — the first such audit in BRFSS cardiovascular ML literature.
Always consult a licensed clinician for medical decisions.
""")

st.markdown("""
<div style="text-align:center;color:#999;font-size:0.82rem;margin-top:0.5rem;">
 Lilian Wanjiku · University of Central Oklahoma MSBA 2026 ·
CDC BRFSS 2022 · 444,975 U.S. Adults · AUC 0.84 · Lift@D1 4.43×
</div>
""", unsafe_allow_html=True)
