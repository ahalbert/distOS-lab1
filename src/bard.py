import threading
import time
import random
import copy
from SimpleXMLRPCServer import SimpleXMLRPCServer 
import xmlrpclib

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

    def updateScore(self):
        score = (0,0,False)
        should_end == False
        while not score_exit:
            team, sport = get_team(), get_sport()
            if random.random >= .99:
                should_end == True
            if team == "Romans":
                proxy.setScore(sport, (score[1]+1, score[2], should_end))
            else:
                proxy.setScore(sport, (score[1], score[2]+1, should_end))

    def updateTally(self):
        while not tally_exit:
            time.sleep(5)
            if random.random >= .75:
                proxy.incrementMedalTaly(get_team(), get_medal_type())

def get_medal_type():
    num = random.randrange(1,4)
    if num == 1:
        return "Gold"
    if num == 2:
        return "Silver"
    else:
        return "Bronze"


def get_sport():
    num = random.randrange(1,4)
    if num == 1:
        return "Curling"
    if num == 2:
        return "Skating"
    else:
        return "Skiing"

def get_team():
    num = random.randrange(1,3)
    if num == 1:
        return "Gauls"
    else:
        return "Romans"

proxy = xmlrpclib.ServerProxy("http://localhost:8080") 
tally_thread = Bard("tally")
tally_thread.start()
score_thread = Bard("score")
score_thread.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    tally_exit = True
    score_exit = True
