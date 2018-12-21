import argparse

from role import Role

parser = argparse.ArgumentParser(description='Client')
parser.add_argument('--id', default=1, type=int)
parser.add_argument('--config', default='', type=str, metavar='PATH',
                    help='path to config')


class Learner(Role):
    def __init__(self, iid, configpath):
        super(Learner, self).__init__('learners', iid, configpath)
        self.state = 0
        #print(configpath)

    def read(self):
        while True:
            msg = self.receive()
            self.state = int(msg.message) + 1
            #self.send(msg, "pro")
            print(self.state)


if __name__ == '__main__':
    args = parser.parse_args()
    learner = Learner(args.id, args.config)
    learner.read()