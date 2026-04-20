import streamlit as st
import math

# ====== CONFIG ======
st.set_page_config(
    page_title="LS Calculator",
    page_icon="📊",
    layout="centered"
)

# ====== CUSTOM STYLE ======
st.markdown("""
<style>
.main {
    background-color: #0f172a;
}
h1, h2, h3, label {
    color: #e2e8f0 !important;
}
.stNumberInput input {
    background-color: #1e293b !important;
    color: white !important;
    border-radius: 8px;
}
.stSelectbox div {
    background-color: #1e293b !important;
    color: white !important;
}
.stButton button {
    background: linear-gradient(90deg, #38bdf8, #6366f1);
    color: white;
    border-radius: 10px;
    font-weight: bold;
}
.result-box {
    background: #1e293b;
    padding: 20px;
    border-radius: 12px;
    margin-top: 20px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
}
</style>
""", unsafe_allow_html=True)

# ====== HEADER ======
st.title("📊 Kalkulator LS (USLE)")
st.caption("Perhitungan faktor panjang & kemiringan lereng untuk analisis erosi tanah")

# ====== INPUT SECTION ======
st.subheader("🔧 Input Data")

col1, col2 = st.columns(2)

with col1:
    lambda_val = st.number_input("Panjang lereng (λ) [m]", min_value=0.0)

with col2:
    S_val = st.number_input("Kemiringan lereng (S)", min_value=0.0)

S_unit = st.selectbox("Satuan kemiringan", ["%", "°"])

# ====== FUNCTION ======
def convert_slope_to_percent(S_val, S_unit):
    if S_unit == "°":
        return math.tan(math.radians(S_val)) * 100
    return S_val

def convert_slope_to_degrees(S_percent):
    return math.degrees(math.atan(S_percent / 100))

def calculate_m(S_percent):
    if S_percent < 1:
        return 0.2
    elif S_percent < 3:
        return 0.3
    elif S_percent < 5:
        return 0.4
    else:
        return 0.5

def calculate_L(lambda_val, m):
    if lambda_val == 0:
        return 0
    return (lambda_val / 22.13) ** m

def calculate_S_factor(S_val, S_unit):
    S_percent = convert_slope_to_percent(S_val, S_unit)

    if S_percent < 9:
        return 0.065 + 0.045 * S_percent + 0.0065 * (S_percent ** 2)
    else:
        if S_unit == "%":
            theta = convert_slope_to_degrees(S_val)
        else:
            theta = S_val

        theta_rad = math.radians(theta)
        return 16.8 * math.sin(theta_rad) - 0.50

# ====== BUTTON ======
if st.button("🚀 Hitung LS"):
    S_percent = convert_slope_to_percent(S_val, S_unit)

    m = calculate_m(S_percent)
    L = calculate_L(lambda_val, m)
    S_factor = calculate_S_factor(S_val, S_unit)
    LS = L * S_factor

    # ====== OUTPUT ======
    st.markdown(f"""
    <div class="result-box">
        <h3>📈 Hasil Perhitungan</h3>
        <p>Nilai m = <b>{m:.3f}</b></p>
        <p>Faktor L = <b>{L:.4f}</b></p>
        <p>Faktor S = <b>{S_factor:.4f}</b></p>
        <hr>
        <h2>LS = {LS:.4f}</h2>
    </div>
    """, unsafe_allow_html=True)
