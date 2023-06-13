from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.tools import BaseTool
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA


def get_qa_tool(chain: RetrievalQA) -> Tool:
    return Tool(
        name='get_information',
        func=chain.run,
        description="Always use to get the information needed to answer any questions. Input should be user's question."
    )
