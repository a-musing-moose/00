import select
import pybonjour
import zmq
from bson import BSON

timeout  = 5
resolved = []
services = {}
context = zmq.Context()
con = False

def resolve_callback(sdRef, flags, interfaceIndex, errorCode, fullname, hosttarget, port, txtRecord):
    if errorCode == pybonjour.kDNSServiceErr_NoError:
        resolved.append(True)
        segments = fullname.split('.')
        
        services[segments[0]] = {
            "name": fullname,
            "host": hosttarget,
            "port": port,
        }


def browse_callback(sdRef, flags, interfaceIndex, errorCode, serviceName, regtype, replyDomain):
    if errorCode != pybonjour.kDNSServiceErr_NoError:
        return

    if not (flags & pybonjour.kDNSServiceFlagsAdd):
        del services[serviceName]
        return

    resolve_sdRef = pybonjour.DNSServiceResolve(0, interfaceIndex, serviceName, regtype, replyDomain, resolve_callback)

    try:
        while not resolved:
            ready = select.select([resolve_sdRef], [], [], timeout)
            if resolve_sdRef not in ready[0]:
                print 'Resolve timed out'
                break
            pybonjour.DNSServiceProcessResult(resolve_sdRef)
        else:
            resolved.pop()
    finally:
        resolve_sdRef.close()


browse_sdRef = pybonjour.DNSServiceBrowse(regtype = '_00._tcp',
                                          callBack = browse_callback)

try:
    try:
        while True:
            ready = select.select([browse_sdRef], [], [])
            if browse_sdRef in ready[0]:
                pybonjour.DNSServiceProcessResult(browse_sdRef)
            
            if "Responder" in services and not con:
                print "Connecting to server %s:%d" % (services['Responder']['host'], services['Responder']['port'])
                socket = context.socket(zmq.REQ)
                socket.connect ("tcp://%s:%d" % (services['Responder']['host'], services['Responder']['port']))
                con = True
                
                for request in range (1,10):
                    print "Sending request ", request,"..."
                    data = {
                        'msg': 'Hello',
                    }
                    socket.send (BSON.encode(data))
                    
                    # Get the reply.
                    message = BSON(socket.recv())
                    print "Received reply ", request, BSON.decode(message)
                break;
            
    except KeyboardInterrupt:
        pass
finally:
    browse_sdRef.close()