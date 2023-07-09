from dotenv import load_dotenv
import streamlit as st
import langchain
from langchain.callbacks import get_openai_callback
from libs.knowledge_base import get_vector_store
from libs.text_utils import get_text_from_file, get_pdf_text, get_docx_text, get_text_chunks
from libs.langchain_utils import get_conversation_agent
from pathlib import Path
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


langchain.verbose = False

def update_file(credentials):
    with open('./config.yaml') as file:
        data = yaml.load(file, Loader=SafeLoader)
    data['credentials'] = credentials

    with open('./config.yaml', 'w') as file:
        yaml.dump(data,file)

def handle_userinput(user_question):
    with get_openai_callback() as cb:
        response = st.session_state.conversation.run(input=user_question)
        print(cb)
    st.write(response)


def main():
    load_dotenv()
    st.set_page_config(page_title="Ask your PDF")
    st.header("Ask your PDF 💬")

    # --- OPEN FILE ---
    with open('./config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days']
        )    

    # --- USER AUTHENTICATION ---
    if not st.session_state['authentication_status']:
        tab1, tab2 = st.tabs(["Login", "Sing up"])

        with tab1:
            try:
                name, authentication_status, username = authenticator.login("Login", "main")
            except Exception as e:
                st.sidebar.error(str(e).splitlines()[0])

            if authentication_status == False:
                st.error("Username/password is incorrect")

            if authentication_status == None:
                st.warning("Please enter your username and password")
        with tab2:
            try:            
                value=authenticator.register_user('Register user', location='main' ,preauthorization=False)
                if value:
                    update_file(authenticator.credentials)
                    st.success('User registered successfully')
                
            except Exception as e:
                st.error(str(e).splitlines()[0])

    # --- PROGRAM ---
    else:
        # st.sidebar.title("Ask your docs")
        st.sidebar.header(f"Welcome {st.session_state['name']}")
        authenticator.logout('Log out', location='sidebar')

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
                    text += get_text_from_file(doc)

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