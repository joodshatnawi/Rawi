# ---------------- Import Libraries ----------------
import streamlit as st
from model_rawi import RAWI
from home_page import page_home
from result_page import result_page
from chat_page import chat_page


# ---------------- Page Configuration ----------------
st.set_page_config(
    page_title="Rawi",
    page_icon="🏛️",
    layout="wide"
)


# ---------------- Global Styles & Sidebar 3D Styling ----------------
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #e3ded8 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.4);
    }

    [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] h3 {
        color: #8e3218 !important;
        font-weight: 700;
        margin-bottom: 15px;
    }

    .landmark-card {
        background: #e3ded8;
        border-radius: 12px;
        padding: 8px 14px;
        margin-bottom: 8px;
        box-shadow: 3px 3px 6px #c4bfb9, -3px -3px 6px #ffffff;
        color: #2b231f;
        font-weight: 600;
        font-size: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: all 0.2s ease-in-out;
    }

    .landmark-card:hover {
        transform: translateX(4px);
        background: #ede8e2;
        box-shadow: 4px 4px 8px #c4bfb9, -4px -4px 10px #ffffff;
    }

    /* Keep the original landmark card appearance */
    [data-testid="stSidebar"] .stButton > button {
    background: #e3ded8 !important;
    border-radius: 12px !important;
    padding: 0px 14px !important;
    min-height: 0px !important;
    height: 38px !important;
    margin-bottom: 8px !important;
    box-shadow: 3px 3px 6px #c4bfb9,
                -3px -3px 6px #ffffff !important;
    color: #2b231f !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    border: none !important;
    text-align: left !important;
    justify-content: flex-start !important;
}
    [data-testid="stSidebar"] .stButton > button:hover {
        transform: translateX(4px);
        background: #ede8e2 !important;
        box-shadow: 4px 4px 8px #c4bfb9,
                    -4px -4px 8px #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)


# ---------------- Sidebar ----------------
with st.sidebar:
    st.markdown("### 🏛️ Recognized Landmarks")
    st.caption("المعالم المدعومة:")

    landmarks = {
        "Ajloun Castle": "Ajloun_Castle",
        "Al-Maghtas": "Al_Maghtas",
        "Dead Sea": "Dead_Sea",
        "Jerash": "Jerash",
        "Karak Castle": "Karak_Castle",
        "Petra": "Petra",
        "Qasr Amra": "Qasr_Amra",
        "Umm Al-Jimal": "Um_AL_Jimal",
        "Umm Qais": "Um_Qais",
        "Wadi Mujib": "Wadi_Mujib",
        "Wadi Rum": "wadi_Rum"
    }

    for name, landmark_key in landmarks.items():
        if st.button(
            name,
            key=f"landmark_{landmark_key}",
            use_container_width=True
        ):
            st.session_state.selected_landmark = landmark_key
            st.session_state.image_source = "Choose from Sidebar"
            st.session_state.page = "home"
            st.rerun()



# ---------------- Initialize Rawi ----------------
@st.cache_resource
def load_rawi():
    return RAWI()

rawi = load_rawi()

# ---------------- Initialize Session State ----------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "result" not in st.session_state:
    st.session_state.result = None


# ---------------- Page Navigation ----------------
if st.session_state.page == "home":
    page_home(rawi)

elif st.session_state.page == "result":
    result_page()

elif st.session_state.page == "chat":
    chat_page(rawi)