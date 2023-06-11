from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.tools import BaseTool
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA


def get_qa_tool(chain: RetrievalQA) -> Tool:
    return Tool(
        name='qa_from-docs',
        func=chain.run,
        description="Use to get the Information needed to answer all questions. Input should be user's question."
    )
