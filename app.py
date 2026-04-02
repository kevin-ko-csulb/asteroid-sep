import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="SEP Asteroid Retrieval", layout="wide")

st.markdown("""
<style>
    /* Compact Main Area */
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 0.5rem !important;
    }
    /* Compact Sidebar */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0.2rem !important;
    }
    [data-testid="stSidebar"] div.stSlider {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }
    /* Compact Metrics */
    [data-testid="stMetricLabel"] p {
        font-size: 0.85rem !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.4rem !important;
        line-height: 1.2 !important;
    }
    /* Compact Separators */
    hr {
        margin-top: 0.2rem !important;
        margin-bottom: 0.2rem !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("Asteroid Retrieval using Solar Electric Propulsion")

# Initial Mission Defaults
if 'dv_out' not in st.session_state:
    st.session_state.dv_out = 4500.0
    st.session_state.dv_ret = 4500.0
    st.session_state.m_dry = 10000.0
    st.session_state.m_ast = 55000.0
    st.session_state.T = 4.8
    st.session_state.Isp = 2400.0

st.sidebar.header("Propulsion System")

if 'prop_mode_key' not in st.session_state:
    st.session_state.prop_mode_key = "Solar Electric Propulsion (SEP)"
if 'sep_mode_key' not in st.session_state:
    st.session_state.sep_mode_key = "X3 Hall Effect Thruster"

def update_propulsion_from_preset():
    mode = st.session_state.prop_mode_key
    if mode == "Chemical (Bi-prop)":
        st.session_state.Isp = 316.0
        st.session_state.T = 0.0
    elif mode == "Nuclear Thermal Propulsion (NTP)":
        st.session_state.Isp = 900.0
        st.session_state.T = 0.0
    elif mode == "Solar Electric Propulsion (SEP)":
        sep = st.session_state.get("sep_mode_key", "X3 Hall Effect Thruster")
        if sep == "X3 Hall Effect Thruster":
            st.session_state.Isp = 2400.0
            st.session_state.T = 4.8
        elif sep == "Gridded Ion Thruster":
            st.session_state.Isp = 4500.0
            st.session_state.T = 2.5
        elif sep == "AEPS":
            st.session_state.Isp = 2700.0
            st.session_state.T = 3.6

st.sidebar.radio(
    "Category:",
    ["Solar Electric Propulsion (SEP)", "Chemical (Bi-prop)", "Nuclear Thermal Propulsion (NTP)", "Custom (Manual)"],
    key="prop_mode_key",
    on_change=update_propulsion_from_preset
)

if st.session_state.prop_mode_key == "Solar Electric Propulsion (SEP)":
    st.sidebar.selectbox(
        "SEP System:", 
        ["X3 Hall Effect Thruster", "Gridded Ion Thruster", "AEPS"],
        key="sep_mode_key",
        on_change=update_propulsion_from_preset
    )

def set_custom_prop():
    st.session_state.prop_mode_key = "Custom (Manual)"

st.sidebar.markdown("---")
st.sidebar.header("Mission & System Parameters")

T = st.sidebar.slider("Thrust T (N) [0=Instant]", 0.0, 10.0, key="T", on_change=set_custom_prop, step=0.1)
Isp = st.sidebar.slider("Isp (s)", 100.0, 5000.0, key="Isp", on_change=set_custom_prop, step=10.0)
dv_out = st.sidebar.slider("Δv_outbound (m/s)", 0.0, 6000.0, key="dv_out", step=10.0)
dv_ret = st.sidebar.slider("Δv_return (m/s)", 0.0, 6000.0, key="dv_ret", step=10.0)
m_dry = st.sidebar.slider("Spacecraft dry mass m_dry (kg)", 1000.0, 30000.0, key="m_dry", step=100.0)
m_ast = st.sidebar.slider("Asteroid mass m_ast (kg)", 0.0, 60000.0, key="m_ast", step=100.0)

# Input validations
if Isp <= 0:
    st.error("Isp must be > 0.")
    st.stop()
if T < 0:
    st.error("Thrust cannot be negative.")
    st.stop()
if m_dry < 0 or m_ast < 0:
    st.error("Masses cannot be negative.")
    st.stop()

# PHYSICS / EQUATIONS
g0 = 9.80665
v_e = Isp * g0

m_return = m_dry + m_ast
m_after_capture = m_return * np.exp(dv_ret / v_e)
m_fuel_return = m_after_capture - m_return

m_pre_capture = m_after_capture - m_ast
m0 = m_pre_capture * np.exp(dv_out / v_e)

m_fuel_outbound = m0 - m_pre_capture
m_fuel_total = m_fuel_outbound + m_fuel_return

# OUTPUTS
st.subheader("Mission Results")

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Outbound Fuel", f"{m_fuel_outbound:,.0f} kg")
m2.metric("Return Fuel", f"{m_fuel_return:,.0f} kg")
m3.metric("Total Fuel", f"{m_fuel_total:,.0f} kg")

if T > 0:
    m_avg_out = (m0 + m_pre_capture) / 2
    t_out_days = (m_avg_out * dv_out / T) / 86400
    m_avg_ret = (m_after_capture + m_return) / 2
    t_ret_days = (m_avg_ret * dv_ret / T) / 86400
    m4.metric("Outbound Burn", f"{t_out_days:,.1f} d")
    m5.metric("Return Burn", f"{t_ret_days:,.1f} d")
else:
    m4.metric("Outbound Burn", "Instant")
    m5.metric("Return Burn", "Instant")

st.markdown("**Intermediate Masses:**")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Start Outbound", f"{m0:,.0f} kg")
c2.metric("Pre-Capture", f"{m_pre_capture:,.0f} kg")
c3.metric("After Capture", f"{m_after_capture:,.0f} kg")
c4.metric("End Return", f"{m_return:,.0f} kg")

st.markdown("---")

col_plot1, col_plot2 = st.columns([2, 1])

with col_plot1:
    st.markdown("**Mass breakdown at key mission points**")
    fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.5), sharey=True)

    # Outbound Leg
    labels_out = ["Start Outbound", "Pre-capture"]
    dry_out = np.array([m_dry, m_dry])
    ret_fuel_out = np.array([m_fuel_return, m_fuel_return])
    out_fuel_out = np.array([m_fuel_outbound, 0.0])

    ax1.bar(labels_out, dry_out, label="Dry Mass", color="#7f7f7f")
    ax1.bar(labels_out, ret_fuel_out, bottom=dry_out, label="Return Fuel", color="#ff7f0e")
    ax1.bar(labels_out, out_fuel_out, bottom=dry_out+ret_fuel_out, label="Outbound Fuel", color="#1f77b4")
    ax1.set_ylabel("Mass (kg)")
    ax1.set_title("Outbound Leg")
    ax1.legend(fontsize=8)

    # Return Leg
    labels_ret = ["After Capture", "End Return"]
    dry_ret = np.array([m_dry, m_dry])
    ret_fuel_ret = np.array([m_fuel_return, 0.0])
    ast_ret = np.array([m_ast, m_ast])

    ax2.bar(labels_ret, dry_ret, label="Dry Mass", color="#7f7f7f")
    ax2.bar(labels_ret, ret_fuel_ret, bottom=dry_ret, label="Return Fuel", color="#ff7f0e")
    ax2.bar(labels_ret, ast_ret, bottom=dry_ret+ret_fuel_ret, label="Asteroid Mass", color="#8c564b")
    ax2.set_title("Return Leg")
    ax2.legend(fontsize=8)
    plt.tight_layout()

    st.pyplot(fig1)

with col_plot2:
    st.markdown("**Fuel totals**")
    fig2, ax_fuel = plt.subplots(figsize=(4, 3.5))
    fuel_labels = ["Outbound", "Return", "Total"]
    fuel_vals = [m_fuel_outbound, m_fuel_return, m_fuel_total]
    ax_fuel.bar(fuel_labels, fuel_vals, color=["#1f77b4", "#ff7f0e", "#2ca02c"])
    ax_fuel.set_ylabel("Fuel Mass (kg)")
    ax_fuel.set_title("Fuel Totals")
    for i, v in enumerate(fuel_vals):
        ax_fuel.text(i, v + m_fuel_total*0.02, f"{v:,.0f}", ha='center', va='bottom', fontsize=9)
    ax_fuel.set_ylim(0, max(fuel_vals)*1.2)
    fig2.tight_layout()

    st.pyplot(fig2)
