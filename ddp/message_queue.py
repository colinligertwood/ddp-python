import Queue

class MessageQueue(Queue.Queue):
    """
    """

    def enqueue(self, message):
        return self.put(message)

    def dequeue(self):
        return self.get()


