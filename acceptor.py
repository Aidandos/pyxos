import argparse

from role import Role
from message import Message

parser = argparse.ArgumentParser(description='Client')
parser.add_argument('--id', default=1, type=int)
parser.add_argument('--config', default='', type=str, metavar='PATH',
                    help='path to config')

'''
Probably the most straightforward script of the whole codebase
'''

class Acceptor(Role):
    def __init__(self, iid, configpath):
        super(Acceptor, self).__init__("acceptors", iid, configpath)
        self.rnd = {}
        self.v_rnd = {}
        self.v_val = {}

    def read(self):
        while True:
            msg = self.receive()
            if msg.instance not in self.rnd.keys():
                self.rnd[msg.instance] = 0
                self.v_rnd[msg.instance] = 0
                self.v_val[msg.instance] = 0

            if msg.type == 2:
                # print('Type 2')
                if msg.c_rnd >= self.rnd[msg.instance]:
                    self.rnd[msg.instance] = msg.c_rnd
                    msg_new = Message(message=msg.message, msg_type=3, rnd=self.rnd[msg.instance],
                                      v_val=self.v_val[msg.instance],
                                      v_rnd=self.v_rnd[msg.instance],
                                      iid=msg.iid, instance=msg.instance)
                    self.send(msg_new, "proposers")
            elif msg.type == 4:
                # print('Type 4')
                if msg.c_rnd >= self.rnd[msg.instance]:
                    self.v_rnd[msg.instance] = msg.c_rnd
                    self.v_val[msg.instance] = msg.c_val
                    msg_new = Message(message=msg.message, msg_type=5, v_rnd=self.v_rnd[msg.instance],
                                      v_val=self.v_val[msg.instance],
                                      iid=msg.iid, instance=msg.instance)
                    self.send(msg_new, "proposers")


if __name__ == '__main__':
    args = parser.parse_args()
    acceptor = Acceptor(args.id, args.config)
    acceptor.read()
