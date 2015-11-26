from message_queue import MessageQueue
from subscription_pool import SubscriptionPool

DESTROY_METHOD = "__DESTROY__"
ddp_message_queue = MessageQueue()
ddp_subscriptions = SubscriptionPool()
ddp_sessions = {}
ddp_connections = []

