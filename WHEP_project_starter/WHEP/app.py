import streamlit as st
from whep.retrieval import retrieve_context
from whep.generation import generate_answer
from whep.config import get_groq_api_key

st.set_page_config(
    page_title="WHEP | Women's Health Education Platform",
    page_icon="🌿",
    layout="centered",
)

st.title("WHEP")
st.caption("Women's Health Education Platform")
st.write(
    "A health education assistant that answers questions using information "
    "from its curated knowledge base."
)

st.info(
    "WHEP provides general health education, not medical diagnosis or "
    "personalized treatment. For personal medical concerns, consult a qualified "
    "health professional."
)

api_key = get_groq_api_key()
if not api_key:
    st.error(
        "Groq API key not found. Add GROQ_API_KEY to "
        ".streamlit/secrets.toml before running the app."
    )
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            with st.expander("Sources used"):
                for source in message["sources"]:
                    st.markdown(f"- [{source['title']}]({source['url']})")

question = st.chat_input("Ask WHEP a women's health question...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching WHEP's knowledge base..."):
            try:
                context, sources = retrieve_context(question)
                answer = generate_answer(question, context, api_key)
                st.markdown(answer)

                if sources:
                    with st.expander("Sources used"):
                        for source in sources:
                            st.markdown(f"- [{source['title']}]({source['url']})")
                else:
                    st.caption("No source links were returned for this answer.")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                })
            except Exception as exc:
                st.error(f"Something went wrong: {exc}")
                st.caption(
                    "Check that the ChromaDB folder is present and that your "
                    "Groq API key and package versions are configured correctly."
                )
