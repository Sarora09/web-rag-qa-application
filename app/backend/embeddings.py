from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
load_dotenv()

embeddings = HuggingFaceEmbeddings(
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
    )