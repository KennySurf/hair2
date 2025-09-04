from openai import OpenAI
from dotenv import load_dotenv
from os import getenv
from services.gpt.proxy import set_proxy, clear_proxy

load_dotenv()

set_proxy()
api_key = getenv('GPT_TOKEN')
client = OpenAI(api_key=api_key)
clear_proxy()

def send_to_gpt(message):
    print(f'отправка в GPT message {message}')


    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=message,
        # temperature=0.7
    )
    reply = response.choices[0].message.content.strip()
    print(f'func send to gpt reply ---- {reply}')

    return reply


