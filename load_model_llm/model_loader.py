from langchain_community.embeddings import HuggingFaceEmbeddings
import google.generativeai as genai
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv() 
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY") or os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)

@st.cache_resource
def load_llm_and_embeddings(embedding_model_name="sentence-transformers/all-MiniLM-L6-v2"):
    model = genai.GenerativeModel("gemini-1.5-flash",system_instruction='''You are a friendly chatbot that will help answering customer questions. 
                                Your name is Siri. For now you just have a knowledge for a billing FAQ PG&E, but customer may add a knowledge based on an input document and a url. 
                                Give the customer the friendly answer by showing a emotions on your response. You can response using many emoji to showing a love, your feeling, or any other expressions.
                                Don't forget to introduce your name to customer. At the end, you must be a good friends for your customer.
                                If you dont know the answer, just ask the customer for adding the information that you may learn from pdf or urls.''')
    chat = model.start_chat(
        history=[
            {"role": "user", "parts": "Hello"},
            {"role": "model", "parts": '''Hai, I'm Siri, Your virtual assistant. 
            I will help you with answering your questions. Feel free for ask me bro! 
            Don't worry i'll try my best to give the best answer. 
            But for now i just have a knowledge about PG&E billing QNA, 
            just gimme the external url or insert the pdf i'll learn it for you.'''},
        ]
    )
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
    return chat, embeddings