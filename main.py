from dotenv import load_dotenv
import streamlit as st
import langchain
from langchain.callbacks import get_openai_callback
from libs.knowledge_base import get_vector_store
from libs.text_utils import get_text, get_pdf_text, get_docx_text, get_text_chunks
from libs.ai_utils import get_conversation_agent


langchain.verbose = False


def handle_userinput(user_question):
    with get_openai_callback() as cb:
        response = st.session_state.conversation.run(input=user_question)
        print(cb)
    st.write(response)


def main():
    load_dotenv()
    st.set_page_config(page_title="Ask your PDF")
    st.header("Ask your PDF 💬")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    # upload file
    docs = st.file_uploader("Upload your PDFs or DOCXs", type=["pdf", "docx", "txt", "odt"], accept_multiple_files=True)

    # extract the text
    if st.button("Process"):
        text = ""
        for doc in docs:
            if doc.type == "application/pdf":
                text = get_pdf_text(doc)
            elif doc.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                text = get_docx_text(doc)
            else:
                # Other formats allowed by textract: eml, epub, html, json, rtf, txt, odt
                # TODO Test all the textract formats
                text += get_text(doc)

        # split into chunks
        text_chunks = get_text_chunks(text=text, chunk_size=1000, chunk_overlap=200)

        # create embeddings
        vector_store = get_vector_store(text_chunks)

        # create conversation agent
        agent = get_conversation_agent(vector_store)
        st.session_state.conversation = agent

    # show user input
    user_question = st.text_input("Ask a question about your docs:")
    if user_question:
        handle_userinput(user_question)


if __name__ == '__main__':
    main()