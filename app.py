import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="SEP Asteroid Mass Calculator", layout="wide")

st.markdown("""
<style>
    /* Compact Main Area & Sidebar Top */
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 0.5rem !important;
    }
    /* Protect the collapser button's click area */
    [data-testid="stSidebarHeader"], [data-testid="collapsedControl"] {
        position: relative !important;
        z-index: 99999 !important;
    }
    [data-testid="stSidebarUserContent"] {
        padding-top: 0rem !important;
    }
    /* Force content upwards aggressively but safely */
    [data-testid="stSidebarUserContent"] > div:first-child {
        margin-top: -2.0rem !important;
    }
    /* Extreme sledgehammer to unconditionally compress ALL bounds of the number box equally */
    [data-testid="stSidebar"] [data-testid="stNumberInput"] div {
        min-height: 1.8rem !important;
        height: 1.8rem !important;
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }
    [data-testid="stSidebar"] [data-testid="stNumberInput"] input {
        min-height: 1.8rem !important;
        height: 1.8rem !important;
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }
    /* Apply the identical squish strictly to the Selectbox interactive box so it matches */
    [data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"],
    [data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        min-height: 1.8rem !important;
        height: 1.8rem !important;
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        align-items: center !important;
    }


    /* Compact Sidebar */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0rem !important;
    }
    [data-testid="stSidebar"] div.stSlider {
        padding-top: 0.6rem !important;
        padding-bottom: 0.4rem !important;
    }
    /* Compact Metrics */
    [data-testid="stMetricLabel"] p {
        font-size: 0.85rem !important;
    }
    /* Compact Radio and Selectbox */
    [data-testid="stSidebar"] .stRadio label p, [data-testid="stSidebar"] .stSelectbox label p {
        font-size: 0.82rem !important;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] {
        gap: 0.1rem !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.4rem !important;
        line-height: 1.2 !important;
    }
    /* Compact Separators */
    hr {
        margin-top: 0.8rem !important;
        margin-bottom: 0.9rem !important;
    }
    /* Hide slider number tooltip */
    [data-testid="stThumbValue"] {
        display: none !important;
    }
    /* Force label and number input to remain on the same line in sidebar */
    [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        align-items: center !important;
    }
    [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] > div {
        min-width: 0 !important;
    }
    /* Pull the red tooltip number closer down to the slider line */
    .stSlider div[data-testid="stThumbValue"] {
        margin-top: 0.4rem !important;
        font-size: 0.85rem !important;
    }
    /* Force min/max labels to physically shift upwards closer to the track */
    .stSlider [data-testid="stTickBar"], 
    .stSlider [data-testid="stTickBarMin"], .stSlider [data-testid="stTickBarMax"],
    .stSlider div[data-baseweb="slider"] > div:last-child {
        transform: translateY(-0.4rem) !important;
        font-size: 0.75rem !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("Asteroid Retrieval Fuel Mass Calculator")

# Initial Mission Defaults
if 'dv_out' not in st.session_state:
    st.session_state.dv_out = 4340.5
    st.session_state.dv_ret = 4340.5
    st.session_state.m_dry = 10000.0
    st.session_state.m_ast = 55000.0
    st.session_state.T = 4.8
    st.session_state.Isp = 2400.0

st.sidebar.markdown("**Mission Parameters**")

def slider_with_input(label, min_value, max_value, key, step=1.0, on_change=None):
    num_key = f"{key}_num"
    sld_key = f"{key}_sld"
    if num_key not in st.session_state: st.session_state[num_key] = st.session_state[key]
    if sld_key not in st.session_state: st.session_state[sld_key] = st.session_state[key]
    def update_from_num():
        st.session_state[key] = st.session_state[num_key]
        st.session_state[sld_key] = st.session_state[num_key]
        if on_change: on_change()
    def update_from_sld():
        st.session_state[key] = st.session_state[sld_key]
        st.session_state[num_key] = st.session_state[sld_key]
        if on_change: on_change()

    col1, col2 = st.sidebar.columns([6, 4])
    with col1:
        st.markdown(label)
    with col2:
        st.number_input(label, min_value=float(min_value), max_value=float(max_value), 
                        step=float(step), key=num_key, label_visibility="collapsed",
                        on_change=update_from_num)
    st.sidebar.slider(label, min_value=float(min_value), max_value=float(max_value), 
                      step=float(step), key=sld_key, label_visibility="collapsed",
                      on_change=update_from_sld)
    return st.session_state[key]

dv_out = slider_with_input(r"$\Delta v_{out}$ (m/s)", 0.0, 6000.0, "dv_out", step=10.0)
dv_ret = slider_with_input(r"$\Delta v_{ret}$ (m/s)", 0.0, 6000.0, "dv_ret", step=10.0)
m_dry = slider_with_input(r"Dry Mass, $m_{dry}$ (kg)", 1000.0, 30000.0, "m_dry", step=100.0)
m_ast = slider_with_input(r"Asteroid Mass, $m_{ast}$ (kg)", 0.0, 60000.0, "m_ast", step=100.0)

st.sidebar.markdown("---")
st.sidebar.markdown("**Propulsion System**")

if 'prop_mode_key' not in st.session_state:
    st.session_state.prop_mode_key = "Solar Electric Propulsion (SEP)"
if 'sep_mode_key' not in st.session_state:
    st.session_state.sep_mode_key = "X3 Hall Effect Thruster"

def update_propulsion_from_preset():
    mode = st.session_state.prop_mode_key
    def set_isp_t(isp, t):
        st.session_state.Isp = isp
        st.session_state.Isp_num = isp
        st.session_state.Isp_sld = isp
        st.session_state.T = t
        st.session_state.T_num = t
        st.session_state.T_sld = t

    if mode == "Chemical (Bi-prop)":
        set_isp_t(316.0, 0.0)
    elif mode == "Nuclear Thermal Propulsion (NTP)":
        set_isp_t(900.0, 0.0)
    elif mode == "Solar Electric Propulsion (SEP)":
        sep = st.session_state.get("sep_mode_key", "X3 Hall Effect Thruster")
        if sep == "X3 Hall Effect Thruster":
            set_isp_t(2400.0, 4.8)
        elif sep == "Gridded Ion Thruster":
            set_isp_t(4500.0, 2.5)
        elif sep == "AEPS":
            set_isp_t(2700.0, 3.6)

st.sidebar.radio(
    "Category:",
    ["Solar Electric Propulsion (SEP)", "Chemical (Bi-prop)", "Nuclear Thermal Propulsion (NTP)", "Custom (Manual)"],
    key="prop_mode_key",
    on_change=update_propulsion_from_preset
)

is_sep = st.session_state.prop_mode_key == "Solar Electric Propulsion (SEP)"

if not is_sep:
    st.sidebar.markdown('<style>div[data-testid="stSelectbox"] { visibility: hidden; pointer-events: none; }</style>', unsafe_allow_html=True)

st.sidebar.selectbox(
    "SEP System:", 
    ["X3 Hall Effect Thruster", "Gridded Ion Thruster", "AEPS"],
    key="sep_mode_key",
    disabled=not is_sep,
    on_change=update_propulsion_from_preset
)

def set_custom_prop():
    st.session_state.prop_mode_key = "Custom (Manual)"

st.sidebar.markdown("---")
st.sidebar.markdown("**Propulsion Parameters**")

Isp = slider_with_input(r"$I_{sp}$ (s)", 100.0, 5000.0, "Isp", step=10.0, on_change=set_custom_prop)

if st.session_state.prop_mode_key in ["Solar Electric Propulsion (SEP)", "Custom (Manual)"]:
    T = slider_with_input(r"Thrust $T$ (N)", 0.0, 10.0, "T", step=0.1, on_change=set_custom_prop)
else:
    T = 0.0

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

m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("Outbound Fuel", f"{m_fuel_outbound:,.0f} kg", help=r"""**Outbound Fuel:**

$$
m_{\mathrm{fuel,out}} = m_0 - m_{\mathrm{pre}}
$$""")
m2.metric("Return Fuel", f"{m_fuel_return:,.0f} kg", help=r"""**Return Fuel:**

$$
m_{\mathrm{fuel,ret}} = m_{\mathrm{after}} - m_{\mathrm{ret}}
$$""")
m3.metric("Total Fuel", f"{m_fuel_total:,.0f} kg", help=r"""**Total Fuel:**

$$
m_{\mathrm{total}} = m_{\mathrm{fuel,out}} + m_{\mathrm{fuel,ret}}
$$""")

if st.session_state.prop_mode_key in ["Solar Electric Propulsion (SEP)", "Custom (Manual)"]:
    if T > 0:
        t_out_days = (m_fuel_outbound * v_e / T) / 86400
        t_ret_days = (m_fuel_return * v_e / T) / 86400
        mdot_mg_s = (T / v_e) * 1e6
        m4.metric("Outbound Burn", f"{t_out_days:,.1f} d", help=r"""**Exact Burn Time:**

$$
t_{\mathrm{out}} = \frac{m_{\mathrm{fuel,out}} \cdot I_{\mathrm{sp}} \cdot g_0}{T}
$$""")
        m5.metric("Return Burn", f"{t_ret_days:,.1f} d", help=r"""**Exact Burn Time:**

$$
t_{\mathrm{ret}} = \frac{m_{\mathrm{fuel,ret}} \cdot I_{\mathrm{sp}} \cdot g_0}{T}
$$""")
        m6.metric("Mass Flow", f"{mdot_mg_s:,.1f} mg/s", help=r"""**Mass Flow Rate:**

$$
\dot{m} = \frac{T}{I_{\mathrm{sp}} \cdot g_0}
$$""")
    else:
        m4.metric("Outbound Burn", "Infinite", help=r"""**Burn Time:**

$$
t_{\mathrm{out}} = \infty \quad \text{(Zero Thrust)}
$$""")
        m5.metric("Return Burn", "Infinite", help=r"""**Burn Time:**

$$
t_{\mathrm{ret}} = \infty \quad \text{(Zero Thrust)}
$$""")
        m6.metric("Mass Flow", "0.0 mg/s", help=r"""**Mass Flow Rate:**

$$
\dot{m} = 0 \quad \text{(Zero Thrust)}
$$""")
else:
    m4.metric("Outbound Burn", "Instant", help="Instantaneous orbit maneuver via high-thrust propulsion")
    m5.metric("Return Burn", "Instant", help="Instantaneous orbit maneuver via high-thrust propulsion")
    m6.metric("Mass Flow", "N/A", help="Not applicable for impulsive trajectory models")

st.markdown("**Intermediate Masses:**")
c1, c2, c3, c4 = st.columns(4)
c1.metric(r"Start Outbound ($m_0$)", f"{m0:,.0f} kg", help=r"""**Tsiolkovsky Rocket Eq:**

$$
m_0 = m_{\mathrm{pre}} \cdot \exp\left(\frac{\Delta v_{\mathrm{out}}}{I_{\mathrm{sp}} \cdot g_0}\right)
$$""")
c2.metric(r"Pre-Capture ($m_{\mathrm{pre}}$)", f"{m_pre_capture:,.0f} kg", help=r"""**Before Capture:**

$$
m_{\mathrm{pre}} = m_{\mathrm{after}} - m_{\mathrm{ast}}
$$""")
c3.metric(r"After Capture ($m_{\mathrm{after}}$)", f"{m_after_capture:,.0f} kg", help=r"""**Tsiolkovsky Rocket Eq:**

$$
m_{\mathrm{after}} = m_{\mathrm{ret}} \cdot \exp\left(\frac{\Delta v_{\mathrm{ret}}}{I_{\mathrm{sp}} \cdot g_0}\right)
$$""")
c4.metric(r"End Return ($m_{\mathrm{ret}}$)", f"{m_return:,.0f} kg", help=r"""**Final Target Mass:**

$$
m_{\mathrm{ret}} = m_{\mathrm{dry}} + m_{\mathrm{ast}}
$$""")

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
