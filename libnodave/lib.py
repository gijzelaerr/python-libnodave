import ctypes
import platform
from ctypes.util import find_library
from libnodave.types import DaveOSserialType
from libnodave.exceptions import LibNoDaveException


def init_dll(lib_location=None):
    """
    initiate the os depending dll-File
    set argtypes and resttypes for used functions
    """
    lib_location = lib_location or find_library('libnodave')

    if not lib_location:
        msg = "can't find libnodave library. If installed, try running ldconfig"
        raise LibNoDaveException(msg)

    if platform.system() == "Windows":
        dave = ctypes.WinDLL(lib_location)
    else:
        dave = ctypes.cdll.LoadLibrary(lib_location)

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
    dave.openSocket.argtypes = [ctypes.c_int, ctypes.c_char_p]

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
