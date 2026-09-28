import streamlit as st
from chat_labels import chat_labels


# ---------------- Chat Page ----------------
def chat_page(rawi):

    # ---------------- Get Result ----------------
    data = st.session_state["result"]

    # ---------------- Initialize Chat History ----------------
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    language = data["language"]
    labels = chat_labels[language]

    # ---------------- 3D CSS & RTL Styling ----------------
    st.markdown("""
        <style>
        .stApp {
            background-color: #f4f2ef;
        }

        /* ---------------- Chat Messages ---------------- */
        .stChatMessage {
            background-color: #f4f2ef !important;
            border-radius: 16px !important;
            box-shadow:
                4px 4px 10px #d2cfc9,
                -4px -4px 10px #ffffff !important;
            padding: 12px 18px !important;
            margin-bottom: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.5) !important;
        }

        /* ---------------- Chat Form ---------------- */
        div[data-testid="stForm"] {
            border: none !important;
            padding: 0 !important;
            background: transparent !important;
        }

        /* ---------------- Text Input ---------------- */
        div[data-testid="stTextInput"] input {
            background-color: #f4f2ef !important;
            border: none !important;
            border-radius: 15px !important;

            box-shadow:
                inset 2px 2px 5px #d2cfc9,
                inset -2px -2px 5px #ffffff !important;

            color: #2b231f !important;
            padding: 0.75rem 1rem !important;
            font-size: 16px !important;
            height: 48px !important;
        }

        div[data-testid="stTextInput"] input:focus {
            border: 1px solid #c45b38 !important;

            box-shadow:
                inset 2px 2px 5px #d2cfc9,
                inset -2px -2px 5px #ffffff,
                0 0 0 1px rgba(196, 91, 56, 0.15) !important;
        }

        div[data-testid="stTextInput"] input::placeholder {
            color: #77716c !important;
            opacity: 1 !important;
        }

        /* ---------------- Send Button ---------------- */
        div[data-testid="stFormSubmitButton"] button {
            height: 48px !important;
            width: 48px !important;
            min-width: 48px !important;

            border-radius: 50% !important;
            border: none !important;

            background: linear-gradient(
                145deg,
                #c45b38,
                #8e3218
            ) !important;

            color: white !important;
            font-size: 22px !important;
            font-weight: 700 !important;

            padding: 0 !important;

            box-shadow:
                4px 4px 8px #d2cfc9,
                -2px -2px 6px #ffffff !important;

            transition: all 0.2s ease-in-out !important;
        }

        div[data-testid="stFormSubmitButton"] button:hover {
            transform: translateY(-2px) !important;

            box-shadow:
                5px 5px 10px #c2bcba,
                -3px -3px 8px #ffffff !important;
        }

        div[data-testid="stFormSubmitButton"] button:active {
            transform: translateY(1px) !important;

            box-shadow:
                inset 2px 2px 5px rgba(80, 30, 15, 0.25) !important;
        }

        /* ---------------- Navigation Buttons ---------------- */
        .stButton > button {
            background: linear-gradient(
                145deg,
                #c45b38,
                #8e3218
            ) !important;

            color: white !important;
            font-weight: 600 !important;
            border-radius: 12px !important;
            border: none !important;
            padding: 10px 20px !important;

            box-shadow:
                4px 4px 10px #d2cfc9,
                -2px -2px 8px #ffffff !important;

            transition: all 0.2s ease-in-out !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px);

            box-shadow:
                6px 6px 14px #c2bcba,
                -4px -4px 10px #ffffff !important;

            background: linear-gradient(
                145deg,
                #d3643f,
                #9b371b
            ) !important;
        }

        /* ---------------- Headings ---------------- */
        h1, h2, h3 {
            color: #2b231f !important;
            font-family:
                'Segoe UI',
                Tahoma,
                Geneva,
                Verdana,
                sans-serif;
        }
        </style>
    """, unsafe_allow_html=True)

    # ---------------- RTL Support ----------------
    if language == "العربية":
        st.markdown("""
        <style>
        .stChatMessage {
            direction: rtl;
            text-align: right;
        }

        .stChatMessage p {
            direction: rtl;
            text-align: right;
        }

        div[data-testid="stTextInput"] input {
            direction: rtl !important;
            text-align: right !important;
        }
        </style>
        """, unsafe_allow_html=True)

    # ---------------- Initialize Messages ----------------
    if st.session_state.get("reset_chat", True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    f"👋 {labels['welcome']}\n\n"
                    f"{labels['ask']} **{data['landmark']}**."
                )
            }
        ]
        st.session_state.reset_chat = False

    # ---------------- Header ----------------
    st.title("💬 Rawi AI")
    st.subheader(f"📍 {data['landmark']}")

    st.write("")

    # ---------------- Display Messages ----------------
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    st.write("")

    # ---------------- User Question ----------------
    typed_question = None

    with st.form("chat_form", clear_on_submit=True):

        input_col, send_col = st.columns([8, 1])

        with input_col:
            question_input = st.text_input(
                "Message",
                placeholder=labels["placeholder"],
                label_visibility="collapsed"
            )

        with send_col:
            send = st.form_submit_button(
                "↑",
                width="stretch"
            )

        if send and question_input.strip():
            typed_question = question_input.strip()

    # ---------------- Generate Answer ----------------
    if typed_question:
        question = typed_question

        # Save user message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        # Generate Answer
        with st.spinner("🤖 Rawi AI is thinking..."):

            answer = rawi.generate_answer(
                data["class"],
                data["language"],
                question,
                st.session_state.chat_history
            )

        # Save Assistant Message
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        # Update Conversation History
        st.session_state.chat_history.append(
            {
                "question": question,
                "answer": answer
            }
        )

        st.rerun()

    # ---------------- Navigation Buttons ----------------
    st.write("")

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button(
            labels["back"],
            width="stretch"
        ):
            st.session_state.page = "result"
            st.session_state.reset_chat = True
            st.session_state.chat_history = []
            st.rerun()

    with col2:
        if st.button(
            "Home",
            width="stretch"
        ):
            st.session_state.page = "home"
            st.session_state.reset_chat = True
            st.session_state.chat_history = []
            st.rerun()