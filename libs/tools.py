import tempfile, os
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.tools import BaseTool
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.agents.agent import AgentExecutor
from libs.table_formats_agent import create_table_format_agent
from libs.text_utils import get_text_from_path, get_text_from_file
from libs.summarization import summarize_long_text, summarize_url


def get_qa_tool(chain: RetrievalQA) -> Tool:
    """
    Creates a Tool object for retrieving information using a RetrievalQA object.

    :param chain: The RetrievalQA object to use for retrieving information.
    :type chain: RetrievalQA
    :return: A Tool object for retrieving information.
    :rtype: Tool
    """
    return Tool(
        name='get_information',
        func=chain.run,
        description="A search tool. Mandatory to find information that is relevant to the user's question. Input should be a search query."
    )


def get_summarize_file_tool() -> Tool:
    """
    Creates a Tool object for summarizing the text content of a file.

    :return: A Tool object for summarizing the text content of a file.
    :rtype: Tool
    """
    return Tool(
        name="summarize_file",
        func=summarize_file,
        description=""
    )


def get_summarize_url_tool() -> Tool:
    """
    Creates a Tool object for summarizing the text content of a URL.

    :return: A Tool object for summarizing the text content of a URL.
    :rtype: Tool
    """
    return Tool(
        name='summarize_url',
        func=summarize_url,
        description="A tool for summarizing the text content of a URL. Input should be a URL string."
    )


def get_summarize_file_from_path_tool() -> Tool:
    """
    Creates a Tool object for summarizing the text content of a file at a specified path.

    :return: A Tool object for summarizing the text content of a file at a specified path.
    :rtype: Tool
    """
    return Tool(
        name='summarize_file_from_path',
        func=summarize_file_from_path,
        description="A tool for summarizing the text content of a file at a specified path. Input should be a file path string."
    )


def summarize_file_from_path(path: str) -> str:
    """
    Summarizes the text content of a file at a specified path.

    :param path: The path of the file to summarize the text content of.
    :type path: str
    :return: The summary of the text content.
    :rtype: str
    """
    # Use the get_text_from_path function to extract the text from the file
    text = get_text_from_path(path)

    # Use the summarize_long_text function to summarize the extracted text
    return summarize_long_text(text)


def summarize_file(file) -> str:
    """
    Summarizes the text content of a file.

    :param file: The file to summarize the text content of.
    :type file: File object
    :return: The summary of the text content.
    :rtype: str
    """
    # Use the get_text_from_file function to extract the text from the file
    text = get_text_from_file(file)

    # Use the summarize_long_text function to summarize the extracted text
    return summarize_long_text(text)


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
