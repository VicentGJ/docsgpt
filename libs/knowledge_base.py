from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings


def get_vector_store(text_chunks):
    embedding = OpenAIEmbeddings()
    vector_store = FAISS.from_texts(text_chunks, embedding)
    return vector_store
