

"""
1: Client Message
2: Phase1A
3: Phase1B
4: Phase2A
5: Phase2B
6: Decision
7: Leader
8: Catchup
9: Catchup_Answer
"""


class Message:
    def __init__(self, msg_type, message=0, instance=0, iid=0, c_rnd=0, c_val=0, rnd=0,
                 v_val=0, v_rnd=0, current_leader=0, prop_id=0, msg_memory=None,
                 print_order=None, total_order=None, total_order_sent=None,
                 total_order_memory=None):
        # Basic message variables needed for various applications inside Paxos
        self.message = message
        self.type = msg_type
        self.instance = instance
        self.iid = iid
        # The values as known from the slides
        self.c_rnd = c_rnd
        self.c_val = c_val
        self.rnd = rnd
        self.v_val = v_val
        self.v_rnd = v_rnd
        # current leader and prop_id needed for leader election
        self.current_leader = current_leader
        self.prop_id = prop_id
        # msg_memory and total order needed for learner catch_up
        self.msg_memory = msg_memory
        self.print_order = print_order
        self.total_order = total_order
        self.total_order_sent = total_order_sent
        self.total_order_memory = total_order_memory

