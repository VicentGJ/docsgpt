from langchain.chains import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.conversational_retrieval.prompts import QA_PROMPT, CONDENSE_QUESTION_PROMPT
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI


def get_conversation_chain(vector_store):
    llm = ChatOpenAI(temperature=0)
    question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT)
    doc_chain = load_qa_chain(llm, chain_type='stuff', prompt=QA_PROMPT)

    memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True
    )

    chain = ConversationalRetrievalChain(
        retriever=vector_store.as_retriever(),
        # max_tokens_limit=3000,
        question_generator=question_generator,
        combine_docs_chain=doc_chain,
        memory=memory
    )
    return chain
