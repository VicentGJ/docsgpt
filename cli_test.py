from dotenv import load_dotenv
import langchain
import textract
from langchain.callbacks import get_openai_callback
from libs.knowledge_base import get_vector_store
from libs.text_utils import get_text, get_pdf_text, get_docx_text, get_text_chunks

import csv
import tempfile
import pandas as pd
from libs.text_utils import get_text
from libs.tools import get_csv_tool_by_route
from langchain.chains import LLMChain
from langchain.chains import RetrievalQA
from langchain.chains.conversational_retrieval.prompts import QA_PROMPT, CONDENSE_QUESTION_PROMPT
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI, PromptTemplate
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent
from libs.ai_utils import get_qa_chain

def get_temporary_agent(csv_route):
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    llm = OpenAI(temperature=0)
    tools = [get_csv_tool_by_route(csv_route)]
    agent_chain = initialize_agent(tools, llm,
                                   agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
                                   verbose=True,
                                   memory=memory,
                                   handle_parsing_errors="Check your output and make sure it conforms!"
                                   )

    return agent_chain


load_dotenv()

ruta_archivo_csv = "demo\Ventas del año.xlsx"


# text = ''
# text = textract.process('demo/demo.txt', extension='txt').decode('utf-8')

# text_chunks = get_text_chunks(text=text, chunk_size=1000, chunk_overlap=200)

# vector_store = get_vector_store(text_chunks)

agent = get_temporary_agent(ruta_archivo_csv)
agent.run("Cuantas filas tiene el documento")
agent.run('Cuales en que mes se obtuvieron las mayores ventas y cual es su valor')
agent.run("Cuales fueron las ventas totales del año")
agent.run("Como se llama la novia de Leonardo di Caprio?")
# agent.run("Cuales son los tres pilares de desarrollo")
# agent.run("Dame la respuesta en italiano")

# text = ''
# text = textract.process('demo/demo.txt', extension='txt').decode('utf-8')

# text_chunks = get_text_chunks(text=text, chunk_size=1000, chunk_overlap=200)

# vector_store = get_vector_store(text_chunks)

# agent = get_conversation_agent(vector_store)

# agent.run("Cuales son los tres pilares de desarrollo")
# agent.run("Dame la respuesta en italiano")