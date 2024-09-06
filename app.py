from css import simple_css
from load_model_llm import model_loader
from api_call.stability_image_ultra import generate_image
from text_processing import clean_translate, loader_text, template_prompt
from inmemory_vectordb import fais
import streamlit as st
from langchain.memory import ConversationBufferMemory
import spacy
import subprocess
import sys
def install_spacy_model():
    try:
        spacy.load("en_core_web_sm")
    except OSError:
        st.write("Downloading en_core_web_sm model...")
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        st.write("Model downloaded!")
def main(chat, embeddings):
    install_spacy_model()
    simple_css.add_custom_css()
    list_docs_path=['sample_data/pge_qna_document.pdf']
    documents = loader_text.load_documents_from_pdf('sample_data/pge_qna_document.pdf')
    
    vector_store = fais.create_vector_store(documents, embeddings)
    retriever = vector_store.as_retriever()

    st.markdown('<h1 class="main-title">Customer Virtual Assistant</h1>', unsafe_allow_html=True)
    st.sidebar.markdown('<h3 class="sidebar-title">Chatbot Navigation</h3>', unsafe_allow_html=True)
    st.sidebar.header("Contributors: :blue[Steven Gianmarg Haposan Siahaan]")
    st.write('<p class="description">Hai, call me Siri, your lovely virtual assistant...</p>', unsafe_allow_html=True)

    if "generate_type" not in st.session_state:
        st.session_state.generate_type = "Text"
    st.session_state.generate_type = st.selectbox("Explain me by:", ["Text", "Image"])
    if st.session_state.generate_type == "Image":
        st.write("## Image Generation Options")
        st.session_state.aspect_ratio = st.selectbox("Choose aspect ratio:", ["3:2", "16:9", "1:1", "4:5", "9:16"])
        st.session_state.seed = st.number_input("Seed (optional):", min_value=0, value=0)
        st.session_state.output_format = st.selectbox("Output format:", ["png", "jpeg", "webp"])

    uploaded_file = st.file_uploader("Insert a temporary knowledge from a PDF", type="pdf")
    url_input = st.text_input("Insert a temporary knowledge from a URL")
    new_documents=[]
    if uploaded_file:
        temp_file = generate_image.handle_add_temp_knowledge_pdf(uploaded_file)
        new_documents = loader_text.load_documents_from_pdf(temp_file)
        list_docs_path.append(temp_file)
    elif url_input:
        new_documents = loader_text.load_documents_from_url(url_input)
        list_docs_path.append(url_input)
    if(new_documents):
        document_text = " ".join([doc.page_content for doc in new_documents])
        st.write("Document/Text Preview:")
        st.write(document_text[:1498])
        vector_store = fais.update_vector_store(new_documents+documents, embeddings)
        retriever = vector_store.as_retriever()
    if len(list_docs_path) > 0:
        for path in list_docs_path:
            st.sidebar.write(f"- {path[12:]}")
    if "content" not in st.session_state:
        st.session_state.content = []
        st.session_state.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    for msg in st.session_state.content:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    if prompt := st.chat_input("Bruh just ask me and let me cook! <3"):
        st.session_state.content.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        context_docs = retriever.get_relevant_documents(prompt) if (new_documents+documents) else []
        context = " ".join([doc.page_content for doc in context_docs])
        final_prompt = template_prompt.create_prompt_template(context, prompt)
        response = chat.send_message(clean_translate.clean_and_translate_prompt(final_prompt)).text
        with st.chat_message("assistant"):
            st.markdown(response)
        if st.session_state.generate_type == "Image":
            st.write("## Generating Image...")
            image_prompt = f"Generate an infographic from this fact: {clean_translate.clean_and_translate_prompt(response)}. Avoid generating long text and typos."
            st.session_state.image_data, st.session_state.seed = generate_image.generate_image_from_stability(image_prompt, st.session_state.aspect_ratio, st.session_state.seed, st.session_state.output_format)
            if st.session_state.image_data:
                generate_image.handle_image_response(st.session_state.image_data, st.session_state.seed, st.session_state.output_format)
            else:
                st.error("Failed to generate an image.")
        st.session_state.content.append({"role": "assistant", "content": response})
embedding_model=st.selectbox("Choose your embedding model :", ["all-MiniLM-L6-v2","all-MiniLM-L12-v2","all-distilroberta-v1","all-mpnet-base-v2"])
chat, embeddings = model_loader.load_llm_and_embeddings(f"sentence-transformers/{embedding_model}")
if __name__ == "__main__":
    main(chat, embeddings)
