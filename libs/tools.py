from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.tools import BaseTool
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.agents.agent import AgentExecutor
from libs.table_formats_agent import create_table_format_agent
import tempfile, os


def get_qa_tool(chain: RetrievalQA) -> Tool:
    return Tool(
        name='get_information',
        func=chain.run,
        description="A search tool. Mandatory to find information that is relevant to the user's question. Input should be a search query."
    )

def get_table_tool_by_route(route_user_file: str) -> Tool:

    with open(route_user_file, mode="rb") as user_file:
        with tempfile.NamedTemporaryFile(delete=False, prefix="temporal_file_of_data",dir='./demo') as temp_file:
            temp_file.write(user_file.read())
            temp_file.seek(0)
            temp_path = temp_file.name

    agent: AgentExecutor = create_table_format_agent(
        OpenAI(temperature=0),
        temp_path,
        extension=route_user_file.split(".")[-1],
        verbose=False,
        max_iterations=3
    )

    os.remove(temp_path)

    return Tool(
        name='get_csv_information',
        func=agent.run,
        description="A search tool. Mandatory to find information that is relevant to the user's question inside sheets and tables. Input must be a search query."
    )


def get_table_tool_by_file(user_file) -> Tool:

    with tempfile.NamedTemporaryFile(delete=False, prefix="temporal_file_of_data",dir='./demo') as temp_file:
        temp_file.write(user_file.read())
        temp_file.seek(0)
        temp_path = temp_file.name

    agent: AgentExecutor = create_table_format_agent(
        ChatOpenAI(temperature=0),
        temp_path,
        extension=user_file.name.split(".")[-1],
        verbose=False,
        max_iterations=3
    )

    os.remove(temp_path)

    return Tool(
        name='get_csv_information',
        func=agent.run,
        description="A search tool. Mandatory to find information that is relevant to the user's question inside a csv, xlsx or ods document. The entry must be a search query."
    )
