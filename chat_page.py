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
    st.title("💬 Rawi ")
    st.subheader(f"📍 {data['landmark']}")
    st.divider()

    # ---------------- Display Messages ----------------
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    st.divider()

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
    st.divider()

    if st.button(labels["back"]):
        st.session_state.page = "result"
        st.session_state.reset_chat = True
        st.session_state.chat_history = []
        st.rerun()   
