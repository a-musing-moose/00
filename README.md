00
==

00 (Double-O) is a proof of concept app to get zeromq and zeroconf living
together in harmony.

I hope to turn it into a library that enables the building of simple zeromq
services and clients that can then be chained in interesting ways

I have also added pymongo as a requirement. The rational here is that some
services will need to send more than plain text. For example an image
service will either need access to some kind of shared storage or ideally it
should be possible to send binary data across the wire.  There are lots of
different encoding options for this. Pyzmq for example has a pickle encoding
option but the aim using zeromq is the rich variety of language bindings.
Using pickle for example would prevent any other language for being able to use
the system.  I felt that bson would a good balance between flexiblity and
efficiency. 

Once you have installed the relevent packages (see the deployment directory)
you can run the requester and responder in seperate terminals:

> python auto_responder.py

> python auto_requester.py
