

"""
1: Client Message
2: Phase1A
3: Phase1B
4: Phase2A
5: Phase2B
6: Decision
"""


class Message:
    def __init__(self, message, msg_type, instance,):
        self.message = message
        self.type = msg_type
        self.instance = 0
