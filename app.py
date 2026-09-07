# ---------------- Import Libraries ----------------
import streamlit as st
from model_rawi import RAWI
from home_page import page_home
from result_page import result_page


# ---------------- Page Configuration ----------------
st.set_page_config(
    page_title="Rawi",
    page_icon="📜",
    layout="wide"
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