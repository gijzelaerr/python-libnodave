# -*- coding: utf-8 -*-
"""
Utility functions
"""
import struct
import atexit
import code
import os
import readline


def tofloat(value):
    return struct.unpack('>f', struct.pack('4B', *value))[0]


def tobigint(value):
    return struct.unpack('>i', struct.pack('4B', *value))[0]


def bitarr_to_int(bitarr):
    """
    eine liste die ein Byte repräsentiert in den passenden
    integer-Wert umrechnen
    """
    str_bitarr = list()
    bitarr.reverse()
    for elem in bitarr:
        str_bitarr.append(str(elem))
    print str_bitarr
    string = ''.join(str_bitarr)
    return int(string,2)


def int_to_bitarr(integer):
    """
    aus einem übergebenen Integer ein 8-stelliges Array erstellen in dem die einzelnen
    Enthaltenen Bits aufzufinden sind
    im bitarr sind die Positionen im array gleich den Werten im Merkerbyte auf der SPS
    m0.0 ist 1. Bit im Merkerbyte (arr[0]
    """
    string = bin(integer)[2:]
    arr = list()

    for bit in xrange(8 - len(string)):
        arr.append(0)

    for bit in string:
        arr.append(int(bit))

    arr.reverse()
    return arr


class HistoryConsole(code.InteractiveConsole):
    """
    Calling this class will launch an interactive console
    """
    def __init__(self, locals=None, filename="<console>",
                 histfile=os.path.expanduser("~/.console-history")):
        code.InteractiveConsole.__init__(self, locals, filename)
        try:
            import readline
        except ImportError:
            pass
        else:
            try:
                import rlcompleter
                readline.set_completer(rlcompleter.Completer(locals).complete)
            except ImportError:
                pass
            readline.parse_and_bind("tab: complete")
        self.init_history(histfile)

    def init_history(self, histfile):
        readline.parse_and_bind("tab: complete")
        if hasattr(readline, "read_history_file"):
            try:
                readline.read_history_file(histfile)
            except IOError:
                pass
            atexit.register(self.save_history, histfile)

    def save_history(self, histfile):
        readline.write_history_file(histfile)