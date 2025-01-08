from css import simple_css
from load_model_llm import model_loader
from api_call.stability_image_ultra import generate_image
from text_processing import loader_text, template_prompt
from inmemory_vectordb import fais
import streamlit as st
import requests
import base64
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
import random
from langchain.memory import ConversationBufferMemory

def main(chat, embeddings):
    simple_css.add_custom_css()
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None
    if "content" not in st.session_state:
        st.session_state.content = []
        st.session_state.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None
    if "url_input" not in st.session_state:
        st.session_state.url_input = None

    initial_document_path = "sample_data/20241220 Peraturan-Perusahaan.pdf"
    list_docs_path = [initial_document_path]

    if st.session_state.vector_store is None:
        st.write("Initializing vector store with initial document...")
        initial_documents = loader_text.load_documents_from_pdf(initial_document_path)
        st.session_state.vector_store = fais.create_vector_store(initial_documents, embeddings)
    st.markdown('<h1 class="main-title">Employee Virtual Assistant</h1>', unsafe_allow_html=True)
    st.sidebar.markdown('<h3 class="sidebar-title">Chatbot Navigation</h3>', unsafe_allow_html=True)
    st.sidebar.header("Contributors: :blue[Steven Gianmarg Haposan Siahaan]")
    st.write('<p class="description">Hai, call me Siri, your lovely virtual assistant...</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Insert a temporary knowledge from a PDF", type="pdf")
    url_input = st.text_input("Insert a temporary knowledge from a URL")
    if uploaded_file:
        st.session_state.uploaded_file = uploaded_file
        list_docs_path.append(st.session_state.uploaded_file.name)
        st.write("Document/Text Preview:")
        file_data = uploaded_file.read()
        base64_pdf = base64.b64encode(file_data).decode('utf-8')

        pdf_display = f"""
            <iframe src="data:application/pdf;base64,{base64_pdf}" 
                    width="100%" height="600px" type="application/pdf">
            </iframe>
        """
        st.markdown(pdf_display, unsafe_allow_html=True)
    if url_input:
        st.session_state.url_input = url_input
        list_docs_path.append(st.session_state.url_input)
        try:
            response = requests.head(url_input, allow_redirects=True)
            if response.status_code == 200:
                st.write(f"Loading content from URL: {url_input}")
                web_display = f"""
                    <iframe src="{url_input}" 
                            width="100%" height="600px" style="border:none;">
                    </iframe>
                """
                st.markdown(web_display, unsafe_allow_html=True)
            else:
                st.error("The provided URL cannot be accessed. Please check the URL.")
        except requests.exceptions.RequestException as e:
            st.error(f"Error accessing the URL: {e}")


    new_documents = []
    if st.session_state.uploaded_file:
        temp_file = generate_image.handle_add_temp_knowledge_pdf(st.session_state.uploaded_file)
        new_documents = loader_text.load_documents_from_pdf(temp_file)
    elif st.session_state.url_input:
        new_documents = loader_text.load_documents_from_url(st.session_state.url_input)

    if(new_documents):
        st.session_state.vector_store = fais.update_vector_store(
            st.session_state.vector_store, new_documents
        )
        st.write("Vector store updated with new documents.")
    if len(list_docs_path) > 0:
        for path in list_docs_path:
            st.sidebar.write(f"- {path}")
    for msg in st.session_state.content:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])            
    if prompt := st.chat_input("Bruh just ask me and let me cook! <3"):
        st.session_state.content.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        retriever = st.session_state.vector_store.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.5})
        if len(prompt.split()) > 2:
            context_docs = retriever.get_relevant_documents(prompt)
            context = " ".join([doc.page_content for doc in context_docs])
        else:
            context = ""
        final_prompt = template_prompt.create_prompt_template(context, loader_text.expand_query_in_indonesian(prompt))
        greetings = [
            "Hai! Aku Siri, apa kabar? 😊",
            "Halo! Apa yang bisa aku bantu hari ini? 😎",
            "Hello! Aku siap membantu. Yuk, ada pertanyaan apa? 🤔"
        ]
        if prompt.lower() in ["hello", "hai", "halo","hi","hi siri","hello siri","hallo siri"]:
            response = random.choice(greetings)
        else:
            response = chat.send_message(final_prompt).text
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.content.append({"role": "assistant", "content": response})

embedding_model=st.selectbox("Choose your embedding model :", ["all-mpnet-base-v2","all-distilroberta-v1","all-MiniLM-L12-v2","all-MiniLM-L6-v2"])
chat, embeddings = model_loader.load_llm_and_embeddings(f"sentence-transformers/{embedding_model}")
if __name__ == "__main__":
    main(chat, embeddings)
