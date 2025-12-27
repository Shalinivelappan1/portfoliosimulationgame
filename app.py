# PASTE YOUR FULL STREAMLIT APP CODE HERE
import streamlit as st
import pandas as pd
from io import BytesIO

# =================================================
# CONFIG
# =================================================
st.set_page_config(
    page_title="Portfolio Simulation – AlgoTraSim",
    layout="wide"
)

ROWS = 25
CAPITAL_LIMIT = 100000  # ₹1,00,000

# =================================================
# HEADER
# =================================================
st.title("📊 Portfolio Simulation – Scenario-Based Allocation-Developed by Prof.Shalini Velappan, IIM Trichy")
st.caption("Academic simulation | Not investment advice")

# =================================================
# STUDENT DETAILS (MANDATORY)
# =================================================
with st.sidebar:
    st.header("👤 Student Details")
    student_name = st.text_input("Student Name", key="student_name")
    roll_no = st.text_input("Roll Number", key="roll_no")

if not student_name or not roll_no:
    st.warning("Please enter Student Name and Roll Number to proceed.")
    st.stop()

# =================================================
# HELPER FUNCTIONS
# =================================================
def create_table():
    return pd.DataFrame({
        "SL. NO.": list(range(1, ROWS + 1)),
        "Stock": ["" for _ in range(ROWS)],
        "Price (₹)": [0.0 for _ in range(ROWS)],
        "AlgoTraSim Qty": [0 for _ in range(ROWS)],
        "Your Qty": [0 for _ in range(ROWS)]
    })

def total_investment(df):
    return (df["Price (₹)"] * df["Your Qty"]).sum()

def risk_label(df):
    if df["Your Qty"].sum() == 0:
        return "Neutral"
    return "Aggressive" if df["Your Qty"].astype(float).std() > 10 else "Defensive"

def export_excel(df, justification, scenario):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Portfolio")
        pd.DataFrame({
            "Student Name": [student_name],
            "Roll Number": [roll_no],
            "Scenario": [scenario],
            "Justification": [justification]
        }).to_excel(writer, index=False, sheet_name="Justification")
    return output.getvalue()

# =================================================
# SESSION STATE INITIALIZATION
# =================================================
for key in ["baseline", "war", "capital"]:
    if key not in st.session_state:
        st.session_state[key] = create_table()
        st.session_state[f"{key}_just"] = ""

# =================================================
# SCENARIO TABS
# =================================================
tab1, tab2, tab3 = st.tabs(
    ["📈 Baseline", "⚠️ War / Global Shock", "💰 Capital Increase"]
)

# =================================================
# BASELINE SCENARIO
# =================================================
with tab1:
    st.subheader("📈 Baseline Scenario")

    st.session_state.baseline = st.data_editor(
        st.session_state.baseline,
        use_container_width=True,
        num_rows="fixed",
        disabled=["SL. NO."],
        key="editor_baseline"
    )

    total = total_investment(st.session_state.baseline)
    if total <= CAPITAL_LIMIT:
        st.success(f"Total Investment: ₹{total:,.0f}")
    else:
        st.error(f"Total exceeds ₹1,00,000 → ₹{total:,.0f}")

    st.info(f"Risk Profile: **{risk_label(st.session_state.baseline)}**")

    st.session_state.baseline_just = st.text_area(
        "Justification (Baseline)",
        value=st.session_state.baseline_just,
        height=120,
        key="just_baseline"
    )

    if st.button("➡️ Carry Forward to War Scenario", key="carry_baseline"):
        st.session_state.war = st.session_state.baseline.copy()

    st.download_button(
        label="📥 Download Baseline (Excel)",
        data=export_excel(
            st.session_state.baseline,
            st.session_state.baseline_just,
            "Baseline"
        ),
        file_name=f"{roll_no}_Baseline.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="download_baseline"
    )

# =================================================
# WAR / GLOBAL SHOCK SCENARIO
# =================================================
with tab2:
    st.subheader("⚠️ War / Global Shock Scenario")

    st.session_state.war = st.data_editor(
        st.session_state.war,
        use_container_width=True,
        num_rows="fixed",
        disabled=["SL. NO."],
        key="editor_war"
    )

    total = total_investment(st.session_state.war)
    if total <= CAPITAL_LIMIT:
        st.success(f"Total Investment: ₹{total:,.0f}")
    else:
        st.error(f"Total exceeds ₹1,00,000 → ₹{total:,.0f}")

    st.info(f"Risk Profile: **{risk_label(st.session_state.war)}**")

    st.session_state.war_just = st.text_area(
        "Justification (War Scenario)",
        value=st.session_state.war_just,
        height=120,
        key="just_war"
    )

    if st.button("➡️ Carry Forward to Capital Increase Scenario", key="carry_war"):
        st.session_state.capital = st.session_state.war.copy()

    st.download_button(
        label="📥 Download War Scenario (Excel)",
        data=export_excel(
            st.session_state.war,
            st.session_state.war_just,
            "War / Global Shock"
        ),
        file_name=f"{roll_no}_War.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="download_war"
    )

# =================================================
# CAPITAL INCREASE SCENARIO
# =================================================
with tab3:
    st.subheader("💰 Capital Increase Scenario")

    st.session_state.capital = st.data_editor(
        st.session_state.capital,
        use_container_width=True,
        num_rows="fixed",
        disabled=["SL. NO."],
        key="editor_capital"
    )

    total = total_investment(st.session_state.capital)
    if total <= CAPITAL_LIMIT:
        st.success(f"Total Investment: ₹{total:,.0f}")
    else:
        st.error(f"Total exceeds ₹1,00,000 → ₹{total:,.0f}")

    st.info(f"Risk Profile: **{risk_label(st.session_state.capital)}**")

    st.session_state.capital_just = st.text_area(
        "Justification (Capital Increase)",
        value=st.session_state.capital_just,
        height=120,
        key="just_capital"
    )

    st.download_button(
        label="📥 Download Capital Increase (Excel)",
        data=export_excel(
            st.session_state.capital,
            st.session_state.capital_just,
            "Capital Increase"
        ),
        file_name=f"{roll_no}_Capital.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="download_capital"
    )

# =================================================
# FOOTER
# =================================================
st.markdown("---")
st.caption("© Academic Simulation | Portfolio Decision-Making under Uncertainty")
