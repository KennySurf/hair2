# core/dialogue_manager
from nlu.get_message_classification import return_message_classification
from classifire_logic.booking.make_booking_reply import get_booking_reply

def dialogue_manager(user_id, message):
    message_classification = return_message_classification(user_id, message)
    reply = 'Повторите вопрос'

    if message_classification == 'smalltalk':
        reply = 'smalltalk'
    elif message_classification == 'other':
        reply = 'other'
    elif message_classification == 'question':
        reply = 'question'
    elif message_classification == 'booking':
        reply = get_booking_reply(user_id, message)

    return reply
