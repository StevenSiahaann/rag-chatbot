from langchain.schema import Document
import re

from langchain.document_loaders import PyPDFLoader, WebBaseLoader
from langchain.text_splitter import SpacyTextSplitter
from nltk.corpus import wordnet

def expand_query_in_indonesian(query, max_synonyms=3):
    """
    Perluas query menggunakan sinonim dari WordNet dalam bahasa Indonesia
    dengan batasan jumlah sinonim.

    Args:
        query (str): Query pengguna.
        max_synonyms (int): Jumlah maksimum sinonim per kata.

    Returns:
        str: Query yang diperluas dengan sinonim bahasa Indonesia.
    """
    words = query.split()
    expanded_query = []
    for word in words:
        synonyms = []
        for syn in wordnet.synsets(word):
            # Ambil sinonim dalam bahasa Indonesia
            synonyms.extend(syn.lemma_names(lang='ind'))
        # Hilangkan duplikasi dan batasi jumlah sinonim
        limited_synonyms = list(set(synonyms))[:max_synonyms]
        expanded_query.extend(limited_synonyms)
    return " ".join(set(expanded_query))

# def expand_query(query):
#     words = query.split()
#     expanded_query = []
#     for word in words:
#         synonyms = [syn.lemmas()[0].name() for syn in wordnet.synsets(word)]
#         expanded_query.extend(synonyms)
#     print("expanded_query",expanded_query)
#     return " ".join(set(expanded_query))
def load_documents_from_pdf(pdf_file):
    loader = PyPDFLoader(pdf_file)
    return loader.load()

def load_documents_from_url(url):
    loader = WebBaseLoader(url)
    return loader.load()
from langchain.schema import Document
import re

def split_documents_by_sentence(documents, source_name="unknown"):
    text_splitter = SpacyTextSplitter(chunk_size=1000, chunk_overlap=150)
    split_docs = []
    for i, doc in enumerate(documents):
        if hasattr(doc, 'page_content') and doc.page_content:
            chunks = text_splitter.split_text(doc.page_content)
            split_docs.extend([
                Document(
                    page_content=chunk,
                    metadata={
                        "source": source_name,
                        "chunk_index": f"sentence-{i}-{j}"
                    }
                ) for j, chunk in enumerate(chunks)
            ])
        else:
            print(f"Warning: Document {doc} has no page_content or is empty")
    return split_docs


def split_documents_by_heading(documents, source_name="unknown"):
    """
    Split documents based on headings (e.g., 'BAB XX\n{NAMA_BAB}' or 'Pasal X').

    Args:
        documents (list): List of Document objects with `page_content`.
        source_name (str): Name or identifier of the source document.

    Returns:
        List[Document]: List of split documents with metadata.
    """
    split_docs = []
    for i, doc in enumerate(documents):
        if hasattr(doc, 'page_content') and doc.page_content:
            chunks = []
            current_chunk = ""
            current_bab = None
            lines = doc.page_content.split("\n")
            
            for idx, line in enumerate(lines):
                if re.match(r"^BAB\s+[IVXLCDM]+\s*$", line.strip()):
                    if current_chunk:
                        chunks.append((current_bab, current_chunk.strip()))
                        current_chunk = ""
                    next_line = lines[idx + 1].strip() if idx + 1 < len(lines) else ""
                    current_bab = f"{line.strip()} {next_line.strip()}"
                elif re.match(r"^Pasal\s+\d+", line.strip()):  # Deteksi Pasal
                    if current_chunk:
                        chunks.append((current_bab, current_chunk.strip()))
                        current_chunk = ""
                    current_chunk += line + "\n"
                else:
                    current_chunk += line + "\n"
            
            if current_chunk:
                chunks.append((current_bab, current_chunk.strip()))
            
            split_docs.extend([
                Document(
                    page_content=chunk,
                    metadata={
                        "source": source_name,
                        "heading": heading,
                        "chunk_index": f"heading-{i}-{j}"
                    }
                ) for j, (heading, chunk) in enumerate(chunks)
            ])
        else:
            print(f"Warning: Document {doc} has no page_content or is empty")
    return split_docs


def split_documents(documents, split_by="sentence", source_name="unknown"):
    """
    Split documents with indexing metadata.

    Args:
        documents (list): List of Document objects with `page_content`.
        split_by (str): Splitting method ("heading" or "sentence").
        source_name (str): Name or identifier of the source document.

    Returns:
        List[Document]: List of split documents with metadata.
    """
    if split_by == "heading":
        return split_documents_by_heading(documents, source_name=source_name)
    elif split_by == "sentence":
        return split_documents_by_sentence(documents, source_name=source_name)
    else:
        raise ValueError("Invalid split_by value. Use 'heading' or 'sentence'.")