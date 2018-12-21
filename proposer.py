from role import Role

class Proposer(Role):
    def __init__(self, roledesc, iid, configpath):
        super(Proposer, self).__init__("proposers", iid, configpath)