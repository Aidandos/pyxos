import argparse
from threading import Thread
import time

from role import Role
from message import Message

parser = argparse.ArgumentParser(description='Client')
parser.add_argument('--id', default=1, type=int)
parser.add_argument('--config', default='', type=str, metavar='PATH',
                    help='path to config')


class Learner(Role):
    def __init__(self, iid, configpath):
        super(Learner, self).__init__('learners', iid, configpath)
        self.instances = {}
        self.caught_up = False

        self.send_catch_up_thread = Thread(target=self.send_catch_up)
        self.send_catch_up_thread.start()

        self.total_order = []
        self.msg_memory = {}

        self.temporary_order = []
        self.temporary_msg_memory = {}

    def send_catch_up(self):
        if not self.caught_up:
            msg_new = Message(msg_type=8)
            self.send(msg_new, "learners")
            time.sleep(0.1)

    def read(self):
        while True:
            msg = self.receive()
            if msg.type == 6:
                # print('Type 6')
                if self.caught_up:
                    self.instances[msg.instance] = msg.v_val
                    print(msg.v_val, flush=True)
                    self.total_order.append(msg.instance)
                    self.msg_memory[msg.instance] = msg.v_val
                else:
                    self.temporary_order.append(msg.instance)
                    self.msg_memory[msg.instance] = msg.v_val

            if msg.type == 8:
                msg_new = Message(msg_type=9, total_order=self.total_order,msg_memory=self.msg_memory)
                self.send(msg_new, "learners")
            if msg.type == 9 and not self.caught_up:
                self.total_order = msg.total_order
                self.msg_memory = msg.msg_memory
                for message in self.total_order:
                    print(self.msg_memory[message], flush=True)
                self.caught_up = True


if __name__ == '__main__':
    args = parser.parse_args()
    learner = Learner(args.id, args.config)
    learner.read()