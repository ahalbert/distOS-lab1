# http://gumuz.looze.net/

import time
import threading
import SocketServer
from SimpleXMLRPCServer import SimpleXMLRPCServer,SimpleXMLRPCRequestHandler
import xmlrpclib

# Threaded mix-in
class AsyncXMLRPCServer(SocketServer.ThreadingMixIn,SimpleXMLRPCServer): pass 

# Example class to be published
global tally_board
global score_board
global dummy_score_for_an_event
global push_registered_map

global team_name_dict
global medal_type_dict
global event_type_dict
global client_dict

class ReaderWriterLocks:
	def __init__(self):
		self.lock_1 = threading.Lock()
		self.lock_2 = threading.Lock()
		self.lock_3 = threading.Lock()
		self.lock_r = threading.Lock()
		self.lock_w = threading.Lock()
		self.read_count = 0
		self.write_count = 0

class RequestObject:
	sum_val = 0;
	def __init__(self, tb_lock, sb_lock):
		self.tb_lock = tb_lock
		self.sb_lock = sb_lock
		self.p_map_lock = threading.Lock()
	
	def get_team_name_index(self, teamName):
		team_name_index = -1
		print "teamName:"
		print teamName
		if team_name_dict.has_key(teamName): 	
			team_name_index = team_name_dict[teamName]
		return team_name_index

	def get_medal_type_index(self, medalType):
		medal_type_index = -1
		if medal_type_dict.has_key(medalType): 	
			medal_type_index = medal_type_dict[medalType]
		return medal_type_index

	def get_event_type_index(self, eventType):
		event_type_index = -1
		if event_type_dict.has_key(eventType): 	
			event_type_index = event_type_dict[eventType]
		return event_type_index

	def pre_read(self, lock):
		lock.lock_3.acquire()
		lock.lock_r.acquire()
		lock.lock_1.acquire()
		lock.read_count += 1
		if lock.read_count == 1: 
			lock.lock_w.acquire();
		lock.lock_1.release()
		lock.lock_r.release()
		lock.lock_3.release()

	def post_read(self, lock):
		lock.lock_1.acquire()
		lock.read_count -= 1
		if lock.read_count == 0: 
			lock.lock_w.release();
		lock.lock_1.release()

	def pre_write(self, lock):
		lock.lock_2.acquire()
		lock.write_count += 1
		if lock.write_count == 1: 
			lock.lock_r.acquire()
		lock.lock_2.release()

		lock.lock_w.acquire()

	def post_write(self, lock):
		lock.lock_w.release()

		lock.lock_2.acquire()
		lock.write_count -= 1
		if lock.write_count == 0: 
			lock.lock_r.release()
		lock.lock_2.release()

	def incrementMedalTally(self, teamName, medalType):
		self.pre_write(self.tb_lock)

		# write here
		team_name_index = self.get_team_name_index(teamName)
		medal_type_index = self.get_medal_type_index(medalType)

		if team_name_index != -1 and medal_type_index != -1:
			tally_board[medal_type_index][team_name_index] += 1
			tally_num = tally_board[medal_type_index][team_name_index]

		#time.sleep(1)

		self.post_write(self.tb_lock)
		print True
		return True

	def getMedalTally(self, teamName):
		self.pre_read(self.tb_lock)

		# read here
		team_name_index = self.get_team_name_index(teamName)
#		team_name_index =0 

		if team_name_index != -1:
			gold_num = tally_board[0][team_name_index]
			silver_num = tally_board[1][team_name_index]
		else:
			gold_num = -1
			silver_num = -1

	#	time.sleep(3)
		self.post_read(self.tb_lock)

		return (gold_num, silver_num)


	def setScore(self, eventType, score): # score is a list (score_of_Gauls, score_of_Romans, flag_whether_the_event_is_over)
		self.pre_write(self.sb_lock)

		# write here
		event_type_index = self.get_event_type_index(eventType)

#		count = 0
#		for x in score:
#			score_board[event_type_index][count] = x
#			count += 1
		if event_type_index != -1:
			score_board[event_type_index] = score

		# push to the clients
		client_set = push_registered_map[eventType]
		for clientID in client_set :
			self.pushUpdate(clientID)

		self.post_write(self.sb_lock)
		return True

	def getScore(self, eventType):
		self.pre_read(self.sb_lock)

		# read here
		event_type_index = self.get_event_type_index(eventType)

		if event_type_index != -1:
			score = score_board[event_type_index]
		else:
			score = dummy_score_for_an_event; 

		self.post_read(self.sb_lock)

		return score

	def registerClient(self, clientID, eventTypes): # eventTypes is a list of eventType
		self.p_map_lock.acquire()
		connect_flag = True
		if clientID not in client_dict:
			try :
				URL = "http://" + clientID
				client_dict[clientID] = [xmlrpclib.ServerProxy(URL), set()]
			except socket.error, (value,message):
				print "Could not open socket to the server: " + message
				connect_flag = False
			except :
				info = sys.exc_info()
				print "Unexpected exception, cannot connect to the server:", info[0],",",info[1]
				connect_flag = False
			finally :
				if connect_flag :
					for eventType in eventTypes:
						event_type_index = self.get_event_type_index(eventType)
						if event_type_index != -1:
							push_registered_map[event_type_index].add(clientID)
							client_dict[clientID][1].add(eventType)
				self.p_map_lock.release()
				return connect_flag

	def deRegisterClient(self, clientID, eventTypes): # eventTypes is a list of eventType
		self.p_map_lock.acquire()
		if clientID in client_dict:
			for eventType in eventTypes:
				event_type_index = self.get_event_type_index(eventType)
				if event_type_index != -1:
					push_registered_map[event_type_index].remove(clientID)
					client_dict[clientID][1].remove(eventType)
			if len(client_dict[clientID][1]) == 0 :
				del client_dict[clientID]
		self.p_map_lock.release()
		return True

	def pushUpdate(self, clientID):
			try :
				client_dict[clientID].pushUpdata(clientID)
			except socket.error, (value,message):
				print "Could not open socket to the server: " + message
				return
			except :
				info = sys.exc_info()
				print "Unexpected exception, cannot connect to the server:", info[0],",",info[1]
				return

	def add(self, y) :	# for test
		time.sleep(5)
		www = [1,2,3]
		www = (3,5,8)
		print www
		return self.__class__.sum_val
#		self.tb_lock.lock_1.acquire()
#		self.__class__.sum_val += y
#		result = self.__class__.sum_val
#		print result
#		time.sleep(5)
#		self.tb_lock.lock_1.release()
#		return result

if __name__ == "__main__":
	tally_board = [[0 for x in xrange(2)] for x in xrange(2)]
	score_board = [[0 for x in xrange(3)] for x in xrange(3)]
	client_dict = {}
	dummy_score_for_an_event = [-1 for x in xrange(3)]

	push_registered_map = [set() for index in xrange(3)]

	team_name_dict = {"Gauls":0, "Romans":1}
	medal_type_dict = {"Gold":0, "Silver":1}
	event_type_dict = {"Curling":0, "Skating":1, "Skiing":2}
	# Instantiate and bind to localhost:8080
	server = AsyncXMLRPCServer(('', 8080), SimpleXMLRPCRequestHandler)

	# Register example object instance
	# tb_lock = threading.Lock();
	# sb_lock = threading.Lock();

	server.register_instance(RequestObject(ReaderWriterLocks(), ReaderWriterLocks()))

	# run!
	server.serve_forever()
