# classifire_logic/question/make_question_reply.py
from classifire_logic.question.get_question_intent import return_question_intent
from services.gpt.gpt_client import send_to_gpt
from db.db_funcs import add_message, get_user_messages
from classifire_logic.question.all_services import get_all_services_reply
from classifire_logic.question.service_cost import get_service_cost_reply
from classifire_logic.question.service import get_service_reply

def get_question_reply(user_id, user_message):
    intent = return_question_intent(user_id, user_message)

    if intent == 'все услуги':
        return get_all_services_reply(user_id)
    elif intent == 'Вопрос цены':
        return get_service_cost_reply(user_id)
    else:
        return get_service_reply(user_id, intent)
