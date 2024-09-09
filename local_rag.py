import os
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever

def prepare_db():
    local_path = "data"

    pdf_files = [f for f in os.listdir(local_path) if f.endswith('.pdf')]
    documents = []

    for file in pdf_files:
        file_path = os.path.join(local_path, file)
        loader = PyPDFLoader(file_path)
        document = loader.load()
        documents.extend(document)
        
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=7500, chunk_overlap=100)
    all_chunks = []
    
    for document in documents:
        chunks = text_splitter.split_documents([document])
        all_chunks.extend(chunks)
    
    vector_db = Chroma.from_documents(
        documents = all_chunks,
        embedding = OllamaEmbeddings(model="nomic-embed-text", show_progress=True),
        collection_name="local-rag"
    )
    return vector_db
