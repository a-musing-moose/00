import pybonjour
import zmq
import time
from bson import BSON

context = zmq.Context()
socket = context.socket(zmq.REP)
port = socket.bind_to_random_port("tcp://*")
print "Bound to port %d" % port

sdRef = pybonjour.DNSServiceRegister(name = 'Responder',
                                     regtype = '_00._tcp',
                                     port = port)

try:
    try:
        while True:
            message = BSON.decode(BSON(socket.recv()))
            print "Received request %s" % message
            time.sleep (1) # Do some 'work'
            data = {
                'msg': message['msg'][::-1]
            }
            socket.send(BSON.encode(data))
    except KeyboardInterrupt:
        pass
finally:
    sdRef.close()