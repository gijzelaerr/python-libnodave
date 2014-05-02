import os
import ctypes
from libnodave.types import DaveOSserialType

#locate the acutal location so we will later find the
#libnodave-libs
APPDIR = os.path.dirname(os.path.abspath(__file__))


def init_dll():
    """
    initiate the os depending dll-File
    set argtypes and resttypes for used functions
    """

    if os.name == 'nt':
        DLL_LOC = os.path.join(APPDIR, 'libnodave', 'win', 'libnodave.dll')
    elif os.name == 'posix':
        DLL_LOC = 'libnodave.so'
    else:
        print 'only win and linux supportet yet'
    if os.name == 'nt':
        dave = ctypes.windll.LoadLibrary(DLL_LOC)
    else:
        dave = ctypes.cdll.LoadLibrary(DLL_LOC)

    dave.setPort.restype = ctypes.c_int
    dave.setPort.argtypes = [ctypes.c_char_p,
                                  ctypes.c_char_p,
                                  ctypes.c_char]

    dave.daveNewInterface.restype = ctypes.c_void_p
    dave.daveNewInterface.argtypes = [DaveOSserialType,
                                           ctypes.c_char_p,
                                           ctypes.c_int,
                                           ctypes.c_int,
                                           ctypes.c_int]

    dave.openSocket.restype = ctypes.c_int
    dave.openSocket.argtypes = [
                                           ctypes.c_int,
                                           ctypes.c_char_p,
                                    ]

    dave.daveSetDebug.restype = ctypes.c_void_p
    dave.daveSetDebug.argtypes = [ ctypes.c_int ]



    dave.daveInitAdapter.restype = ctypes.c_void_p
    dave.daveInitAdapter.argtypes = [ctypes.c_void_p]

    dave.daveNewConnection.restype = ctypes.c_void_p
    dave.daveNewConnection.argtypes = [ctypes.c_void_p,
                                            ctypes.c_int,
                                            ctypes.c_int,
                                            ctypes.c_int]

    dave.daveStop.restype = ctypes.c_int
    dave.daveStop.argtypes = [ctypes.c_void_p]

    dave.daveConnectPLC.restype = ctypes.c_int
    dave.daveConnectPLC.argtypes = [ctypes.c_void_p]

    dave.daveSetTimeout.restype = ctypes.c_void_p
    dave.daveSetTimeout.argtypes = [ctypes.c_void_p,
                                         ctypes.c_int]

    dave.daveGetU8.restype = ctypes.c_int
    dave.daveGetU8.argtypes = [ctypes.c_void_p]

    dave.daveDisconnectPLC.restype = ctypes.c_int
    dave.daveDisconnectPLC.argtypes = [ctypes.c_void_p]

    dave.daveFree.restype = None
    dave.daveFree.argtypes = [ctypes.c_void_p]

    dave.daveDisconnectAdapter.restype = ctypes.c_int
    dave.daveDisconnectAdapter.argtypes = [ctypes.c_void_p]

    dave.daveReadBytes.restype = ctypes.c_int
    dave.daveReadBytes.argtypes = [ctypes.c_void_p,
                                        ctypes.c_int,
                                        ctypes.c_int,
                                        ctypes.c_int,
                                        ctypes.c_int,
                                        ctypes.c_void_p]

    dave.daveGetCounterValue.restype = ctypes.c_int
    dave.daveGetCounterValue.argtypes = [ctypes.c_void_p,
                                              ctypes.c_int,
                                              ctypes.c_int,
                                              ctypes.c_int,
                                              ctypes.c_int,
                                              ctypes.c_void_p]

    dave.daveWriteBytes.restype = ctypes.c_int
    dave.daveWriteBytes.argtypes = [ctypes.c_void_p,
                                         ctypes.c_int,
                                         ctypes.c_int,
                                         ctypes.c_int,
                                         ctypes.c_int,
                                         ctypes.c_void_p]

    dave.daveStrerror.restype = ctypes.c_char_p
    dave.daveStrerror.argtypes = [ctypes.c_int]

    return dave
