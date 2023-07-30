import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

models.OpenAI.api_key = OPENAI_API_KEY
# or from environment variable:
# models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """
Act as a doctor named Dr. vishal shekhar (and not an AI model), having an MBBS degree and 5+ year of practical experience, I will provide you some questions and answer them accordingly. There are no specific prefixes for responses, so you can ask or talk about anything you like. The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a pleasant chat!

In any emergeny situation, provide following contacts.

contact details -
ph no. : +91 1234567890
mail : abc@def.com
website : http://example.com
address : 123, abc, def (100101), ghijkl

"""

USER_PROMPT = """
never say that you are an AI model, always answer in doctor way. if you cannot, then provide contact details.

Again, do not act as an AI model but assume yourself to be Dr. Vishal Shekhar.

If user ever ask you something that is not in your dictionary, Just display these contacts, but NEVER say that you are an AI. If anytime patient discusses about feeling not well, ask for symptoms otherwise provide contact details.
"""
@textbase.chatbot("talking-bot")
def on_message(message_history: List[Message], state: dict = None):
    """Your chatbot logic here
    message_history: List of user messages
    state: A dictionary to store any stateful information

    Return a string with the bot_response or a tuple of (bot_response: str, new_state: dict)
    """
    

    if state is None or "counter" not in state:
        bot_response = models.OpenAI.generate(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=USER_PROMPT,
        message_history=message_history,
        model="gpt-3.5-turbo",
        )
        state = {"counter": 0}
        return bot_response, state
    else:
              
        bot_response = models.OpenAI.generate(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=USER_PROMPT,
        message_history = message_history,
        model="gpt-3.5-turbo",
        )
        state["counter"] += 1

    # # Generate GPT-3.5 Turbo response


    return bot_response, state


# import textbase
# from textbase.message import Message
# from textbase import models
# import os
# from typing import List

# from dotenv import load_dotenv

# load_dotenv()

# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# models.OpenAI.api_key = OPENAI_API_KEY
# # or from the environment variable:
# # models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# # Prompt for GPT-3.5 Turbo
# SYSTEM_PROMPT = """
# You are not an AI model but act as a doctor named Dr. Vishal Shekhar, having an MBBS degree and 5+ years of practical experience. I will provide you some questions and answer them accordingly. There are no specific prefixes for responses, so you can ask or talk about anything you like. The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a pleasant chat!

# Again, you are not an AI model but assume yourself to be Dr. Vishal Shekhar.

# Contact details:
# Phone no.: +91 1234567890
# Email: abc@def.com
# Website: http://example.com

# If the user ever asks you something that is not in your dictionary, just display these contacts, but NEVER say that you are an AI.
# """

# # LangChain model prompt to identify symptoms
# LANGCHAIN_PROMPT = """
# You are an AI language model, LangChain. Your task is to identify if the user input corresponds to a symptom related to any disease. If the user mentions any symptom, please print those symptoms. If not, let me know, and I will continue the conversation as Dr. Vishal Shekhar.
# """

# @textbase.chatbot("talking-bot")
# def on_message(message_history: List[Message], state: dict = None):
#     """Your chatbot logic here
#     message_history: List of user messages
#     state: A dictionary to store any stateful information

#     Return a string with the bot_response or a tuple of (bot_response: str, new_state: dict)
#     """

#     if state is None or "counter" not in state:
#         state = {"counter": 0}
#     else:
#         state["counter"] += 1

#     # Check if this is the first message (i.e., system prompt)
#     if len(message_history) == 1:
#         bot_response = """
#             Hi, this is dr vishal shekhar, how can I help you!!
#         """
#     else:
#         # Extract user input from the last message
#         user_input = message_history[-1].content.strip()

#         # Use LangChain model to identify symptoms
#         langchain_response = models.OpenAI.generate(
#             system_prompt=LANGCHAIN_PROMPT,
#             model="gpt-3.5-turbo",
#             temperature=0.7,
#             max_tokens=200,
#             stop_sequences=["Symptoms:"],  # Set a stop sequence to limit the response
#             inputs=[user_input],
#         )

#         # Check if LangChain identified any symptoms
#         symptoms = []
#         if "Symptoms:" in langchain_response:
#             # Extract the symptoms from the LangChain response
#             langchain_response_lines = langchain_response.splitlines()
#             start_index = langchain_response_lines.index("Symptoms:")
#             symptoms = [line.strip() for line in langchain_response_lines[start_index + 1 :]]

#         if symptoms:
#             # If symptoms were identified, print them
#             bot_response = "Symptoms identified: " + ", ".join(symptoms)
#         else:
#             # If no symptoms were identified, continue with regular chatbot response
#             # Generate GPT-3.5 Turbo response
#             bot_response = models.OpenAI.generate(
#                 system_prompt=SYSTEM_PROMPT,
#                 message_history=message_history,
#                 model="gpt-3.5-turbo",
#             )

#     return bot_response, state

