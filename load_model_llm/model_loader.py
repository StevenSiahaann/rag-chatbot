from langchain_community.embeddings import HuggingFaceEmbeddings
import google.generativeai as genai

import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv() 
GOOGLE_API_KEY = st.secrets["secrets"]["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

@st.cache_resource
def load_llm_and_embeddings(embedding_model_name="sentence-transformers/all-MiniLM-L6-v2"):

    model = genai.GenerativeModel("gemini-1.5-pro",system_instruction='''Kamu adalah chatbot yang sangat bersahabat yang akan membantu karyawan menjawab kebingungannya terkait peraturan suatu perusahaan. 
                                Nama kamu adalah siri, untuk sekarang kamu hanya memiliki pengetahuan terkait peraturan perusahaan, tetapi karyawan mungkin saja menambahkan dokumen tambahan baik itu dalam bentuk file maupun link.
                                Berikan jawaban yang bersahabat dengan nuansa bahasa yang santai serta jangan lupa tunjukkan emoji di dalam respon kamu untuk menunjukkan rasa sayang, marah, kesal, ataupun humoris kepada karyawan.
                                Jangan lupa untuk memperkenalkan namamu kepada karyawan. Hal paling utama adalah kamu harus menjadi teman yang baik untuk karyawan.
                                Jika kamu tidak mengetahui jawabannya, lebih baik kamu melemparkan pertanyaan kembali serta memastikan kembali kepada karyawan, jika kamu tetap tidak mengetahui setelah memastikan kepada karyawan lebih baik kamu menolak untuk menjawab.''')

    chat = model.start_chat(
        history=[
            {"role": "user", "parts": "Hello"},
            {"role": "model", "parts": '''Hai, Aku siri, Your virtual assistant. 
            Aku akan membantu kamu menjawab pertanyaan terkait peraturan perusahaan, jangan ragu untuk bertanya bro!.'''},
        ]
    )
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
    return chat, embeddings