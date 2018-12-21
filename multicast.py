import socket
import struct
import sys
import pickle
import message
import role


# message = b'very important data'
# multicast_group = ('224.3.29.71',10000)
#
# #Create the datagram socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,socket.IPPROTO_UDP)
#
# # Set the time-to-live for messages to 1 so they do not go past the
# # local network segment.
# ttl = struct.pack('b', 1)
#
# sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
#
# try:
#
#     # Send data to the multicast group
#     print(sys.stderr, 'sending "%s"' % message)
#     sent = sock.sendto(message, multicast_group)
#
#     # Look for responses from all recipients
#     while True:
#         print(sys.stderr, 'waiting to receive')
#         try:
#             data, server = sock.recvfrom(16)
#         except socket.timeout:
#             print(sys.stderr, 'timed out, no more responses')
#             break
#         else:
#             print(sys.stderr, 'received "%s" from %s' % (data, server))
#
# finally:
#     print(sys.stderr, 'closing socket')
#     sock.close()



# MCAST_GRP = '224.1.1.1'
# MCAST_PORT = 5007
#
# msg_p = pickle.dumps(msg)
# # regarding socket.IP_MULTICAST_TTL
# # ---------------------------------
# # for all packets sent, after two hops on the network the packet will not
# # be re-sent/broadcast (see https://www.tldp.org/HOWTO/Multicast-HOWTO-6.html)
# MULTICAST_TTL = 2
#
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
# sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
# sock.sendto(msg_p, (MCAST_GRP, MCAST_PORT))


roledesc="learners"
configpath='config.txt'
msg = message.Message("robot")
agent = role.Role( roledesc, configpath)

agent.send(msg, "learners")