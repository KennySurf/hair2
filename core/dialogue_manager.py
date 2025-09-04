# core/dialogue_manager
from classifire_logic.get_classifier import get_message_classification
from classifire_logic.booking_classifier import get_booking_reply

def dialogue_manager(user_id, message):
    message_classification = get_message_classification(message)
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