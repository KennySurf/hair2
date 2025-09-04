# core/dialogue_manager
from nlu.get_message_classification import return_message_classification
from classifire_logic.booking.make_booking_reply import get_booking_reply
from classifire_logic.question.make_question_reply import get_question_reply
from classifire_logic.other.make_other_reply import get_other_reply
from classifire_logic.smalltalk.make_smalltalk_reply import get_smalltalk_reply

def dialogue_manager(user_id, message):
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

    return reply
