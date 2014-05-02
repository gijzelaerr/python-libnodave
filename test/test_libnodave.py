import unittest
import logging
import libnodave.lib

logging.basicConfig(level=logging.DEBUG)


class TestLibNoDave(unittest.TestCase):
    def setUp(self):
        libnodave.lib.init_dll()

    def testLibNoDave(self):
        pass