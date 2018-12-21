import socket
import struct
import pickle
import sys
import message
import role

"""multicast_group = '224.3.29.71'
server_address =('',10000)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(server_address)

group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Receive/respond loop
while True:
    print(sys.stderr, '\nwaiting to receive message')
    data, address = sock.recvfrom(1024)
    print(sys.stderr, 'received %s bytes from %s' % (len(data), address))
    print( sys.stderr, data)

    print(sys.stderr, 'sending acknowledgement to', address)
    sock.sendto(b'ack', address)"""

# MCAST_GRP = '224.1.1.1'
# MCAST_PORT = 5007
# IS_ALL_GROUPS = True
#
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
# sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
# if IS_ALL_GROUPS:
#     # on this port, receives ALL multicast groups
#     sock.bind(('', MCAST_PORT))
# else:
#     # on this port, listen ONLY to MCAST_GRP
#     sock.bind((MCAST_GRP, MCAST_PORT))
# mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
#
# sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
#
# while True:
#   print(pickle.loads(sock.recv(10240)).message)


roledesc="learners"
configpath='config.txt'
msg = message.Message("robot")
agent = role.Role(roledesc, configpath)

agent.receive()