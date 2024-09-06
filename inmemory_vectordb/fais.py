import streamlit as st
from text_processing import loader_text
from langchain_community.vectorstores import FAISS

@st.cache_resource
def create_vector_store(_documents, _embeddings):
    _split_documents = loader_text.split_documents_by_sentence(_documents)
    return FAISS.from_documents(_split_documents, _embeddings)

@st.cache_resource
def update_vector_store(_documents, _embeddings):
    _split_documents = loader_text.split_documents_by_sentence(_documents)
    return FAISS.from_documents(_split_documents, _embeddings)
