import os
import ai21
import langchain
from dotenv import load_dotenv
from libs.ai_utils import get_agent_for_summary


load_dotenv()
ai21.api_key = os.getenv('AI21_API_KEY')

text = """"
The Seventh Conference of the International Woman Suffrage Alliance met in Budapest, Hungary, from 15 to 21 June 1913. As had been the case with all the preceding conferences, the location had been chosen to reflect the status of women's suffrage: a place where the prospects seemed favorable and liable to influence public sentiment by demonstrating that it was now a global movement. When it had been announced at the sixth congress (in Stockholm) that the next one would be held in the capital of Hungary, it was felt that the location seemed very remote, and there were concerns that Hungary did not have representative government. In fact, it proved to be one of the largest and most important conventions. Furthermore the delegates stopped en route for mass meetings and public banquets in Berlin, Dresden, Prague and Vienna, spreading its influence ever further afield. This poster for the conference, designed by Anna Soós Korányi and now in the collection of the French Union for Women's Suffrage, depicts a woman helping Atlas hold up a globe on his shoulders.
"""

agent = get_agent_for_summary()

agent.run(f"Haz un resumen del texto: {text}.")
