from classifire_logic.booking.answer_intent_logic import answer_intent
from classifire_logic.booking.other_intent_logic import other_intent
from db.db_funcs import get_state, get_user_messages, add_message
from classifire_logic.booking.get_booking_intent import return_booking_intent

def get_booking_reply(user_id, user_message):
    prompt = ''
    state = get_state(user_id)
    user_messages = get_user_messages(user_id)

    intent = return_booking_intent(user_message)
    if intent == 'answer':
        print(user_message)
        reply = answer_intent(user_id, user_message)
    else:
        reply = other_intent(user_id)

    add_message(user_id, 'assistant', reply)
    return reply