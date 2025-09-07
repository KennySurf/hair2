from services.gpt.gpt_client import send_to_gpt
from db.db_funcs import get_user_messages

def get_tryon_reject_reply(user_id, message):
    messages = get_user_messages(user_id)

    prompt = f"""
    Вежливо ответь клиенту, что тогда мы бы могли записать его на консультацию.
    """

    reply = send_to_gpt(messages + [{'role': 'system', 'content': prompt}])
    return reply
