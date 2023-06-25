from langchain.agents import Tool
from langchain.chains import RetrievalQA
from libs.text_utils import get_text_from_path, get_text_from_file
from libs.summarization import summarize_long_text, summarize_url


def get_qa_tool(chain: RetrievalQA) -> Tool:
    return Tool(
        name='get_information',
        func=chain.run,
        description="A search tool. Mandatory to find information that is relevant to the user's question. Input should be a search query."
    )


def get_summarize_file_tool() -> Tool:
    return Tool(
        name="summarize_file",
        func=summarize_file,
        description=""
    )


def get_summarize_url_tool() -> Tool:
    return Tool(
        name='summarize_url',
        func=summarize_url,
        description=""
    )


def get_summarize_file_from_path_tool() -> Tool:
    return Tool(
        name='summarize_file_from_path',
        func=summarize_file_from_path,
        description=""
    )


def summarize_file_from_path(path: str) -> str:
    return summarize_long_text(get_text_from_path(path))


def summarize_file(file) -> str:
    return summarize_long_text(get_text_from_file(file))
