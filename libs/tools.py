import ai21
from langchain.agents import Tool
from langchain.chains import RetrievalQA
from langchain.agents import tool


def get_qa_tool(chain: RetrievalQA) -> Tool:
    return Tool(
        name='get_information',
        func=chain.run,
        description="A search tool. Mandatory to find information that is relevant to the user's question. Input should be a search query."
    )


def get_summarize_tool() -> Tool:

    def get_summarize_func(text: str) -> str:
        summary = ai21.Summarize.execute(
            source=text,
            sourceType="TEXT"
        )

        return summary

    return Tool(
        name="Summarize",
        func=get_summarize_func,
        description="A tool to summarize english text. Use it when the user wants the summary of a piece of english text or the user wants the main idea of an english text. Input should be a piece of text in English."
    )
