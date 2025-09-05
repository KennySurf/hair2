from classifire_logic.tryon.get_tryon_intent import return_tryon_intent
from classifire_logic.tryon import make_tryon_other_reply, make_tryon_accept_reply

def intent_manager(message):
    intent = return_tryon_intent(message)

    if intent == 'TRYON_ACCEPT':
        make_tryon_accept_reply
    elif intent == 'TRYON_REJECT':
        prompt = """
        
        """

        reply = None
        return reply
    else:
        make_tryon_other_reply
