import sys
from role import Role
from message import Message

class Client(Role):
    def __init__(self, roledesc, iid, configpath):
        super(Client, self).__init__("clients", iid, configpath)

    def send_input(self):
        for value in sys.stdin:
            try:
                value = value.strip()
                msg = Message(value)
                self.send(msg, "proposers")

            except KeyboardInterrupt:
                print("Interruption by keyboard")
                raise
            except EOFError:
                print("File is at its end")
                raise

