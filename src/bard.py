import threading
import time
import random
import copy

tally={"Gaul":(0,0,0), "Rome":(0,0,0)}
score = (0,0)

class Bard(threading.Thread):
    """docstring for Bard"""
    def __init__(self, mode):
        threading.Thread.__init__(self)
        self.mode = mode

    def run(self):
        if self.mode == 0:
            self.changeMedalTally()
        if self.mode == 1:
            self.updateScore()
        else:
            self.server()
            

    def server():
        server = SimpleXMLRPCServer(("localhost", 8001))
        server.register_function(get_tally, "get_tally")
        server.register_function(get_score, "get_score")
        server.serve_forever()

    def get_score(self):
        global score
        lock.acquire()
        s = copy.copy(score)
        lock.release()
        return s

    def get_tally(self):
        global tally
        lock.acquire()
        t = copy.copy(score)
        lock.release()
        return t

    def updateScore():
        pass
        
    def changeMedalTally(self):
        global tally
        try:
            while True: 
                time.sleep(5)
                lock.acquire()
                print tally
                if random.random() >= .75:
                    medal_type = random.randrange(0,3)
                    team = random.randrange(1,3)
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
                    lock.release()
        except KeyboardInterrupt:
            print "hello"
            return

lock = threading.Lock()
tallythread = Bard(0)
tallythread.run()
