import unittest 
import xmlrpclib

class ClientTest(unittest.TestCase):
    """docstring for ClientTest"""
    def setUp(self):
       self.proxy = xmlrpclib.ServerProxy("http://localhost:8000")
       self.serverproxy = xmlrpclib.ServerProxy("http://localhost:8080")

    def test_updateScore(self):
        self.proxy.pushUpdate((0, 0, False))

    def test_register(self):
            self.assertTrue(self.serverproxy.registerClient("","Curling"))
           
    def test_deRegister(self):
            self.assertTrue( self.serverproxy.deRegisterClient("","Curling") )
    
    def test_getMedalTally(self):
        r = self.serverproxy.getMedalTally("Gauls")
        self.assertEqual(type(r), list)

    def test_getScores(self):
        r  = self.serverproxy.getScore("Curling")
        self.assertEqual(type(r), list)

    def test_IncrementMedalTally(self):
        self.assertTrue( self.serverproxy.incrementMedalTally("Gauls", "Gold"))
    
    def test_setScore(self):
			 self.assertTrue( self.serverproxy.setScore("Curling",[int(0), int(0), False]) )  

if __name__ == "__main__":
    unittest.main()
