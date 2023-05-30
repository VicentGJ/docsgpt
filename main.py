from dotenv import load_dotenv
import streamlit as st
import langchain
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
langchain.verbose = False


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text, chunk_size, chunk_overlap):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    return text_splitter.split_text(text)


def get_vector_store(text_chunks):
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_texts(text_chunks, embeddings)
    return vector_store


def get_conversation_chain(vector_store):
    llm = ChatOpenAI()
    question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT)
    doc_chain = load_qa_chain(llm, chain_type='map_reduce')

    memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True
    )

    chain = ConversationalRetrievalChain(
        retriever=vector_store.as_retriever(),
        question_generator=question_generator,
        combine_docs_chain=doc_chain,
        memory=memory
    )
    return chain


def handle_userinput(user_question):
    with get_openai_callback() as cb:
        response = st.session_state.conversation({'question': user_question})
        print(cb)
    st.write(response["answer"])


def main():
    load_dotenv()
    st.set_page_config(page_title="Ask your PDF")
    st.header("Ask your PDF 💬")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    # upload file
    pdf_docs = st.file_uploader("Upload your PDFs", type="pdf", accept_multiple_files=True)

    # extract the text
    if st.button("Process"):
        text = get_pdf_text(pdf_docs)

        # split into chunks
        text_chunks = get_text_chunks(text=text, chunk_size=1000, chunk_overlap=200)

        # create embeddings
        vector_store = get_vector_store(text_chunks)

        # create conversation chain
        st.session_state.conversation = get_conversation_chain(vector_store)

    # show user input
    user_question = st.text_input("Ask a question about your docs:")
    if user_question:
        handle_userinput(user_question)


if __name__ == '__main__':
    main()
