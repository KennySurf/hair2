# core/dialogue_manager
from nlu.get_message_classification import return_message_classification
from classifire_logic.booking.make_booking_reply import get_booking_reply
from classifire_logic.question.make_question_reply import get_question_reply
from classifire_logic.other.make_other_reply import get_other_reply
from classifire_logic.smalltalk.make_smalltalk_reply import get_smalltalk_reply
from classifire_logic.tryon.tryon_intent_manager import intent_manager
from db.db_funcs import add_message

def dialogue_manager(user_id, message, update):
    message_classification = return_message_classification(user_id, message)
    reply = 'Повторите вопрос'

    if message_classification == 'smalltalk':
        reply = get_smalltalk_reply(user_id, message)
    elif message_classification == 'other':
        reply = get_other_reply(user_id, message)
    elif message_classification == 'question':
        reply = get_question_reply(user_id, message)
    elif message_classification == 'booking':
        reply = get_booking_reply(user_id, message)
    elif message_classification == 'tryon_request':
        reply = intent_manager(user_id, message)
        add_message(user_id, 'assistant', reply)

    return reply
