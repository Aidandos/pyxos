import socket
import struct
import pickle
import toolbox
from message import Message


# https://stackoverflow.com/questions/603852/how-do-you-udp-multicast-in-python

class Role:
    def __init__(self,  roledesc, iid, configpath):
        self.iid = iid
        self.roleDesc = roledesc
        self.config = toolbox.readConfig(configpath)

        mcastGrp = self.config[self.roleDesc][0]
        mcastPort = self.config[self.roleDesc][1]

        self.mcastConfig = (mcastGrp, mcastPort)

        self.sockRcv = self.createSocket(self.mcastConfig)
        self.sockRcv.bind(self.mcastConfig)

        self.sockSnd = self.createSocket(self.mcastConfig)


    def createSocket(self, mcastConfig):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        mreq = struct.pack("4sl", socket.inet_aton(mcastConfig[0]), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        # Set the time-to-live for messages to 1 so they do not go past the
        # local network segment.
        ttl = struct.pack('b', 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

        return sock

    def receive(self):
        while True:
            print(pickle.loads(self.sockRcv.recv(10240)).message)
            #msg = pickle.loads(self.sock.recv(10240))
        # return msg


    def send(self, msg, roleDescRecv):
        assert isinstance(msg, Message)
        msg_p = pickle.dumps(msg)

        if roleDescRecv == self.roleDesc:
            self.sockSnd.sendto(msg_p, self.mcastConfig)
        else:
            mcastGrpRcv = self.config[roleDescRecv][0]
            mcastPortRcv = self.config[roleDescRecv][1]
            mcastConfigRcv = (mcastGrpRcv, mcastPortRcv)

            sock = self.createSocket(mcastConfigRcv)
            sock.sendto(msg_p, mcastConfigRcv)
            sock.close()