#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python wrapper for libnodave, a PLC communication library
"""
import ctypes
import logging
from libnodave.exceptions import LibDaveException

import libnodave.types
import libnodave.lib
from libnodave.utils import int_to_bitarr

logger = logging.getLogger(__name__)


class Libnodave(object):
    def __init__(self):
        self.fds = libnodave.types.DaveOSserialType()
        self.di = None
        self.dave = libnodave.lib.init_dll()
        self.buffer = ctypes.create_string_buffer(1024)
        self.buffer_p = ctypes.pointer(self.buffer)

    def set_port(self, port, baud='9600', parity='E'):
        """
        set a serial connection port
        """
        self.fds.rfd = self.dave.setPort(port, baud, parity)
        self.fds.wfd = self.fds.rfd

    def open_socket(self, ip, port=102):
        logger.debug("connecting to %s:%s" % (ip, port))
        socket = self.dave.openSocket(port, ip)
        self.fds.rfd = socket
        self.fds.wfd = self.fds.rfd
        
    def new_interface(self, name, localMPI, protocol, speed):
        """
        add a new interface
        """
        msg = "new interface name: %s localMPI: %s protocol: %s speed: %s" % \
              (name, localMPI, protocol, speed)
        logger.debug(msg)
        self.di = self.dave.daveNewInterface(self.fds, name, localMPI, protocol,
                                             speed)
    
    def set_timeout(self, time):
        """
        Set time out value.
        """
        logging.info("setting timeout to %s" % time)
        self.dave.daveSetTimeout(self.di, time)
    
    def init_adapter(self):
        """
        Initialise the adapter
        """
        logger.info("initialising adapter")
        self.dave.daveInitAdapter(self.di)
        
    def connect_plc(self, mpi, rack, slot):
        """
         Connect to the PLC
        """
        logger.info("Connecting to PLC. mpi: %s rack: %s slot: %s" % (mpi,
                    rack, slot))
        self.dc = self.dave.daveNewConnection(self.di, mpi, rack, slot)
        res = self.dave.daveConnectPLC(self.dc)

    def stop(self):
        """
        """
        res = self.dave.daveStop(self.dc)

    def SetDebug(self, level):
        """
        """
        res = self.dave.daveSetDebug(level)


    def disconnect(self):
        """
        disconnect connection to PLC and Adapter
        """
        self.dave.daveDisconnectPLC(self.dc)
        self.dave.daveFree(self.dc)
        self.dave.daveDisconnectAdapter(self.di)
        self.dave.daveFree(self.di)
        return True
        
    def read_bytes(self, area, db, start, length):
        """
        Read len bytes from PLC at location start
        """
        buffer = ctypes.create_string_buffer(length)
        logging.info("reading bytes from area: %s db: %s start: %s len: %s" %
                     (area, db, start, length))
        error = self.dave.daveReadBytes(self.dc, area, db, start, length,
                                         buffer)
        if error:
            msg =self.str_error(error)
            logging.error(msg)
            raise LibDaveException(msg)
        return bytearray(buffer)
    
    def get_counter_value(self, counter_number):
        """
        read a counter from the plc
        """
        self.read_bytes(libnodave.types.daveCounter, 0, 0, 1)
        counters = list()
        for val in xrange(16):
            counters.append(self.dave.daveGetCounterValue(self.dc)) 
        return counters[counter_number]
    
    def get_counters(self):
        """
        Liste mit allen Zählern der S5 auslesen und zurückgeben
        TODO: wird das wirklich gebraucht?
        """
        if self.read_bytes(libnodave.types.daveCounter, 0, 0, 1):
            counters = list()
            for val in xrange(16):
                counters.append(self.dave.daveGetCounterValue(self.dc)) 
            return counters
        return False
    
    def get_marker_byte(self, marker):
        """
        einen merkerbyte auslesen
        rückgabewert ist ein Integer. Sollen die einzelnen Bits untersucht werden
        muss der rückgabewert nach binär konvertiert werden -> bin(result)
        """
        if self.read_bytes(libnodave.types.daveFlags, 0, marker, 1):
            return self.dave.daveGetU8(self.dc)
        return -1
        
    def get_output_byte(self, output):

        if self.read_bytes(libnodave.types.daveOutputs, 0, output, 1):
            return self.dave.daveGetU8(self.dc)
        return -1
    
    def get_marker(self, marker, byte):
        """
        einen bestimmten Merker aus einem Merkerbyte auslesen
        """
        m_byte = self.get_marker_byte(marker)
        if m_byte >= 0:
            byte_arr = int_to_bitarr(m_byte)
            return byte_arr[byte]
        return False
        
    def get_output(self, output, byte):
        """
        einen bestimmten Merker aus einem Merkerbyte auslesen
        """
        m_byte = self.get_output_byte(output)
        if m_byte >= 0:
            byte_arr = int_to_bitarr(m_byte)
            return byte_arr[byte]
        return False

    
    def get_marker_byte_list(self, marker):
        """
        ein Merkerbyte als liste zurückgeben
        get a list with a bits representing all marker from read byte
        """   
        if self.read_bytes(libnodave.types.daveFlags, 0, marker, 1):
            return int_to_bitarr(self.dave.daveGetU8(self.dc))
        return False
    
    def get_marker_byte_dict(self, marker):
        """
        ein Merkerbyte als Dict zurückgeben
        """
        _l = self.get_marker_byte_list(marker)
        print 'libnodave - merkerbyte:', _l
        d = dict()
        for val in xrange(8):
            d[val]= _l[val]
        return d
        
    def write_marker_byte(self, marker, value):
        """
        EXPORTSPEC int DECL2 daveWriteBytes(daveConnection * dc, int area, int DB, int start,
                                            int len, void * buffer);
        ein Merkerbyte in die SPS schreiben
        TODO: anpassen und testen
        """
        buffer = ctypes.c_byte(int(value))
        buffer_p = ctypes.pointer(buffer)
        self.dave.daveWriteBytes(self.dc, libnodave.types.daveFlags, 0, marker,
                                 1, buffer_p)
        
    def write_vm_byte(self, vm, value):
        """
        EXPORTSPEC int DECL2 daveWriteBytes(daveConnection * dc, int area, int DB, int start,
                                            int len, void * buffer);
        ein Merkerbyte in die SPS schreiben
        TODO: anpassen und testen
        """
        buffer = ctypes.c_byte(int(value))
        buffer_p = ctypes.pointer(buffer)
        self.dave.daveWriteBytes(self.dc, libnodave.types.daveDB, 1, vm, 1, buffer_p)
        
    def outputs(self):
        Q1 = self.get_output(0,0)
        Q2 = self.get_output(0,1)
        Q3 = self.get_output(0,2)
        Q4 = self.get_output(0,3)

        print "Padverlichting      : " + str(Q1)
        print "Tuinhuisverlichting : " + str(Q2)
        print "Tuinhuis buiten     : " + str(Q3)
        print "Terrasverlichting   : " + str(Q4)

    def str_error(self, error_code):
        """
        return error string for given error_code
        """
        return self.dave.daveStrerror(error_code)

    def get_float(self):
        result = self.daveGetFloat(self.dave)
        return result
