#!/usr/bin/env python

"""
Python source code - replace this with a description of the code and write the code below this text.
"""

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import xmlrpclib
import threading
import time
import sys
import socket
from numpy  import *
from numpy.random import *

global s
global index_array
global lock

def handle(index, lock):
	try:
		s = xmlrpclib.ServerProxy('http://localhost:8000')
		result = 0
		if index == 1:
			result = s.incrementMedalTally("Gauls", "Gold")  # Returns 5
		if index == 0:
			result = s.getMedalTally("Gauls")
		if index == 3:
			r_int = randint(0,10, (2))
			result = s.setScore("Skating",[int(r_int[0]), int(r_int[1]), False])  # Returns 5
		if index == 2:
			result = s.getScore("Curling")
		lock.acquire()
		print result
		lock.release()
	except socket.error, (value,message):
		print "Could not open socket: " + message
		return
	except :
		info = sys.exc_info()
		print "Unexpected exception:", info[0],",",info[1]
		return

if __name__ == "__main__":
#	s = xmlrpclib.ServerProxy('http://localhost:8080')
#	s.incrementMedalTally("Gauls", "Gold")  # Returns 5
#	s.incrementMedalTally("Gauls", "Silver")  # Returns 5
#	s.incrementMedalTally("Romans", "Gold")  # Returns 5
#	print s.getMedalTally("Gauls")
#	print s.getMedalTally("Romans")

	index_array = array([1,0,0,0,0,1,0,0,0,1,0,0,0])
	lock = threading.Lock()
	for index in index_array:
		time.sleep(0.1)
		thread = threading.Thread(target=handle, args=(index, lock))
		thread.daemon = True
		thread.start()

	current_thread = threading.currentThread()
	for thread in threading.enumerate():
		if thread != current_thread:
			thread.join()
	# Print list of available methods
	# print s.system.listMethods()
