from classifire_logic.tryon.get_tryon_intent import return_tryon_intent
from classifire_logic.tryon.make_tryon_accept_reply import get_tryon_accept_reply
from classifire_logic.tryon.make_tryon_other_reply import get_tryon_other_reply
from classifire_logic.tryon.make_tryon_reject_reply import get_tryon_reject_reply
from db.db_funcs import add_message


def intent_manager(user_id, message):
    intent = return_tryon_intent(user_id, message)

    if intent == 'TRYON_ACCEPT':
        reply = get_tryon_accept_reply(user_id, message)
    elif intent == 'TRYON_REJECT':
        reply = get_tryon_reject_reply(user_id, message)
    else:
        reply = get_tryon_other_reply(user_id, message)

    add_message(user_id, 'assistant', reply)
    return reply