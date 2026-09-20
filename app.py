# ---------------- Import Libraries ----------------
import streamlit as st
from model_rawi import RAWI
from home_page import page_home
from result_page import result_page
from chat_page import chat_page


# ---------------- Page Configuration ----------------
import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="Rawi",
    page_icon="🏛️",
    layout="wide"
)
# ---------------- Sidebar ----------------
with st.sidebar:

    st.image(
        "rawi_logo.svg.png",
        width="stretch"
    )
    st.divider()
    # ---------------- Supported Landmarks ----------------
    st.markdown("### Landmarks You Can Recognize")
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
    for landmark in landmarks:
        st.markdown(f"• **{landmark}**")


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