#!/usr/bin/env python

"""
Python source code - replace this with a description of the code and write the code below this text.
"""

import xmlrpclib
import threading
import socket
import sys
from SimpleXMLRPCServer import SimpleXMLRPCServer

#handle the requests. All the logic of pigs are processed by class_processor
def handle(connection, address):
	processor = class_processor.Processor(connection, address, g_config, g_status)
	processor.Process()

#the server framework. When there is an connection, start a new thread and put all the
#logic to handle function
class ServerFrame(SimpleXMLRPCServer):
	def __init__(self, address):
		self.hostname = address[0]
		self.port = address[1]
    
	def start(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((self.hostname, self.port))
		self.socket.listen(10)
		print "PIG%s on %s:%s starting"%(g_config["peerid"],self.hostname,self.port)
		
		while True:
			conn, address = self.socket.accept()
			thread = threading.Thread(target=handle, args=(conn, address))
			thread.daemon = True
			thread.start()
def is_even(n):
    return n%2 == 0

server = SimpleXMLRPCServer(("localhost", 8000))
print "Listening on port 8000..."
server.register_function(is_even, "is_even")
server.serve_forever()
