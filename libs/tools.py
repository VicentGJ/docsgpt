from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.tools import BaseTool
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.agents.agent import AgentExecutor
from langchain.agents import create_csv_agent
from libs.table_formats_agent import create_table_format_agent
import tempfile, os


def get_qa_tool(chain: RetrievalQA) -> Tool:
    return Tool(
        name='get_information',
        func=chain.run,
        description="A search tool. Mandatory to find information that is relevant to the user's question. Input should be a search query."
    )

def get_csv_tool_by_route(route_user_csv: str) -> Tool:

    with open(route_user_csv, mode="rb") as user_csv:
        with tempfile.NamedTemporaryFile(delete=False, prefix="temporal_file_of_data",dir='./demo') as temp_file:
            temp_file.write(user_csv.read())
            temp_file.seek(0)
            temp_path = temp_file.name

    agent: AgentExecutor = create_csv_agent(OpenAI(temperature=0), temp_path,verbose=True)

    os.remove(temp_path)

    return Tool(
        name='get_csv_information',
        func=agent.run,
        description="A search tool. Mandatory to find information that is relevant to the user's question inside a csv document. The entry must be a search query."
    )


def get_csv_tool_by_file(user_csv) -> Tool:

    with tempfile.NamedTemporaryFile(delete=False, prefix="temporal_file_of_data",dir='./demo') as temp_file:
        temp_file.write(user_csv.read())
        temp_file.seek(0)
        temp_path = temp_file.name

    agent: AgentExecutor = create_csv_agent(OpenAI(temperature=0), temp_path, verbose=False, max_iterations=3)

    os.remove(temp_path)

    return Tool(
        name='get_csv_information',
        func=agent.run,
        description="A search tool. Mandatory to find information that is relevant to the user's question inside a csv document. The entry must be a search query."
    )

    #A search tool. Mandatory to find information that is relevant to the user's question inside a csv, xlsx or ods document. The entry must be a search query.