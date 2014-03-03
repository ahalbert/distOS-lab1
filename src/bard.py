import threading
import time
import random
import copy
from SimpleXMLRPCServer import SimpleXMLRPCServer 
import xmlrpclib

"""
Bard class - Thin client that updates the server when medal tally or score needs to be changed.
"""

global tally_exit
tally_exit = False
global score_exit
score_exit = False

class Bard(threading.Thread):
    """Threads that manage updatescore and updateTally. Inherits threading.Thread methods"""
    def __init__(self, mode):
        threading.Thread.__init__(self)
        self.mode = mode

    def run(self):
        """Overrides threading.run. Launches the proper function based on how the class was init"""
        if self.mode == "tally":
            self.updateTally()
        if self.mode == "score":
            self.updateScore()

    def updateScore(self):
        """
        Updates score to tell if event should end or if score should be updated
        Uses a remote procedure call to update the score
        """
        score = (0,0,False)
        should_end = False
        while not score_exit:
            time.sleep(5)
            team, sport = get_team(), get_sport()
            if random.random >= .99:
                should_end == True
            if random.random >= .8:
                lock.acquire()
                if team == "Gauls":
                    proxy.setScore(sport, (score[1]+1, score[2], should_end))
                else:
                    proxy.setScore(sport, (score[1], score[2]+1, should_end))
                lock.release()

    def updateTally(self):
        """Updates medal tally, incremeninting by making a remote procedure call to the server"""
        while not tally_exit:
            time.sleep(5)
            if random.random >= .75:
                lock.acquire()
                proxy.incrementMedalTally(get_team(), get_medal_type())
                lock.release()

def get_medal_type():
    """Returns a random medal type"""
    num = random.randrange(1,4)
    if num == 1:
        return "Gold"
    if num == 2:
        return "Silver"
    else:
        return "Bronze"


def get_sport():
    """Returns a random sport"""
    num = random.randrange(1,4)
    if num == 1:
        return "Curling"
    if num == 2:
        return "Skating"
    else:
        return "Skiing"

def get_team():
    """Returns a random team"""
    num = random.randrange(1,3)
    if num == 1:
        return "Gauls"
    else:
        return "Romans"

lock = threading.Lock()
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
