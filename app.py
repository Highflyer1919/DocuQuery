import streamlit as st
from rag_pipeline import process_pdf, get_answer

st.set_page_config(
    page_title="DocuQuery",
    page_icon="📄",
    layout="centered"
)

st.title("📄 DocuQuery")
st.caption("Upload a PDF and ask questions — every answer includes page-level citations.")

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_doc" not in st.session_state:
    st.session_state.current_doc = None

with st.sidebar:
    st.header("📁 Document")
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

    if uploaded_file:
        if uploaded_file.name != st.session_state.current_doc:
            with st.spinner("Reading and indexing document..."):
                vector_store, page_count = process_pdf(uploaded_file)
                st.session_state.vector_store = vector_store
                st.session_state.current_doc = uploaded_file.name
                st.session_state.chat_history = []
            st.success(f"✅ Loaded: {uploaded_file.name}")
            st.caption(f"{page_count} pages indexed")

    if st.session_state.current_doc:
        st.divider()
        st.caption(f"Active: **{st.session_state.current_doc}**")
        if st.button("🗑️ Clear & upload new"):
            st.session_state.vector_store = None
            st.session_state.current_doc = None
            st.session_state.chat_history = []
            st.rerun()

if not st.session_state.vector_store:
    st.info("👈 Upload a PDF in the sidebar to get started.")
else:
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if msg.get("pages"):
                st.caption(f"📍 Source: Page(s) {', '.join(map(str, msg['pages']))}")

    question = st.chat_input("Ask anything about your document...")

    if question:
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching document..."):
                answer, pages = get_answer(st.session_state.vector_store, question)
            st.write(answer)
            if pages:
                st.caption(f"📍 Source: Page(s) {', '.join(map(str, pages))}")

        st.session_state.chat_history.append({"role": "user", "content": question})
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer,
            "pages": pages
        })