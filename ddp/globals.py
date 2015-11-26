from message_queue import MessageQueue
from subscription_pool import SubscriptionPool

__DESTROY__ = "__DESTROY__"
ddp_message_queue = MessageQueue()
ddp_subscriptions = SubscriptionPool()
ddp_sessions = {}
ddp_connections = []

