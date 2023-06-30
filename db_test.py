import os
import ai21
import pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from dotenv import load_dotenv
from libs.text_utils import get_text_segments, get_text_from_path

load_dotenv()
# TODO Load key directly in the required lib
ai21.api_key = os.getenv('AI21_API_KEY')


def init_pinecone_db() -> None:
    # initialize pinecone
    pinecone.init(
        api_key=os.getenv('PINECONE_API_KEY'),  # find at app.pinecone.io
        environment=os.getenv('PINECONE_API_ENV'),  # next to api key in console
    )


def get_pinecone_vector_store(index_name: str) -> Pinecone:
    if index_name not in pinecone.list_indexes():
        # we create a new index
        pinecone.create_index(
            name=index_name,
            metric='cosine',
            dimension=1536  # 1536 dim of text-embedding-ada-002
        )

    embedding = OpenAIEmbeddings()
    vector_store = Pinecone.from_existing_index(index_name=index_name, embedding=embedding)

    return vector_store


def add_file_to_pinecone_db(file_path: str, vector_store: Pinecone) -> None:
    text = get_text_from_path(file_path)
    texts = get_text_segments(text, 'TEXT')
    print("chunks ready")
    vector_store.add_texts(texts=texts)


def get_similar_docs(query: str, vector_store: Pinecone) -> list[str]:
    pinecone_docs = vector_store.similarity_search(query, k=5)
    docs: list[str] = []
    for doc in pinecone_docs:
        docs.append(doc.page_content)
        print(doc.page_content)

    return docs


def main():
    index_name = "test1"
    query = "Cuales son los mejores algoritmos de ordenamiento?"
    init_pinecone_db()
    vector_store = get_pinecone_vector_store(index_name)
    print("yes")
    # add_file_to_pinecone_db("demo/Algorithms + Data Structures = Programs.pdf", vector_store)
    print("YES")
    get_similar_docs(query, vector_store)


if __name__ == '__main__':
    main()
