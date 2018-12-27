import argparse
from message import Message

from role import Role

parser = argparse.ArgumentParser(description='Client')
parser.add_argument('--id', default=1, type=int)
parser.add_argument('--config', default='', type=str, metavar='PATH',
                    help='path to config')


class Proposer(Role):
    def __init__(self, iid, configpath):
        super(Proposer, self).__init__("proposers", iid, configpath)
        self.state = 0
        self.v = 0
        self.c_rnd = 0
        self.c_val = 0
        self.quorum1B = []
        self.Reached1B = False
        self.quorum2B = []
        self.quorum_length = 2
        self.Reached2B = False
        self.k = 0
        self.V = {}
        self.v_val = 0

    def read(self):
        while True:
            msg = self.receive()

            if msg.type == 1:
                print('Type 1')
                self.v = msg.message
                self.c_rnd = self.c_rnd + 1
                msg_new = Message(msg.message, msg_type=2, c_rnd=self.c_rnd)
                self.send(msg_new, "acceptors")
            elif msg.type == 3:
                print('Type 3')
                if self.c_rnd == msg.rnd:
                    self.quorum1B.append(msg)
                    if len(self.quorum1B) >= self.quorum_length and not self.Reached1B:
                        print('Quorum 1B reached')
                        self.Reached1B = True
                        for msg in self.quorum1B:
                            if msg.v_rnd >= self.k:
                                self.k = msg.v_rnd
                                potential_v = msg.v_val
                        if self.k == 0:
                            self.c_val = self.v
                        else:
                            self.c_val = potential_v

                        msg_new = Message(msg.message, msg_type=4, c_rnd=self.c_rnd, c_val=self.c_val)
                        self.send(msg_new, "acceptors")
            elif msg.type == 5:
                print('Type 5')
                if self.c_rnd == msg.v_rnd:
                    self.quorum2B.append(msg)
                    if len(self.quorum2B) >= self.quorum_length and not self.Reached2B:
                        print('Quorum 2B reached')
                        self.Reached2B = True
                        if all(msg.v_rnd == self.c_rnd for msg in self.quorum2B):
                            msg_new = Message(msg.message, msg_type=6, v_val=self.quorum2B[0].v_val)
                            self.send(msg_new, "learners")


if __name__ == '__main__':
    args = parser.parse_args()
    proposer = Proposer(args.id, args.config)
    proposer.read()
