import os
import ai21
from dotenv import load_dotenv
import libs.tools

load_dotenv()
ai21.api_key = os.getenv('AI21_API_KEY')

# text = "demo/New OpenDocument Text.odt"
# text = "demo/Long text.docx"
# text = "https://en.wikipedia.org/wiki/Elvis_Presley"
# text = "demo/demo.txt"
# text = "demo/2020_2011.09825.pdf"
# text = "demo/El ciclo empresarial y las transacciones económicas.pdf"
text = "demo/Prerrequisitos del AEF.pdf"

# agent = get_agent_for_summary()
# agent.run(f"Haz un resumen del texto: {text}.")

# print(libs.ai_utils.summarize_long_text(text))
# print(libs.ai_utils.summarize_url(text))
# print(libs.tools.summarize_file_from_path(text))
print(libs.tools.summarize_file_from_path(text))
