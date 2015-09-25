class SubscriptionPool(list):
    """
    """

    def add(self, subscription):
        self.append(subscription)

    def remove_id(self, subscription_id):
        subscriptions = [subscription for subscription in self if subscription.id == subscription_id]
        for subscription in subscriptions:
            self.remove(subscription)


