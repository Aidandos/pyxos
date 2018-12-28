

"""
1: Client Message
2: Phase1A
3: Phase1B
4: Phase2A
5: Phase2B
6: Decision
7: Leader
"""


class Message:
    def __init__(self, msg_type, message=0, instance=0, iid=0, c_rnd=0, c_val=0, rnd=0,
                 v_val=0, v_rnd=0, current_leader=0, prop_id=0):
        self.message = message
        self.type = msg_type
        self.instance = instance
        self.iid = iid
        self.c_rnd = c_rnd
        self.c_val = c_val
        self.rnd = rnd
        self.v_val = v_val
        self.v_rnd = v_rnd
        self.current_leader = current_leader
        self.prop_id = prop_id

