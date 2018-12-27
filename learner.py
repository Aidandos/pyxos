import argparse

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
        # print(configpath)

    def read(self):
        while True:
            msg = self.receive()

            if msg.type == 6:
                print('Type 6')
                self.instances[msg.instance] = msg.v_val
                print(msg.v_val)


if __name__ == '__main__':
    args = parser.parse_args()
    learner = Learner(args.id, args.config)
    learner.read()