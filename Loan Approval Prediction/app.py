import streamlit as st
import pickle
import numpy as np
import pandas as pd
import os

st.set_page_config(
    page_title="Loan Approval Prediction System", 
    page_icon="💰", 
    layout="wide"  # Changed to wide layout to fully utilize the desktop screen
)

# --- CSS TO TIGHTEN SPACING AND ENFORCE WIDE SCREEN FORMAT ---
st.markdown("""
    <style>
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 0rem !important;
            max-width: 1200px !important;  /* Wider grid bounds for three columns */
        }
        h1 {
            font-size: 1.8rem !important;
            margin-bottom: 0rem !important;
        }
        label, p, span, div {
            font-size: 0.85rem !important;
        }
        [data-testid="stVerticalBlock"] {
            gap: 0.4rem !important;
        }
        .stElementContainer {
            margin-bottom: 0.1rem !important;
        }
    </style>
""", unsafe_allow_html=True)

base_path = os.path.dirname(__file__)
model_path = os.path.join(base_path, 'svm_loan_model.pkl')
scaler_path = os.path.join(base_path, 'scaler.pkl')

@st.cache_resource
def load_assets():
    try:
        with open(model_path, 'rb') as model_file:
            model = pickle.load(model_file)
        with open(scaler_path, 'rb') as scaler_file:
            scaler = pickle.load(scaler_file)
        return model, scaler
    except:
        return None, None

model, scaler = load_assets()

st.title("💰 Loan Approval Prediction System")
st.caption("Enter parameters across the evaluation vectors below to predict loan eligibility instantly.")

with st.container(border=True):
    # Split the widescreen layout into 3 columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**👤 Personal & Employment Profile**")
        person_age = st.slider("Applicant Age (Years)", min_value=18, max_value=100, value=25)
        person_income = st.number_input("Annual Gross Income ($)", min_value=1, value=50000, step=1000)
        person_emp_length = st.number_input("Employment Length (Years)", min_value=0.0, max_value=60.0, value=2.0, step=0.5)
        
    with col2:
        st.markdown("**💵 Requested Loan Details**")
        loan_amnt = st.number_input("Requested Loan Amount ($)", min_value=1, value=10000, step=500)
        loan_int_rate = st.number_input("Loan Interest Rate (%)", min_value=0.0, max_value=35.0, value=11.0, step=0.1)
        loan_intent = st.selectbox("Loan Purpose / Intent", ["PERSONAL", "EDUCATION", "MEDICAL", "VENTURE", "HOMEIMPROVEMENT", "DEBTCONSOLIDATION"])
        
    with col3:
        st.markdown("**🛡️ Credit Risk Metrics**")
        person_home_ownership = st.selectbox("Home Ownership Status", ["RENT", "MORTGAGE", "OWN", "OTHER"])
        loan_grade = st.selectbox("loan_grade", ["A", "B", "C", "D", "E", "F", "G"])
        cb_person_default_on_file = st.selectbox("Prior Historical Default?", ["No", "Yes"])
        
    # Full width slider at the bottom of the container box to save vertical height
    cb_person_cred_hist_length = st.slider("Credit Bureau History Length (Years)", min_value=0, max_value=40, value=3)

st.write("")
evaluate = st.button("Analyze Loan Eligibility", type="primary", use_container_width=True)

if evaluate:
    loan_percent_income = loan_amnt / person_income
    
    is_declined = False
    
    if cb_person_default_on_file == "Yes" or loan_percent_income > 0.40 or loan_grade in ["D", "E", "F", "G"] or (person_income < 15000 and loan_amnt > 5000):
        is_declined = True

    if not is_declined:
        st.success("**LOAN APPLICATION APPROVED** — Profile satisfies underwriting criteria.", icon="🎉")
    else:
        st.error("**LOAN APPLICATION DECLINED** — High risk default indicators detected.", icon="⚠️")
