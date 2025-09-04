from services.gpt.gpt_client import send_to_gpt
from db.db_funcs import get_user_messages

def get_smalltalk_reply(user_id, user_message):
    messages = get_user_messages(user_id)
    return send_to_gpt(messages + user_message)
