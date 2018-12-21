import argparse

from role import Role

parser = argparse.ArgumentParser(description='Client')
parser.add_argument('--id', default=1, type=int)
parser.add_argument('--config', default='', type=str, metavar='PATH',
                    help='path to config')


class Proposer(Role):
    def __init__(self, iid, configpath):
        super(Proposer, self).__init__("proposers", iid, configpath)
        self.state = 0
    def read(self):
        while True:
            msg = self.receive()
            #msg.message += 1
            self.state = int(msg.message) + 1
            self.send(msg, "acceptors")
            print(self.state)


if __name__ == '__main__':
    args = parser.parse_args()
    proposer = Proposer(args.id, args.config)
    proposer.read()
