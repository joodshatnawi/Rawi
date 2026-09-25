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
    /* خلفية القائمة الجانبية وتنسيقها */
    [data-testid="stSidebar"] {
        background-color: #e3ded8 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.4);
    }
    
    [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] h3 {
        color: #8e3218 !important;
        font-weight: 700;
        margin-bottom: 15px;
    }

    /* كروت ناعمة بتأثير 3D للمعالم */
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
        box-shadow: 4px 4px 8px #c4bfb9, -4px -4px 8px #ffffff;
    }
    </style>
""", unsafe_allow_html=True)


# ---------------- Sidebar ----------------
with st.sidebar:
    st.markdown("### 🏛️ Recognized Landmarks")
    st.caption("المعالم المدعومة:")
    
    landmarks = [
        "Ajloun Castle",
        "Al-Maghtas",
        "Dead Sea",
        "Jerash",
        "Karak Castle",
        "Petra",
        "Qasr Amra",
        "Umm Al-Jimal",
        "Umm Qais",
        "Wadi Mujib",
        "Wadi Rum"
    ]
    
    for name in landmarks:
        st.markdown(
            f"""
            <div class="landmark-card">
                <span>{name}</span>
            </div>
            """, 
            unsafe_allow_html=True
        )

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