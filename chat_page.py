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

        /* تحسين شكل الفقاعات الخاص بالدردشة */
        .stChatMessage {
            background-color: #f4f2ef !important;
            border-radius: 16px !important;
            box-shadow: 4px 4px 10px #d2cfc9, -4px -4px 10px #ffffff !important;
            padding: 12px 18px !important;
            margin-bottom: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.5) !important;
        }

        /* تحسين صندوق الإدخال (Chat Input) */
        div[data-testid="stChatInput"] {
            border-radius: 15px !important;
            box-shadow: inset 2px 2px 5px #d2cfc9, inset -2px -2px 5px #ffffff !important;
        }

        /* الأزرار بتقنية 3D */
        .stButton > button {
            background: linear-gradient(145deg, #c45b38, #8e3218) !important;
            color: white !important;
            font-weight: 600 !important;
            border-radius: 12px !important;
            border: none !important;
            padding: 10px 20px !important;
            box-shadow: 4px 4px 10px #d2cfc9, -2px -2px 8px #ffffff !important;
            transition: all 0.2s ease-in-out !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 6px 6px 14px #c2bcba, -4px -4px 10px #ffffff !important;
            background: linear-gradient(145deg, #d3643f, #9b371b) !important;
        }

        h1, h2, h3 {
            color: #2b231f !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
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

        div[data-testid="stChatInput"] textarea {
            direction: rtl;
            text-align: right;
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
    
    st.write("") # مسافة أنيقة بدلاً من st.divider

    # ---------------- Display Messages ----------------
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    st.write("")

    # ---------------- User Question ----------------
    typed_question = st.chat_input(labels["placeholder"])

    if typed_question:
        question = typed_question

        # Save user message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        # ---------------- Generate Answer ----------------
        with st.spinner("🤖 Rawi AI is thinking..."):

            answer = rawi.generate_answer(
                data["class"],
                data["language"],
                question,
                st.session_state.chat_history
            )

        # ---------------- Save Assistant Message ----------------
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        # ---------------- Update Conversation History ----------------
        st.session_state.chat_history.append(
            {
                "question": question,
                "answer": answer
            }
        )

        st.rerun()

    # ---------------- Back Button ----------------
    st.write("")

    if st.button(labels["back"]):
        st.session_state.page = "result"
        st.session_state.reset_chat = True
        st.session_state.chat_history = []
        st.rerun()