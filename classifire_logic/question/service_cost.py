from docx import Document
from db.db_funcs import update_services_id, update_state, get_user_messages, add_message
from services.gpt.gpt_client import send_to_gpt


def get_service_cost_reply(user_id):
    user_messages = get_user_messages(user_id)

    file = f'classifire_logic/question/files/общее положение.docx'

    doc = Document(file)
    full_text = "\n".join([para.text for para in doc.paragraphs])

    prompt = f"""
    Если клиент спрашивает про цену услуги - вежливо сообщай ему, что цену сказать можем только после консультации
    объясни почему это так и спроси хочет ли он записаться на неё?'
    
    Информацию почему только после консультации можем можно взять тут:
    {full_text}
    """

    service_prompt = f"""
    выдели услугу из запроса клиента.
    Наш пул:
    окрашивание
    наращивание
    
    Строго напиши только название нашей услуги, к которой подходит клиентский запрос.
    """

    service_name = send_to_gpt(user_messages[:-1] + [{'role': 'assistant', 'content': service_prompt}] + user_messages[-1:])

    if service_name == 'окрашивание':
        update_services_id(user_id, '17637553')
    else:
        update_services_id(user_id, '10928000')
    update_state(user_id, 'get_advice')

    reply = send_to_gpt(user_messages[:-1] + [{'role': 'assistant', 'content': prompt}] + user_messages[-1:])

    add_message(user_id, 'assistant', reply)
    return reply
