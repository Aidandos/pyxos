import role.Role as Role

class Learner(Role):
    def __init__(self, roledesc, iid, configpath):
        super(Learner, self).__init__('learners', iid, configpath)