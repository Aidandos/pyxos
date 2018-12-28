import argparse
from threading import Thread
import time

from message import Message

from role import Role

parser = argparse.ArgumentParser(description='Client')
parser.add_argument('--id', default=1, type=int)
parser.add_argument('--config', default='', type=str, metavar='PATH',
                    help='path to config')


class Proposer(Role):
    def __init__(self, iid, configpath):
        super(Proposer, self).__init__("proposers", iid, configpath)
        self.v = {}
        self.c_rnd = {}
        self.c_val = {}

        self.quorum1B = {}
        self.Reached1B = {}
        self.quorum2B = {}
        self.Reached2B = {}

        self.quorum_length = 2

        self.k = {}
        self.V = {}
        self.v_val = {}
        self.potential_v = {}

        self.prop_iid = iid
        self.current_leader = 0
        self.cardiac_arrest_threshold = 0.5
        self.potential_leaders = []

        self.heart = Thread(target=self.beat_heart, daemon=True)
        self.heart.start()

        self.stethoscope = Thread(target=self.check_heartbeat_leader)
        self.stethoscope.start()

    # https://stackoverflow.com/questions/29769332/how-to-create-a-background-threaded-on-interval-function-call-in-python
    def beat_heart(self):
        while True:
            msg_new = Message(msg_type=7, prop_id=self.prop_iid, current_leader=self.current_leader)
            self.send(msg_new, "proposers")
            time.sleep(0.1)

    def check_heartbeat_leader(self):
        while True:
            time.sleep(0.2)
            self.potential_leaders = []
            time.sleep(self.cardiac_arrest_threshold)
            lowest = sorted(self.potential_leaders)[0]
            if lowest != self.current_leader:
                self.current_leader = lowest

    def read(self):
        while True:
            msg = self.receive()

            if msg.type == 7:
                # print('Type 7')
                self.potential_leaders.append(msg.prop_id)
                # print('current leader',self.current_leader)
                # print('me', self.prop_iid)

            if not self.current_leader == self.prop_iid:
                continue

            if msg.instance not in self.v.keys():
                self.v[msg.instance] = {}
                self.c_rnd[msg.instance] = {}
                self.c_rnd[msg.instance]['most_current'] = 0
                self.c_val[msg.instance] = {}
                self.quorum1B[msg.instance] = {}
                self.quorum2B[msg.instance] = {}
                self.Reached1B[msg.instance] = {}
                self.Reached2B[msg.instance] = {}
                self.k[msg.instance] = {}
                self.V[msg.instance] = {}
                self.v_val[msg.instance] = {}
                self.potential_v[msg.instance] = {}

            if msg.type == 1:
                # print('Type 1')

                self.v[msg.instance][msg.iid] = msg.message

                if msg.iid not in self.c_rnd[msg.instance].keys():
                    self.c_rnd[msg.instance]['most_current'] += 1
                    self.c_rnd[msg.instance][msg.iid] = self.c_rnd[msg.instance]['most_current']

                self.Reached1B[msg.instance][msg.iid] = False
                self.Reached2B[msg.instance][msg.iid] = False

                msg_new = Message(message=msg.message, msg_type=2, c_rnd=self.c_rnd[msg.instance][msg.iid],
                                  iid=msg.iid, instance=msg.instance)

                self.send(msg_new, "acceptors")
            elif msg.type == 3:
                # print('Type 3')
                if self.c_rnd[msg.instance][msg.iid] == msg.rnd:
                    if msg.iid not in self.quorum1B[msg.instance].keys():
                        self.quorum1B[msg.instance][msg.iid] = [msg]
                    else:
                        self.quorum1B[msg.instance][msg.iid].append(msg)
                    if len(self.quorum1B[msg.instance][msg.iid]) >= self.quorum_length \
                            and not self.Reached1B[msg.instance][msg.iid]:
                        # print('Quorum 1B reached')
                        self.k[msg.instance][msg.iid] = 0
                        self.Reached1B[msg.instance][msg.iid] = True
                        for msg in self.quorum1B[msg.instance][msg.iid]:
                            if msg.v_rnd >= self.k[msg.instance][msg.iid]:
                                self.k[msg.instance][msg.iid] = msg.v_rnd
                                self.potential_v[msg.instance][msg.iid] = msg.v_val
                        if self.k[msg.instance][msg.iid] == 0:
                            self.c_val[msg.instance][msg.iid] = self.v[msg.instance][msg.iid]
                        else:
                            self.c_val[msg.instance][msg.iid] = self.potential_v[msg.instance][msg.iid]

                        msg_new = Message(msg_type=4, message=msg.message, c_rnd=self.c_rnd[msg.instance][msg.iid],
                                          c_val=self.c_val[msg.instance][msg.iid],
                                          iid=msg.iid, instance=msg.instance)
                        self.send(msg_new, "acceptors")
            elif msg.type == 5:
                # print('Type 5')
                if self.c_rnd[msg.instance][msg.iid] == msg.v_rnd:
                    if msg.iid not in self.quorum2B[msg.instance].keys():
                        self.quorum2B[msg.instance][msg.iid] = [msg]
                    else:
                        self.quorum2B[msg.instance][msg.iid].append(msg)
                    if len(self.quorum2B[msg.instance][msg.iid]) >= self.quorum_length \
                            and not self.Reached2B[msg.instance][msg.iid]:
                        # print('Quorum 2B reached')
                        self.Reached2B[msg.instance][msg.iid] = True
                        if all(msg.v_rnd == self.c_rnd[msg.instance][msg.iid]
                               for msg in self.quorum2B[msg.instance][msg.iid]):
                            msg_new = Message(message=msg.message, msg_type=6,
                                              v_val=self.quorum2B[msg.instance][msg.iid][0].v_val,
                                              iid=msg.iid, instance=msg.instance)
                            self.send(msg_new, "learners")


if __name__ == '__main__':
    args = parser.parse_args()
    proposer = Proposer(args.id, args.config)
    proposer.read()
