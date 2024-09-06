from langchain.schema import Document
from langchain.document_loaders import PyPDFLoader, WebBaseLoader
from langchain.text_splitter import SpacyTextSplitter
def load_documents_from_pdf(pdf_file):
    loader = PyPDFLoader(pdf_file)
    return loader.load()

def load_documents_from_url(url):
    loader = WebBaseLoader(url)
    return loader.load()

def split_documents_by_sentence(documents):
    text_splitter = SpacyTextSplitter(chunk_size=1000, chunk_overlap=150)
    return [Document(page_content=chunk) for doc in documents for chunk in text_splitter.split_text(doc.page_content)]
