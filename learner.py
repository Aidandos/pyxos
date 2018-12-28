import argparse
from threading import Thread
import time

from role import Role
from message import Message

parser = argparse.ArgumentParser(description='Client')
parser.add_argument('--id', default=1, type=int)
parser.add_argument('--config', default='', type=str, metavar='PATH',
                    help='path to config')
'''
The Learner has two special functions:
The total order logic will make sure that a message is only sent when it's previous message is
already sent. It can check on that by the msg.instance value.
This results of course in a failure in the lossy test as we need all the messages.
Even when a learner joins later he will have the same guarantee for total order as we can recreate
the queue with the variables sent.
'''

class Learner(Role):
    def __init__(self, iid, configpath):
        super(Learner, self).__init__('learners', iid, configpath)
        self.instances = {}
        self.caught_up = False

        self.send_catch_up_thread = Thread(target=self.send_catch_up)
        self.send_catch_up_thread.start()

        self.print_order = []
        self.msg_memory = {}

        self.temporary_print_order = []
        self.temporary_msg_memory = {}

        self.total_order = {}
        self.total_order_sent = {}
        self.total_order_memory = {}

    def send_catch_up(self):
        if not self.caught_up:
            msg_new = Message(msg_type=8)
            self.send(msg_new, "learners")
            time.sleep(1)

    def print_next_message(self, instance):
        if instance[1]+1 in self.total_order[instance[0]]:
            if instance[1]+1 not in self.total_order_sent[instance[0]]:
                print(self.total_order_memory[(instance[0], instance[1]+1)].v_val, flush=True)
                self.total_order_sent[instance[0]].append(instance[1])
                self.print_order.append(instance)
                self.print_next_message((instance[0], instance[1]+1))

    def read(self):
        while True:
            msg = self.receive()
            if msg.type == 6:
                # print('Type 6')
                if self.caught_up:
                    if msg.instance[0] not in self.total_order.keys():
                        self.total_order[msg.instance[0]] = []
                        self.total_order[msg.instance[0]].append(msg.instance[1])
                        self.total_order_sent[msg.instance[0]] = []
                    else:
                        self.total_order[msg.instance[0]].append(msg.instance[1])
                    self.total_order_memory[msg.instance] = msg.v_val
                    # print(msg.instance[1])
                    if ((msg.instance[1]-1) in self.total_order_sent[msg.instance[0]]) or msg.instance[1] == 0:
                        self.instances[msg.instance] = msg.v_val
                        print(msg.v_val, flush=True)
                        self.total_order_sent[msg.instance[0]].append(msg.instance[1])
                        self.print_order.append(msg.instance)
                        self.print_next_message(msg.instance)

                else:
                    self.temporary_print_order.append(msg.instance)
                    self.total_order_memory[msg.instance] = msg.v_val

            if msg.type == 8:
                #print('Type8')
                msg_new = Message(msg_type=9, total_order=self.print_order, msg_memory=self.total_order_memory)
                self.send(msg_new, "learners")
            if msg.type == 9 and not self.caught_up:
                self.print_order = msg.total_order
                self.total_order_memory = msg.msg_memory
                for instance in self.print_order:
                    if instance[0] not in self.total_order.keys():
                        self.total_order[instance[0]] = []
                        self.total_order[instance[0]].append(instance[1])
                        self.total_order_sent[instance[0]] = []
                    else:
                        self.total_order[instance[0]].append(instance[1])
                    # print(msg.instance[1])
                    if ((instance[1]-1) in self.total_order_sent[instance[0]]) or instance[1] == 0:
                        print(self.total_order_memory[instance], flush=True)
                        self.total_order_sent[instance[0]].append(instance[1])

                for instance in self.temporary_print_order:
                    if instance[0] not in self.total_order.keys():
                        self.total_order[instance[0]] = []
                        self.total_order[instance[0]].append(instance[1])
                        self.total_order_sent[instance[0]] = []
                    else:
                        self.total_order[instance[0]].append(instance[1])
                    # print(msg.instance[1])
                    if ((instance[1] - 1) in self.total_order_sent[instance[0]]) or instance[1] == 0:
                        print(self.total_order_memory[instance], flush=True)
                        self.total_order_sent[instance[0]].append(instance[1])
                        self.print_order.append(msg.instance)
                        self.print_next_message(msg.instance)

                self.caught_up = True
                #print(self.caught_up)


if __name__ == '__main__':
    args = parser.parse_args()
    learner = Learner(args.id, args.config)
    learner.read()