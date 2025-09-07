from db.db_funcs import get_user_messages
from services.gpt.gpt_client import send_to_gpt
from docx import Document


def get_tryon_other_reply(user_id, message):
    messages = get_user_messages(user_id)
    file = f'classifire_logic/question/files/общее положение.docx'

    doc = Document(file)

    full_text = "\n".join([para.text for para in doc.paragraphs])


    prompt = f"""
    Если клиент задаёт вопросы касательно визуализации, отвечай на них. Информацию можешь брать из доп материалов.
    доп материалы: {full_text}
    """

    reply = send_to_gpt(messages + [{'role': 'system', 'content': prompt}])
    return reply
