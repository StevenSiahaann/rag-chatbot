import streamlit as st
from text_processing import loader_text
from langchain_community.vectorstores import FAISS

@st.cache_data
def create_vector_store(_documents, _embeddings, split_by="heading", source_name="unknown"):
    """
    Create a new vector store from a list of documents.

    Args:
        documents (list): List of Document objects.
        embeddings: Embedding function to convert text to vectors.
        split_by (str): Splitting method ('heading' or 'sentence').
        source_name (str): Name or identifier of the source document.

    Returns:
        FAISS: Vector store containing document embeddings.
    """
    split_docs = loader_text.split_documents(_documents, split_by=split_by, source_name=source_name)
    return FAISS.from_documents(split_docs, _embeddings)


@st.cache_data
def update_vector_store(_vector_store, _new_documents, split_by="sentence", source_name="unknown"):
    """
    Update an existing vector store with new documents.

    Args:
        vector_store (FAISS): Existing vector store to update.
        new_documents (list): List of new Document objects to add.
        embeddings: Embedding function to convert text to vectors.
        split_by (str): Splitting method ('heading' or 'sentence').
        source_name (str): Name or identifier of the source document.

    Returns:
        FAISS: Updated vector store.
    """
    split_docs = loader_text.split_documents(_new_documents, split_by=split_by, source_name=source_name)
    valid_split_docs = [doc for doc in split_docs if hasattr(doc, 'page_content') and doc.page_content]
    if not valid_split_docs:
        raise ValueError("No valid documents to add to the vector store.")
    _vector_store.add_documents(split_docs)
    return _vector_store
