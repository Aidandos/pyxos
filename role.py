import pickle
import toolbox
from message import Message
from socket_utils import createSocket

# https://stackoverflow.com/questions/603852/how-do-you-udp-multicast-in-python


class Role:
    def __init__(self,  roledesc, iid, configpath):
        print(configpath)
        self.iid = iid
        self.roleDesc = roledesc

        self.c_rnd = 0
        self.c_val = 0
        self.rnd = 0
        self.v_rnd = 0
        self.v_val = 0

        self.config = toolbox.parse_cfg(configpath)


        mcastGrp = self.config[self.roleDesc][0]
        mcastPort = self.config[self.roleDesc][1]

        self.mcastConfig = (mcastGrp, mcastPort)

        self.sockRcv = createSocket(self.mcastConfig)
        self.sockRcv.bind(self.mcastConfig)

        self.sockSnd = createSocket(self.mcastConfig)

    def receive(self):
        while True:
            # print(pickle.loads(self.sockRcv.recv(10240)).message)
            msg = pickle.loads(self.sockRcv.recv(10240))
            return msg

    def send(self, msg, roleDescRecv):
        assert isinstance(msg, Message)
        msg_p = pickle.dumps(msg)

        if roleDescRecv == self.roleDesc:
            self.sockSnd.sendto(msg_p, self.mcastConfig)
        else:
            mcastGrpRcv = self.config[roleDescRecv][0]
            mcastPortRcv = self.config[roleDescRecv][1]
            mcastConfigRcv = (mcastGrpRcv, mcastPortRcv)

            sock = createSocket(mcastConfigRcv)
            sock.sendto(msg_p, mcastConfigRcv)
            sock.close()