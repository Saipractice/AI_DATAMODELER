import os
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

from config import OPENAI_API_KEY

def load_vector_store(index_path="data/faiss_index"):
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vector_store = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    return vector_store, embeddings




# import os
# import pandas as pd
# from pathlib import Path
# from langchain_openai import OpenAIEmbeddings
# from langchain.vectorstores import FAISS
# from langchain.docstore.document import Document

# INDEX_PATH = "data/faiss_index"
# CSV_PATH = "data/Silver_Table.csv"
# OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# def build_documents_from_csv(csv_path):
#     df = pd.read_csv(csv_path)

#     def row_to_text(row):
#         return " | ".join([f"{col}: {row[col]}" for col in df.columns if pd.notnull(row[col])])

#     documents = [Document(page_content=row_to_text(row), metadata={"row": i}) for i, row in df.iterrows()]
#     return documents

# def create_vector_store():
#     print("🔄 Creating FAISS index...")
#     documents = build_documents_from_csv(CSV_PATH)
#     embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
#     vectorstore = FAISS.from_documents(documents, embeddings)
#     vectorstore.save_local(INDEX_PATH)
#     print("✅ FAISS index created and saved.")
#     return vectorstore, embeddings

# def load_vector_store():
#     embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

#     faiss_index_path = Path(INDEX_PATH) / "index.faiss"
#     if not faiss_index_path.exists():
#         print("⚠️ FAISS index not found. Generating now...")
#         return create_vector_store()
    
#     print("📦 Loading existing FAISS index...")
#     vectorstore = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
#     print("✅ FAISS index loaded.")
#     return vectorstore, embeddings




import os
import pandas as pd
from pathlib import Path
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document

# HuggingFace model via langchain-community
from langchain_community.embeddings import HuggingFaceEmbeddings

# Constants
CSV_PATH = "data/Silver_Table.csv"
INDEX_PATH = "data/faiss_index"

def get_embedding_provider():
    print("🧠 Using HuggingFace embedding model: BAAI/bge-small-en-v1.5")
    return HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

def build_documents_from_csv(csv_path):
    df = pd.read_csv(csv_path)
    def row_to_text(row):
        return " | ".join([f"{col}: {row[col]}" for col in df.columns if pd.notnull(row[col])])
    return [Document(page_content=row_to_text(row), metadata={"row": i}) for i, row in df.iterrows()]

def create_vector_store():
    print("🔄 Creating FAISS index...")
    documents = build_documents_from_csv(CSV_PATH)
    embeddings = get_embedding_provider()
    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local(INDEX_PATH)
    print("✅ FAISS index created and saved.")
    return vectorstore, embeddings

def load_vector_store():
    embeddings = get_embedding_provider()
    faiss_index_path = Path(INDEX_PATH) / "index.faiss"
    if not faiss_index_path.exists():
        print("⚠️ FAISS index not found. Generating now...")
        return create_vector_store()
    
    print("📦 Loading existing FAISS index...")
    vectorstore = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
    print("✅ FAISS index loaded.")
    return vectorstore, embeddings