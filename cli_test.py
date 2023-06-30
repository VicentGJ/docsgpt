from dotenv import load_dotenv
from libs.tools import get_table_tool_by_route
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent


def get_temporary_agent(file_route):
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    llm = ChatOpenAI(temperature=0)
    tools = [get_table_tool_by_route(file_route)]
    agent_chain = initialize_agent(tools, llm,
                                   agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
                                   verbose=True,
                                   memory=memory,
                                   handle_parsing_errors="Check your output and make sure it conforms!"
                                   )

    return agent_chain


load_dotenv()

file_route = "demo/Ventas del año.xlsx"

agent = get_temporary_agent(file_route)
agent.run("Cuantas filas tiene el documento")
agent.run('En que mes hubo más ventas?')
agent.run("Cuales fueron las ventas totales del año")
agent.run("Cual es el valor de produccion promedio")
agent.run("Como se llama la novia de Leonardo di Caprio?")

# text = ''
# text = textract.process('demo/demo.txt', extension='txt').decode('utf-8')

# text_chunks = get_text_chunks(text=text, chunk_size=1000, chunk_overlap=200)

# vector_store = get_vector_store(text_chunks)

# agent = get_conversation_agent(vector_store)

# agent.run("Cuales son los tres pilares de desarrollo")
# agent.run("Dame la respuesta en italiano")
