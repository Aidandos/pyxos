from role import Role

class Acceptor(Role):
    def __init__(self, roledesc, iid, configpath):
        super(Acceptor, self).__init__("acceptors", iid, configpath)