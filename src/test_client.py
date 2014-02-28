import threading
import SocketServer
import sys
from SimpleXMLRPCServer import SimpleXMLRPCServer,SimpleXMLRPCRequestHandler
#import SimpleXMLRPCServer
import xmlrpclib
import socket
import re

global tally_board
global score_board
#global sb_lock
#global output_lock

def update_score(score):
#	sb_lock.acquire()
	score_board = score
	return True
#	sb_lock.release()

class ServerThread(threading.Thread):
	def __init__(self, host_name, port):
		threading.Thread.__init__(self)

		self.host_name = host_name
		self.port = port

		self.localServer = SimpleXMLRPCServer((host_name, port))
		self.localServer.register_function(update_score, "pushUpadte") #just return a string

	def run(self):
		self.localServer.serve_forever()

class ClientObject:
	def __init__(self, host_name, port):
		self.address = (host_name, port)
		self.options = {"MEDAL": self.get_medal_tally,
				"SCORE": self.get_score,
				"REGI": self.register_events,
				"DE_REGI": self.de_register_events,
				}

	def get_medal_tally(self, s, args):
		team_name = "Gauls"
		if len(args) >= 1:
			team_name = args[0]
		result = s.getMedalTally(team_name)
		tally_board = result
		return result

	def get_score(self, s, args):
		event_type = "Curling"
		if len(args) >= 1:
			event_type = args[0]
		result = s.getScore(event_type)
#		sb_lock.acquire()
		score_board = result
#		sb_lock.release()
		return result

	def register_events(self, s, args):
		event_types = ("Curling")
		if len(args) >= 1:
			event_types = args[0]
		return s.registerClient(self.address[0]+":"+str(self.address[1]), event_types)

	def de_register_events(self, s, args):
		event_types = ("Curling")
		if len(args) >= 1:
			event_types = args[0]
		return s.deRegisterClient(self.address[0]+":"+str(self.address[1]), event_type)

	def usage(self):
		print "Usage: 'COMMAND'"
		print "COMMAND:\n\tMEDAL [TEAMNAME='Gauls']: Get medal number array [gold, silver] for the given team"
		print "\tSCORE [TEAMNAME='Gauls']: Get scores array for the given team" 
		print "\tREGI [LIST OF EVENTTYPES=('Curling')]: Register events for push scores" 
		print "\tDE_REGI [LIST OF EVENTTYPES=('Curling')]: De-register events for push scores"

	def start(self):
		try:
			URL = "http://" + self.address[0] + ":" + str(self.address[1]);
			print URL

			s = xmlrpclib.ServerProxy(URL)
		except socket.error, (value,message):
			print "Could not open socket to the server: " + message
			return
		except :
			info = sys.exc_info()
			print "Unexpected exception, cannot connect to the server:", info[0],",",info[1]
			return
		while True:
			line = raw_input('--> ')
			r = re.split(r'\s+',line)
			r_len = len(r)
			print r
			print "wzd" + str(r_len) + "wzd"
			command = r[0]
		
			if r_len == 1 and '' in r:
				self.usage()
				continue

			if command in self.options:
				print self.options[command](s, r[1:len(r)])

if __name__ == "__main__":
	host_name = "127.0.0.1"
	port = 8000

	remote_host_name = "127.0.0.1"
	remote_port = 8080

	tally_board = [0 for x in xrange(2)]
	score_board = [0 for x in xrange(3)]

#	sb_lock = threading.Lock()
#	output_lock = threading.Lock()

	server = ServerThread(host_name, port)
	server.daemon = True;
	server.start() # The server is now running
	client = ClientObject(remote_host_name, remote_port)
	client.start()

#	while threading.active_count() > 0:
#		time.sleep(0.1)
	server.join(1)
