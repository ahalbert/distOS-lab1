#!/usr/bin/env python

"""
Python source code - replace this with a description of the code and write the code below this text.
"""

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import unittest 
import xmlrpclib
import time

class systemTest(unittest.TestCase):
    def setUp(self):
       self.proxy = xmlrpclib.ServerProxy("http://127.0.0.1:8005")
       self.serverproxy = xmlrpclib.ServerProxy("http://localhost:8000")

    def test_register(self):
        st = time.clock()
        self.assertTrue(self.serverproxy.registerClient("","Curling"))
        end = time.clock()
        print end - st
           
    def test_deRegister(self):
        st = time.clock()
        self.assertTrue( self.serverproxy.deRegisterClient("","Curling") )
        end = time.clock()
        print end - st
    
    def test_getMedalTally(self):
        st = time.clock()
        r = self.serverproxy.getMedalTally("Gauls")
        self.assertEqual(type(r), list)
        end = time.clock()
        print end - st

    def test_getScores(self):
        st = time.clock()
        r  = self.serverproxy.getScore("Curling")
        self.assertEqual(type(r), list)
        end = time.clock()
        print end - st

    def test_IncrementMedalTally(self):
        st = time.clock()
        self.assertTrue( self.serverproxy.incrementMedalTally("Gauls", "Gold"))
        end = time.clock()
        print end - st
    
    def test_setScore(self):
        st = time.clock()
        self.assertTrue(self.serverproxy.setScore("Curling",( int(0), int(0), False )) )  
        end = time.clock()
        print end - st

if __name__ == "__main__":
    unittest.main()
