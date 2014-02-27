# http://gumuz.looze.net/

import time
import threading
import SocketServer
from SimpleXMLRPCServer import SimpleXMLRPCServer,SimpleXMLRPCRequestHandler

# Threaded mix-in
class AsyncXMLRPCServer(SocketServer.ThreadingMixIn,SimpleXMLRPCServer): pass 

# Example class to be published
class TestObject:
	sum_val = 0;
	def __init__(self, lock):
		self.lock = lock;
	def pow(self, x, y):
		return pow(x, y)

	def add(self, y) :
		self.lock.acquire()
		self.__class__.sum_val += y
		result = self.__class__.sum_val
		print result
		time.sleep(3)
		self.lock.release()
		return result

	def divide(self, x, y):
		return float(x) / float(y)


# Instantiate and bind to localhost:8080
server = AsyncXMLRPCServer(('', 8080), SimpleXMLRPCRequestHandler)

# Register example object instance
lock = threading.Lock();
server.register_instance(TestObject(lock))

# run!
server.serve_forever()
