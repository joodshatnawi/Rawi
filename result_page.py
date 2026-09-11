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

    # ---------------- Page Header ----------------
    st.title("🧭 Your AI Tour")

    header1, header2 = st.columns([4, 1])

    with header1:
        st.subheader(f"📍 {data['landmark']}")

    with header2:
        st.metric("Confidence", f"{float(data['confidence']) * 100:.1f}%")

    st.divider()

    # ---------------- Main Layout ----------------
    left, right = st.columns([1.5, 1])

    # ---------------- Landmark Image ----------------
    with left:
        st.image(data["image"], width="stretch")

    # ---------------- Story & Audio ----------------
    with right:
        st.subheader("📖 Story")

        st.markdown(f"""
        <div style="
            background:#f5ecd7;
            color:#222;
            padding:20px;
            border-radius:15px;
            border:2px solid #b08d57;
            line-height:1.8;
            font-size:17px;
        ">
        {data["story"]}
        </div>
        """, unsafe_allow_html=True)

        st.subheader("🔊 Listen")
        st.audio(data["audio"])

    st.divider()

    # ---------------- Map ----------------
    st.subheader("🗺️ Location")

    m = folium.Map(
        location=[data["lat"], data["lon"]],
        zoom_start=12
    )

    folium.Marker(
        [data["lat"], data["lon"]],
        popup=data["landmark"],
        tooltip=data["landmark"],
        icon=folium.Icon(color="red")
    ).add_to(m)

    st_folium(m, width=900, height=350)

    st.divider()

    # ---------------- Landmark Information ----------------
    st.subheader("📋 Information")
 
    info = data["info"]
    selected_language = data["language"]
    labels = info_labels[selected_language]
    unesco = labels[info["unesco"]]

    c1, c2 = st.columns(2)

    with c1:
       st.metric(labels["built"], info["built"])
       st.metric(labels["unesco"], unesco)
       st.metric(labels["best_time"], info["best_time"])

    with c2:
        st.metric(labels["governorate"], info["governorate"])
        st.metric(labels["visit_time"], info["visit_time"])

    st.divider()
    

    st.subheader("🎲 Fun Fact")

    if st.button("🎲 Show Fun Fact"):
        st.success(data["fun_fact"])

    # ---------------- Ask Rawi AI ----------------
    st.markdown("### Have More Questions?")
    st.write("Ask Rawi AI anything about this landmark.")

    if st.button("💬 Ask Rawi AI", use_container_width=True):
        st.session_state.page = "chat"
        st.rerun()


    # ---------------- Back Button ----------------
    st.divider()
    if st.button(" Back to the Main Page"):
        st.session_state.page = "home"
        st.rerun()
