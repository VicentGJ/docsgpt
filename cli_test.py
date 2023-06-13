from dotenv import load_dotenv
import langchain
import textract
from langchain.callbacks import get_openai_callback
from libs.knowledge_base import get_vector_store
from libs.text_utils import get_text, get_pdf_text, get_docx_text, get_text_chunks
from libs.ai_utils import get_conversation_agent

load_dotenv()
text = ''
text = textract.process('demo/demo.txt', extension='txt').decode('utf-8')

text_chunks = get_text_chunks(text=text, chunk_size=1000, chunk_overlap=200)

vector_store = get_vector_store(text_chunks)

agent = get_conversation_agent(vector_store)

agent.run("Cuales son los tres pilares de desarrollo")
agent.run("Dame la respuesta en italiano")