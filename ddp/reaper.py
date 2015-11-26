from time import sleep
from globals import *

class Reaper(object):
    def __init__(self):
        """
        """
    def start(self):
        global ddp_sessions
        global ddp_subscriptions
        while True:
            sleep(10)
            reap_sessions = []
            reap_subscriptions = []
            for ddp_session_id, session in ddp_sessions.items():
                if session.has_expired():
                    reap_sessions.append(ddp_session_id)

            for subscription in ddp_subscriptions:
                if subscription.method == DESTROY_METHOD:
                    reap_subscriptions.append(subscription.id)
                    
            for ddp_session_id in reap_sessions:
                ddp_subscriptions.remove_session(ddp_session_id)
                del ddp_sessions[ddp_session_id]

            for ddp_subscription_id in reap_subscriptions:
                ddp_subscriptions.remove_id(ddp_subscription_id)
