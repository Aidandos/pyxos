

"""
1: Client Message
2: Phase1A
3: Phase1B
4: Phase2A
5: Phase2B
6: Decision
"""


class Message:
    def __init__(self, message, msg_type, instance=0, c_rnd=0, c_val=0, rnd=0, v_val=0, v_rnd=0):
        self.message = message
        self.type = msg_type
        self.instance = instance
        self.c_rnd = c_rnd
        self.c_val = c_val
        self.rnd = rnd
        self.v_val = v_val
        self.v_rnd = v_rnd

