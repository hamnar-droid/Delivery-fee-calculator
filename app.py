import streamlit as st
import pandas as pd
from datetime import date

# ------------------ Page setup ------------------
st.set_page_config(page_title="Parcel Waybill — Delivery Fee Calculator", page_icon="📮", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&family=Inter:wght@400;500&family=JetBrains+Mono:wght@400;500&display=swap');

    .stApp {
        background-color: #E4D5B7;
    }
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .waybill-header {
        font-family: 'Special Elite', monospace;
        font-size: 30px;
        color: #2B2620;
        letter-spacing: 0.5px;
        margin-bottom: 0;
    }
    .waybill-sub {
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        color: #8A7F68;
        letter-spacing: 0.5px;
        margin-top: 2px;
        margin-bottom: 1.2em;
    }

    .perforation {
        text-align: center;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        color: #8A7F68;
        letter-spacing: 2px;
        margin: 0.6em 0 1.4em 0;
        overflow: hidden;
        white-space: nowrap;
    }

    div[data-testid="stForm"] {
        background-color: #F4ECDA;
        border: 1px solid #C7B68C;
        border-radius: 2px;
        padding: 1.6em 1.8em;
    }

    label, .stMarkdown, p, span {
        color: #2B2620;
    }
    div[data-testid="stForm"] label p {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #8A7F68 !important;
    }

    .stTextInput input, .stNumberInput input {
        background-color: #F4ECDA;
        border: none;
        border-bottom: 1px solid #C7B68C;
        border-radius: 0;
        color: #2B2620;
        font-family: 'JetBrains Mono', monospace;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-bottom: 1px solid #B23A2E;
        box-shadow: none;
    }

    div[role="radiogroup"] label span {
        font-family: 'Inter', sans-serif !important;
        text-transform: none !important;
        color: #2B2620 !important;
        font-size: 14px !important;
    }

    .stButton>button, .stFormSubmitButton>button {
        background-color: #2B2620;
        color: #F4ECDA;
        border-radius: 2px;
        border: none;
        padding: 0.6em 1.4em;
        font-family: 'Special Elite', monospace;
        letter-spacing: 0.5px;
    }
    .stButton>button:hover, .stFormSubmitButton>button:hover {
        background-color: #B23A2E;
        color: #F4ECDA;
    }

    .receipt {
        background-color: #F4ECDA;
        border: 1px solid #C7B68C;
        border-radius: 2px;
        padding: 1.4em 1.6em;
        margin-top: 1.2em;
        position: relative;
    }
    .receipt-top {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        border-bottom: 2px dashed #C7B68C;
        padding-bottom: 0.7em;
        margin-bottom: 0.9em;
    }
    .receipt-title {
        font-family: 'Special Elite', monospace;
        font-size: 18px;
        color: #2B2620;
    }
    .receipt-track {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        color: #8A7F68;
        margin-top: 4px;
    }
    .fragile-tag {
        border: 1.5px solid #B23A2E;
        color: #B23A2E;
        font-family: 'Special Elite', monospace;
        font-size: 10px;
        padding: 3px 8px;
        transform: rotate(3deg);
        white-space: nowrap;
    }
    .receipt-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.8em 1.2em;
        margin-bottom: 1em;
    }
    .receipt-field-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        color: #8A7F68;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .receipt-field-value {
        font-size: 14px;
        color: #2B2620;
        border-bottom: 1px solid #C7B68C;
        padding: 4px 0;
    }
    .receipt-totals {
        border-top: 2px dashed #C7B68C;
        padding-top: 0.9em;
        position: relative;
    }
    .receipt-line {
        display: flex;
        justify-content: space-between;
        font-size: 13px;
        color: #6B6250;
        margin-bottom: 4px;
    }
    .receipt-line span:last-child {
        font-family: 'JetBrains Mono', monospace;
    }
    .receipt-total-final {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 8px;
    }
    .receipt-total-final .label {
        font-family: 'Special Elite', monospace;
        font-size: 15px;
        color: #2B2620;
    }
    .receipt-total-final .value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 22px;
        color: #2B2620;
        font-weight: 500;
    }
    .postmark {
        position: absolute;
        right: 6px;
        top: 6px;
        width: 76px;
        height: 76px;
        border: 2px solid #34547A;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        transform: rotate(-12deg);
        opacity: 0.9;
    }
    .postmark-inner {
        width: 64px;
        height: 64px;
        border: 1px dashed #34547A;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    .postmark-inner span {
        font-family: 'Special Elite', monospace;
        font-size: 10px;
        color: #34547A;
        line-height: 1.3;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #C7B68C;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="waybill-header">Parcel waybill</p>', unsafe_allow_html=True)
st.markdown('<p class="waybill-sub">DELIVERY FEE CALCULATOR &nbsp;·&nbsp; PESHAWAR DEPOT</p>', unsafe_allow_html=True)

# ------------------ Session state ------------------
# Keeps a running record of every customer calculated in this session,
# which mirrors the "loop until user types stop" behaviour of the
# original console program (Requirement 1).
if "bills" not in st.session_state:
    st.session_state.bills = []
if "tracking_seq" not in st.session_state:
    st.session_state.tracking_seq = 41  # first parcel becomes PW-00042


def calculate_delivery(customer_name, package_weight, delivery_distance, is_fragile):
    """
    Same core pricing logic as the original console function:
    - base cost = flat fee + weight rate + distance rate
    - surcharge of $5 if distance > 10km OR package is fragile (Requirement 3)
    """
    base_cost = 5 + (package_weight * 2) + (delivery_distance * 0.5)
    surcharge = 5 if (delivery_distance > 10 or is_fragile) else 0
    final_cost = base_cost + surcharge

    return {
        "Customer": customer_name,
        "Weight (kg)": package_weight,
        "Distance (km)": delivery_distance,
        "Fragile": "Yes" if is_fragile else "No",
        "Base Cost ($)": round(base_cost, 2),
        "Surcharge ($)": round(surcharge, 2),
        "Final Bill ($)": round(final_cost, 2),
    }


# ------------------ Input form ------------------
# Requirement 2: capture all 4 inputs with correct data types, and
# handle invalid input gracefully (no crashes on bad values).
with st.form("delivery_form", clear_on_submit=True):
    customer_name = st.text_input("Customer")
    col1, col2 = st.columns(2)
    with col1:
        package_weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1, format="%.2f")
    with col2:
        delivery_distance = st.number_input("Distance (km)", min_value=0.0, step=0.1, format="%.2f")
    is_fragile = st.radio("Fragile?", ["No", "Yes"], horizontal=True)

    submitted = st.form_submit_button("Stamp waybill")

    if submitted:
        if customer_name.strip() == "":
            st.error("Enter a customer name.")
        elif package_weight <= 0 or delivery_distance <= 0:
            st.error("Weight and distance must be greater than 0.")
        else:
            fragile_bool = is_fragile == "Yes"
            bill = calculate_delivery(customer_name.strip(), package_weight, delivery_distance, fragile_bool)
            st.session_state.tracking_seq += 1
            bill["Tracking"] = f"PW-{st.session_state.tracking_seq:05d}"
            st.session_state.bills.append(bill)

st.markdown(
    '<div class="perforation">✂ ' + ('- ' * 60) + '</div>',
    unsafe_allow_html=True,
)

# ------------------ Show latest bill as a receipt ------------------
if st.session_state.bills:
    latest = st.session_state.bills[-1]
    fragile_tag_html = '<div class="fragile-tag">FRAGILE</div>' if latest["Fragile"] == "Yes" else ""

    st.markdown(f"""
        <div class="receipt">
            <div class="receipt-top">
                <div>
                    <div class="receipt-title">{latest['Customer']}</div>
                    <div class="receipt-track">TRACKING NO. {latest['Tracking']}</div>
                </div>
                {fragile_tag_html}
            </div>
            <div class="receipt-grid">
                <div>
                    <div class="receipt-field-label">Weight</div>
                    <div class="receipt-field-value">{latest['Weight (kg)']} kg</div>
                </div>
                <div>
                    <div class="receipt-field-label">Distance</div>
                    <div class="receipt-field-value">{latest['Distance (km)']} km</div>
                </div>
            </div>
            <div class="receipt-totals">
                <div class="receipt-line"><span>Base cost</span><span>${latest['Base Cost ($)']}</span></div>
                <div class="receipt-line"><span>Surcharge</span><span>${latest['Surcharge ($)']}</span></div>
                <div class="receipt-total-final">
                    <span class="label">Total due</span>
                    <span class="value">${latest['Final Bill ($)']}</span>
                </div>
                <div class="postmark">
                    <div class="postmark-inner">
                        <span>PAID<br>{date.today().strftime('%d %b')}</span>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ------------------ Full history table ------------------
if len(st.session_state.bills) > 1:
    st.markdown('<p class="waybill-sub" style="margin-top:1.6em;">MANIFEST — ALL PARCELS THIS SESSION</p>', unsafe_allow_html=True)
    df = pd.DataFrame(st.session_state.bills)
    df = df[["Tracking", "Customer", "Weight (kg)", "Distance (km)", "Fragile", "Base Cost ($)", "Surcharge ($)", "Final Bill ($)"]]
    st.dataframe(df, use_container_width=True, hide_index=True)

    total_revenue = df["Final Bill ($)"].sum()
    st.markdown(
        f'<p style="font-family:\'JetBrains Mono\', monospace; font-size:13px; color:#2B2620;">'
        f'Total collected this session: <b>${total_revenue:.2f}</b></p>',
        unsafe_allow_html=True,
    )

# ------------------ Reset ------------------
if st.session_state.bills:
    if st.button("Clear manifest"):
        st.session_state.bills = []
        st.rerun()

st.markdown(
    '<p style="font-family:\'JetBrains Mono\', monospace; font-size:11px; color:#8A7F68; margin-top:2em;">'
    'Base cost = $5 flat fee + (weight × $2) + (distance × $0.5). '
    '$5 surcharge applies if distance &gt; 10km or the package is fragile.</p>',
    unsafe_allow_html=True,
)
