import base64
import tempfile
import streamlit as st
from PIL import Image


def get_image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# ---------------- Home Page ----------------

def page_home(rawi):

    # ---------------- 3D CSS Styling ----------------
    st.markdown("""
        <style>
        /* خلفية التطبيق */
        .stApp {
            background-color: #f4f2ef;
        }

        /* أزرار 3D ملونة بألوان الشعار */
        .stButton > button {
            background: linear-gradient(145deg, #c45b38, #8e3218) !important;
            color: white !important;
            font-weight: 600 !important;
            border-radius: 12px !important;
            border: none !important;
            padding: 12px 24px !important;
            box-shadow: 4px 4px 10px #d2cfc9, 
                       -2px -2px 8px #ffffff !important;
            transition: all 0.2s ease-in-out !important;
            width: 100%;
        }

        /* تفاعل الأزرار عند التحويم والضغط */
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 6px 6px 14px #c2bcba, 
                       -4px -4px 10px #ffffff !important;
            background: linear-gradient(145deg, #d3643f, #9b371b) !important;
        }
        
        .stButton > button:active {
            transform: translateY(1px);
            box-shadow: inset 2px 2px 5px #5e2110, 
                        inset -2px -2px 5px #c45b38 !important;
        }

        /* تأثير Soft 3D غاطس لخيارات الراديو والقوائم المنسدلة */
        div[data-baseweb="select"] > div, div[role="radiogroup"] {
            background: #f4f2ef !important;
            border-radius: 12px !important;
            box-shadow: inset 3px 3px 6px #d2cfc9, inset -3px -3px 6px #ffffff !important;
            border: none !important;
            padding: 6px !important;
        }

        /* تحسين نصوص العناوين */
        h1, h2, h3 {
            color: #2b231f !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        </style>
    """, unsafe_allow_html=True)

    # ---------------- Logo & Title ----------------
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        logo_base64 = get_image_base64("rawi_logo.svg.png")
        
        st.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="data:image/png;base64,{logo_base64}" width="210" style="display: block; margin: 0 auto 2px auto; filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.15));">
                <h2 style="margin: 0; font-weight: 600; color: #8e3218;">
                    Your AI Guide to Jordan
                </h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    # ---------------- Image Source Selection ----------------
    st.markdown("### Discover a Landmark")

    image_source = st.radio(
        "Choose how you want to provide the image:",
        ["Upload Image", "Take a Photo"],
        horizontal=True
    )

    # ---------------- Upload / Camera ----------------
    upload_data = None

    if image_source == "Upload Image":
        upload_data = st.file_uploader(
            "Choose an image:",
            type=["jpg", "jpeg", "png", "webp"]
        )
    else:
        upload_data = st.camera_input(
            "Take a photo of the landmark"
        )

    # ---------------- If Image Exists ----------------
    if upload_data is not None:

        st.divider()

        # ---------------- Preview ----------------
        img = Image.open(upload_data)
        st.image(
            img,
            caption="Your Landmark",
            width="stretch"
        )

        st.write("") # مسافة بسيطة أنيقة

        # ---------------- Preferences Section Header ----------------
        st.markdown(
            """
            <div style="margin-top: 10px; margin-bottom: 12px;">
                <h4 style="margin: 0; color: #8e3218; font-weight: 600;">
                    Customize Your Tour
                </h4>
                <p style="margin: 0; font-size: 0.88rem; color: #666;">
                    Select your preferred language and story length
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ---------------- Preferences Inputs ----------------
        col_lang, col_len = st.columns(2)

        with col_lang:
            selected_language = st.selectbox(
                "Choose Language",
                ["العربية", "English", "Français"]
            )

        with col_len:
            story_length = st.selectbox(
                "Story Length",
                ["Short", "Medium", "Long"]
            )

        st.divider()

        # ---------------- Start Tour ----------------
        if st.button("Start My Tour"):

            with st.spinner("Rawi is identifying the landmark..."):

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".jpg"
                ) as tmp_file:

                    tmp_file.write(
                        upload_data.getbuffer()
                    )

                    image_path = tmp_file.name

                # ---------------- Analyze ----------------
                (
                    image,
                    story,
                    audio,
                    confidence,
                    landmark_name,
                    lat,
                    lon,
                    info,
                    detected_class,
                    fun_fact
                ) = rawi.analyze(
                    image_path,
                    selected_language,
                    story_length
                )

            # ---------------- Detection Successful ----------------
            if image is not None:

                st.session_state.result = {
                    "image": image,
                    "story": story,
                    "audio": audio,
                    "landmark": landmark_name,
                    "class": detected_class,
                    "confidence": confidence,
                    "lat": lat,
                    "lon": lon,
                    "info": info,
                    "language": selected_language,
                    "length": story_length,
                    "fun_fact": fun_fact,
                }

                st.session_state.page = "result"
                st.rerun()

            # ---------------- Detection Failed ----------------
            else:

                error_messages = {
                    "العربية": "لم يتم التعرف على المعلم. حاول رفع صورة أوضح.",
                    "English": "The landmark could not be recognized. Please upload a clearer image.",
                    "Français": "Le monument n’a pas pu être reconnu. Veuillez télécharger une image plus claire."
                }

                st.error(
                    error_messages.get(
                        selected_language,
                        "The landmark could not be recognized."
                    )
                )