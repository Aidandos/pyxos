import argparse

from role import Role

parser = argparse.ArgumentParser(description='Client')
parser.add_argument('--id', default=1, type=int)
parser.add_argument('--config', default='', type=str, metavar='PATH',
                    help='path to config')


class Acceptor(Role):
    def __init__(self, iid, configpath):
        super(Acceptor, self).__init__("acceptors", iid, configpath)
        self.state = 0
    def read(self):
        while True:
            msg = self.receive()
            #msg.message += 1
            self.state = int(msg.message) + 1
            self.send(msg, "learners")
            print(self.state)


if __name__ == '__main__':
    args = parser.parse_args()
    acceptor = Acceptor(args.id, args.config)
    acceptor.read()
