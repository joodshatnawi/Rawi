import streamlit as st
import folium
from streamlit_folium import st_folium
from data.info_labels import info_labels


# ---------------- Result Page ----------------
def result_page():

    data = st.session_state.get("result")

    if data is None:
        st.error("No result found")
        st.stop()

    # ---------------- 3D CSS Styling & Layout Polish ----------------
    st.markdown("""
        <style>
        .stApp {
            background-color: #f4f2ef;
        }

        /* كروت Neumorphism ناعمة */
        .result-card {
            background: #f4f2ef;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 6px 6px 14px #d2cfc9, -6px -6px 14px #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.6);
        }

        /* تنسيق بطاقة القصة الورقية بألوان راوي */
        .story-box {
            background: #faf6f0;
            color: #2b231f;
            padding: 20px 24px;
            border-radius: 14px;
            border-left: 5px solid #8e3218;
            box-shadow: inset 2px 2px 5px #d2cfc9, inset -2px -2px 5px #ffffff;
            line-height: 1.8;
            font-size: 15.5px;
            max-height: 380px;
            overflow-y: auto;
        }

        /* الأزرار بتقنية 3D */
        .stButton > button {
            background: linear-gradient(145deg, #c45b38, #8e3218) !important;
            color: white !important;
            font-weight: 600 !important;
            border-radius: 12px !important;
            border: none !important;
            padding: 10px 22px !important;
            box-shadow: 4px 4px 10px #d2cfc9, -2px -2px 8px #ffffff !important;
            transition: all 0.2s ease-in-out !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 6px 6px 14px #c2bcba, -4px -4px 10px #ffffff !important;
            background: linear-gradient(145deg, #d3643f, #9b371b) !important;
        }

        /* كروت المعلومات والمقاييس */
        div[data-testid="stMetric"] {
            background: #f4f2ef;
            padding: 14px 16px;
            border-radius: 14px;
            box-shadow: 4px 4px 10px #d2cfc9, -4px -4px 10px #ffffff;
            margin-bottom: 12px;
        }

        h1, h2, h3 {
            color: #2b231f !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin-top: 10px !important;
            margin-bottom: 10px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # ---------------- Page Header ----------------
    st.title("🧭 Your AI Tour")

    header1, header2 = st.columns([3, 1])

    with header1:
        st.subheader(f"📍 {data['landmark']}")

    with header2:
        st.metric("Confidence", f"{float(data['confidence']) * 100:.1f}%")

    st.markdown("---")

    # ---------------- Main Layout (Image + Story) ----------------
    left, right = st.columns([1.1, 1], gap="medium")

    # ---------------- Landmark Image ----------------
    with left:
        st.image(data["image"], width='stretch')

    # ---------------- Story & Audio ----------------
    with right:
        st.subheader("📖 Story")

        st.markdown(f"""
        <div class="story-box">
            {data["story"]}
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        st.subheader("🔊 Audio Tour")
        st.audio(data["audio"])

    st.write("")

    # ---------------- Map Section ----------------
    st.subheader("🗺️ Location Map")

    m = folium.Map(
        location=[data["lat"], data["lon"]],
        zoom_start=13
    )

    folium.Marker(
        [data["lat"], data["lon"]],
        popup=data["landmark"],
        tooltip=data["landmark"],
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

    st_folium(m, width="100%", height=320)

    st.write("")

    # ---------------- Landmark Information ----------------
    st.subheader("📋 Key Information")

    info = data["info"]
    selected_language = data["language"]
    labels = info_labels[selected_language]
    unesco = labels[info["unesco"]]

    # توزيع التخزين على 3 أعمدة بدلاً من 2 لتحسين المظهر على الشاشات الواسعة
    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(labels["built"], info.get("built", "Not available"))
        st.metric(labels["governorate"], info["governorate"])

    with c2:
        st.metric(labels["unesco"], unesco)
        st.metric(labels["visit_time"], info.get("visit_time", "Not available"))

    with c3:
        st.metric(labels["best_time"], info.get("best_time", "Not available"))

    st.write("")

    # ---------------- Fun Fact & Actions Sections ----------------
    col_fact, col_chat = st.columns(2, gap="large")

    with col_fact:
        st.subheader("🎲 Fun Fact")
        if st.button("🎲 Show Fun Fact"):
            st.info(data["fun_fact"])

    with col_chat:
        st.subheader("💬 Ask Rawi AI")
        st.write("Have questions about this landmark?")
        if st.button("💬 Start Chatting"):
            st.session_state.page = "chat"
            st.rerun()

    # ---------------- Back Button ----------------
    st.write("")
    st.markdown("---")
    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()