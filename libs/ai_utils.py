import ai21
from langchain.chains import RetrievalQA
from langchain.agents import AgentType, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI, PromptTemplate
from langchain.agents import initialize_agent
from libs.tools import get_qa_tool, get_summarize_tool
from libs.text_utils import get_text_segments


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


def get_agent_for_summary() -> AgentExecutor:
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    llm = OpenAI(temperature=0)
    tools = [get_summarize_tool()]
    agent_chain = initialize_agent(tools, llm,
                                   agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
                                   verbose=True,
                                   memory=memory,
                                   handle_parsing_errors="Check your output and make sure it conforms!"
                                   )

    return agent_chain


def summarize_long_text(text: str) -> str:
    texts: list[str] = []
    summary = ""
    count = 0

    if len(text) > 50000:
        text_segments = get_text_segments(text)

        while len(text_segments) > 0:
            texts.append("")
            while len(text_segments) > 0 and len(text_segments[0]) + len(texts[-1]) < 50000:
                texts[-1] += text_segments.pop(0)
    else:
        texts.append(text)

    for text in texts:
        print(len(text))
        result = ai21.Summarize.execute(
        source=text,
        sourceType="TEXT"
        )
        summary += result['summary']
        count += 1

    if count > 1:
        summary = summarize_long_text(summary)

    return summary


