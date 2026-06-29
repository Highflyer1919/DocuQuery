import os
import re
import tempfile
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from rank_bm25 import BM25Okapi

load_dotenv()

# Handle Streamlit Cloud secrets
import streamlit as st
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]


def tokenize(text):
    return re.findall(r'\w+', text.lower())


def process_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    loader = PyPDFLoader(tmp_path)
    documents = loader.load()
    page_count = len(documents)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = splitter.split_documents(documents)
    os.unlink(tmp_path)

    tokenized_chunks = [tokenize(chunk.page_content) for chunk in chunks]
    bm25 = BM25Okapi(tokenized_chunks)

    return {"chunks": chunks, "bm25": bm25}, page_count


def get_answer(store, question):
    chunks = store["chunks"]
    bm25 = store["bm25"]

    tokenized_query = tokenize(question)
    scores = bm25.get_scores(tokenized_query)
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:4]
    top_docs = [chunks[i] for i in top_indices]

    context = "\n\n".join([doc.page_content for doc in top_docs])

    llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0.3)

    prompt = f"""You are a helpful assistant that answers questions based strictly 
on the document provided. Use ONLY the context below.
If the answer is not found in the context, say:
"I couldn't find the answer in the uploaded document."
Keep your answer clear and concise.

Context:
{context}

Question: {question}

Answer:"""

    response = llm.invoke([HumanMessage(content=prompt)])

    pages = sorted(set(
        doc.metadata.get("page", 0) + 1
        for doc in top_docs
    ))

    return response.content, pages