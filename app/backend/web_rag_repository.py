from urllib.parse import urlparse
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import CharacterTextSplitter
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
import uuid
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

def is_valid_url(url: str) -> bool:
    if url is None or url.strip() == "":
        return False
    result = urlparse(url)
    is_valid = (
            all([result.scheme, result.netloc]) and 
            result.scheme in ['http', 'https'] and
            '.' in result.netloc and
            not result.netloc.endswith('.') and 
            len(result.netloc.split('.')[-1]) >= 2
        )
    return is_valid

def setup_database(url) -> str:
    loader = WebBaseLoader([url,])
    website_document = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    website_document_chunks = text_splitter.split_documents(website_document)
    embeddings = HuggingFaceEmbeddings(
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
    )
    db = FAISS.from_documents(website_document_chunks, embeddings)
    db_name = str(uuid.uuid4())
    faiss_dbs_folder = os.path.join(os.path.dirname(__file__), "faiss_dbs", db_name)
    os.makedirs(faiss_dbs_folder, exist_ok=True)
    db.save_local(faiss_dbs_folder)
    return db_name
    

def fetch_data(query: str, db_name: str) -> str:
    embeddings = HuggingFaceEmbeddings(
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
    )
    faiss_db_folder = os.path.join(os.path.dirname(__file__), "faiss_dbs", db_name)
    new_faiss_db = FAISS.load_local(faiss_db_folder, embeddings, allow_dangerous_deserialization=True)
    template = """You are an expert research assistant. Use the following pieces of retrieved context to answer the question.
                If you don't know the answer, just say that you don't know. Don't try to make an answer.
                Use maximum 10 sentences maximum and keep your answer to the point.
                Question: {question}
                Context: {context}
                Answer:
                """
    prompt = ChatPromptTemplate.from_template(template)
    retriever = new_faiss_db.as_retriever()
    llm = ChatGroq(model="openai/gpt-oss-20b")
    str_output_parser = StrOutputParser()
    rag_chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough()
        } | prompt | llm | str_output_parser
    )
    ai_response = rag_chain.invoke(query)
    return ai_response
    
def delete_database(db_name: str) -> str:
    faiss_dbs_folder = os.path.join(os.path.dirname(__file__), "faiss_dbs", db_name)
    if not os.path.exists(faiss_dbs_folder):
        return "Database not found"
    for file in os.listdir(faiss_dbs_folder):
        file_path = os.path.join(faiss_dbs_folder, file)
        os.remove(file_path)
    os.rmdir(faiss_dbs_folder)
    return "Database deleted successfully"