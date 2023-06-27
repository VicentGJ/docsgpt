from langchain.chains import RetrievalQA
from langchain.agents import AgentType, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI, PromptTemplate
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


def get_conversation_agent(vector_store) -> AgentExecutor:
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    llm = OpenAI(temperature=0)
    chain = get_qa_chain(llm, vector_store)
    tools = [get_qa_tool(chain)]
    agent_chain = initialize_agent(tools, llm,
                                   agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
                                   verbose=True,
                                   memory=memory,
                                   handle_parsing_errors="Check your output and make sure it conforms!"
                                   )

    return agent_chain
