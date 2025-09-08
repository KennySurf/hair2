# classifire_logic/question/make_question_reply.py
from classifire_logic.question.get_question_intent import return_question_intent
from classifire_logic.question.all_services import get_all_services_reply
from classifire_logic.question.service_cost.service_cost import get_service_cost_reply
from classifire_logic.question.service import get_service_reply

def get_question_reply(user_id, user_message):
    intent = return_question_intent(user_id, user_message).lower()

    if intent == 'все услуги':
        return get_all_services_reply(user_id)
    elif intent == 'вопрос цены':
        return get_service_cost_reply(user_id)
    else:
        return get_service_reply(user_id, intent)
