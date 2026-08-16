import streamlit as st
import pandas as pd

# ------------------ Page setup ------------------
st.set_page_config(page_title="Delivery Fee Calculator", page_icon="🚚", layout="centered")

st.markdown("""
    <style>
    .main {
        background-color: #fff8f0;
    }
    .stButton>button {
        background-color: #ff8fa3;
        color: white;
        border-radius: 12px;
        border: none;
        padding: 0.6em 1.2em;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #ff6f91;
        color: white;
    }
    .bill-card {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 1.2em;
        margin-top: 1em;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
        border-left: 6px solid #ff8fa3;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚚 Delivery Fee Calculator")
st.caption("Enter package details below and get an instant delivery bill 💌")

# ------------------ Session state ------------------
# Keeps a running record of every customer calculated in this session,
# which mirrors the "loop until user types stop" behaviour of the
# original console program (Requirement 1).
if "bills" not in st.session_state:
    st.session_state.bills = []


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
    st.subheader("📦 Package Details")

    customer_name = st.text_input("Customer Name")
    package_weight = st.number_input("Package Weight (kg)", min_value=0.0, step=0.1, format="%.2f")
    delivery_distance = st.number_input("Delivery Distance (km)", min_value=0.0, step=0.1, format="%.2f")
    is_fragile = st.radio("Is the package fragile?", ["No", "Yes"], horizontal=True)

    submitted = st.form_submit_button("Calculate Bill 🧾")

    if submitted:
        if customer_name.strip() == "":
            st.error("Please enter a customer name.")
        elif package_weight <= 0 or delivery_distance <= 0:
            st.error("Weight and distance must be greater than 0.")
        else:
            fragile_bool = is_fragile == "Yes"
            bill = calculate_delivery(customer_name.strip(), package_weight, delivery_distance, fragile_bool)
            st.session_state.bills.append(bill)
            st.success(f"Bill calculated for {bill['Customer']} 🎉")

# ------------------ Show latest bill ------------------
if st.session_state.bills:
    latest = st.session_state.bills[-1]
    st.markdown(f"""
        <div class="bill-card">
            <h4>🧾 Latest Bill — {latest['Customer']}</h4>
            <p>Weight: {latest['Weight (kg)']} kg &nbsp;|&nbsp; Distance: {latest['Distance (km)']} km &nbsp;|&nbsp; Fragile: {latest['Fragile']}</p>
            <p>Base Cost: ${latest['Base Cost ($)']}<br>
            Surcharge: ${latest['Surcharge ($)']}<br>
            <b>Final Bill: ${latest['Final Bill ($)']}</b></p>
        </div>
    """, unsafe_allow_html=True)

# ------------------ Full history table ------------------
if len(st.session_state.bills) > 1:
    st.subheader("📋 All Customers This Session")
    df = pd.DataFrame(st.session_state.bills)
    st.dataframe(df, use_container_width=True)

    total_revenue = df["Final Bill ($)"].sum()
    st.info(f"💰 Total revenue this session: **${total_revenue:.2f}**")

# ------------------ Reset ------------------
if st.session_state.bills:
    if st.button("🔄 Start Over (clear all customers)"):
        st.session_state.bills = []
        st.rerun()

st.markdown("---")
st.caption("Base cost = $5 flat fee + (weight × $2) + (distance × $0.5). "
           "A $5 surcharge applies if distance > 10km OR the package is fragile.")
