# classifire_logic/booking_classifier.py
from db.db_funcs import get_state, get_services_id, get_date, update_state, get_time, get_user_messages
from services.gpt.gpt_client import send_to_gpt
from docx import Document


def other_intent(user_id):
    messages = get_user_messages(user_id)

    file = f'classifire_logic/question/files/общее положение.docx'
    doc = Document(file)
    full_text = "\n".join([para.text for para in doc.paragraphs])

    prompt = f"""
    Ответь на вопрос клиента опираясь на знания из файла. Только не говори, откуда ты берёшь информацию.
    После ответа вежливо спроси в новом абзаце - хочет ли клиент продолжить запись?
    Но если клиент спрашивает цену наращивания или окрашивания - строго верни ответ - цена
        
    Информация из файла - 
    {full_text}
    """

    reply = send_to_gpt(messages[:-1] + [{'role': 'system', 'content': prompt}] + messages[-1:])

    if reply.lower() == 'цена':
        price_prompt = """
        вежливо ответь клиенту, что цену можем озвучить только на консультации, объясни почему и спроси хочет ли он записаться на неё?
        """
        update_state(user_id, 'get_advice')

        reply = send_to_gpt(messages + [{'role': 'system', 'content': price_prompt}])
    return reply
