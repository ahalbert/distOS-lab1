import threading
import time
import random
import copy
from SimpleXMLRPCServer import SimpleXMLRPCServer 

global tally
tally ={"Gaul":(0,0,0), "Rome":(0,0,0)}
global score 
global tally_exit
tally_exit = False
global score_exit
score_exit = False

class Bard(threading.Thread):
    """docstring for Bard"""
    def __init__(self, mode):
        threading.Thread.__init__(self)
        self.mode = mode

    def run(self):
        if self.mode == "tally":
            self.changeMedalTally()
        if self.mode == "score":
            self.updateScore()
        else:
            self.server()

    def server(self):
        server = SimpleXMLRPCServer(("localhost", 8001))
        print "Server running"
        server.register_function(get_tally, "get_tally")
        server.register_function(getMedalTally, "getMedalTally")
        server.register_function(incrementMedalTally, "incrementMedalTally")
        server.register_function(get_score, "getScore")
        server.register_function(set_score, "setScore")
        server.serve_forever()


    def updateScore(self):
            global score
            print "score running"
            score = (0,0)
            while not score_exit: 
                time.sleep(5)
                if random.random() >= .95:
                    team = random.randrange(1,3)
                    if team == 1:
                        score = (score[0]+1,score[1])
                    else:
                        score = (score[0],score[1]+1)

    def changeMedalTally(self):
        print "tally running"
        while not tally_exit: 
            time.sleep(5)
            lock.acquire()
            if random.random() >= .75:
                medal_type = random.randrange(0,3)
                team = random.randrange(1,3)
                incrementMedalTally(team, medal_type)
            lock.release()

def get_score(sport):
    #lock.acquire()
    s = copy.copy(score)
    #lock.release()
    return s

def set_score(sport, sc):
    score = sc
    return 5

def get_tally():
    #lock.acquire()
    t = copy.copy(tally)
    #lock.release()
    return t

def getMedalTally(team):
    t = copy.copy(tally)
    return t[team]

def incrementMedalTally(team, medal_type):
    if team == "Gaul":
        team = 1
    else:
        team = 0
    if medal_type == "Gold":
        medal_type == 0
    elif medal_type == "Silver":
        medal_type == 1
    else:
        medal_type == 2
    if team == 1:
            if (medal_type == 0):
                tally["Gaul"] = (tally["Gaul"][0]+1, tally["Gaul"][1], tally["Gaul"][2])
            if (medal_type == 1):
                tally["Gaul"] = (tally["Gaul"][0], tally["Gaul"][1]+1, tally["Gaul"][2])
            if (medal_type == 2):
                tally["Gaul"] = (tally["Gaul"][0], tally["Gaul"][1], tally["Gaul"][2]+1)
    else:
            if (medal_type == 0):
                tally["Rome"] = (tally["Rome"][0]+1, tally["Rome"][1], tally["Rome"][2])
            if (medal_type == 1):
                tally["Rome"] = (tally["Rome"][0], tally["Rome"][1]+1, tally["Rome"][2])
            if (medal_type == 2):
                tally["Rome"] = (tally["Rome"][0], tally["Rome"][1], tally["Rome"][2]+1)
    return 5

lock = threading.Lock()
tally_thread = Bard("tally")
tally_thread.start()
score_thread = Bard("score")
score_thread.start()
server_thread = Bard("server")
server_thread.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    tally_exit = True
    score_exit = True
