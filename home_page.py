import tempfile
import streamlit as st
from PIL import Image


# ---------------- Home Page ----------------

def page_home(rawi):

    # ---------------- Title ----------------
    st.title("Rawi — Your AI Guide to Jordan")
    st.divider()


    # ---------------- Upload Image ----------------
    st.markdown("### Discover a Landmark")

    upload_data = st.file_uploader(
        "Choose an image:",
        type=["jpg", "jpeg", "png", "webp"]
    )

    # ---------------- If Image Exists ----------------
    if upload_data is not None:

        st.divider()

        # ---------------- Preview ----------------
        img = Image.open(upload_data)

        st.image(
            img,
            caption="Your Landmark",
            use_container_width=True
        )


        # ---------------- Select Language ----------------
        selected_language = st.selectbox(
            "Choose Language",
            ["العربية", "English", "Français"]
        )

        # ---------------- Story Length ----------------
        story_length = st.selectbox(
            " Story Length",
            ["Short", "Medium", "Long"]
        )

        st.divider()

        # ---------------- Start Tour ----------------
        if st.button(" Start My  Tour"):

            with st.spinner("Rawi is identifying the landmark..."):

                # Save image as temporary JPG
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
                    #fun_fact
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
                    #"fun_fact": fun_fact,
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