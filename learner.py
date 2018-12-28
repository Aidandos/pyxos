import argparse
from threading import Thread

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

        self.catch_up_thread = Thread(target=self.catch_up)

    def read(self):
        while True:
            msg = self.receive()

            if msg.type == 6:
                # print('Type 6')
                self.instances[msg.instance] = msg.v_val
                print(msg.v_val, flush=True)


if __name__ == '__main__':
    args = parser.parse_args()
    learner = Learner(args.id, args.config)
    learner.read()