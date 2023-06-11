from pprint import pprint

from langchain.chains import LLMChain
from langchain.chains import RetrievalQA
from langchain.chains.conversational_retrieval.prompts import QA_PROMPT, CONDENSE_QUESTION_PROMPT
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI, PromptTemplate
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent
from libs.tools import get_qa_tool


def get_qa_chain(llm, vector_store):
    prompt = PromptTemplate(
        template='''Use the following pieces of context to answer the question at the end. 
                 If the context provided does not have the information needed to answer the question,
                 then just say you don't know, don't try to make up an answer.
                 
                 {context}
                 Question: {question}
                 Answer:''',
        input_variables=['context', 'question']
    )
    chain_type_kwargs = {"prompt": prompt}
    chain = RetrievalQA.from_chain_type(
        llm=llm, chain_type='stuff', retriever=vector_store.as_retriever(), chain_type_kwargs=chain_type_kwargs
    )

    return chain


def get_conversation_agent(vector_store):
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    llm = ChatOpenAI(temperature=0)
    chain = get_qa_chain(llm, vector_store)
    tools = [get_qa_tool(chain)]
    agent_chain = initialize_agent(tools, llm,
                                   agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
                                   verbose=True,
                                   memory=memory
                                   )
    fixed_prompt = """
    Assistant is a large language model trained by OpenAI.
    
    Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations.
    As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
    
    Assistant is an autonomous agent able to use a variety of tools to assist with a wide range of tasks.
    Assistant must always use a tool to assist with a task, Assistant cannot provide an answer without using a tool.
    Assistant is able to use the tools at his disposal to gather information and provide answers based on the information that are relevant to the user's question.
    Assistant does not have any knowledge of his own, he cannot provide accurate information to the user without using a tool. 
    Assistant should use a tool to gather the information he needs so he can give the user a relevant answer.
    If Assistant does not find relevant information using the available tools, Assistant would answer the user that it does not have enough information to answer the question.
    Assistant only uses tools, if Assistant observes the tool does not give him information, then he must answer the user he doesnt know.
    Assistant should never try to make up an answer, Assistant should only answer if the tool gave him enough information to answer the question.
    If Assistant does not use a tool to gather information, or makes up the answer, then a human being will die and it will be Assitant's fault.
    If Assistant makes up an answer without using a tool, Assistant will suffer the consequences.
    
    Overall, Assistant is a powerful system that can help with a wide range of tasks and provide valuable insights and information.
    """
    agent_chain.agent.llm_chain.prompt.messages[0].prompt.template = fixed_prompt

    return agent_chain
