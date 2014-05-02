import ctypes

daveProtoMPI = 0    # MPI for S7 300/400
daveProtoMPI2 = 1    # MPI for S7 300/400, "Andrew's version" without STX 
daveProtoMPI3 = 2    # MPI for S7 300/400, Step 7 Version, not yet implemented 
daveProtoMPI4 = 3    # MPI for S7 300/400, "Andrew's version" with STX 
daveProtoPPI = 10    # PPI for S7 200
daveProtoAS511 = 20    # S5 programming port protocol 
daveProtoS7online = 50    # use s7onlinx.dll for transport 
daveProtoISOTCP = 122    # ISO over TCP */
daveProtoISOTCP243 = 123 # ISO over TCP with CP243 */
daveProtoISOTCPR = 124   # ISO over TCP with Routing */
daveProtoMPI_IBH = 223   # MPI with IBH NetLink MPI to ethernet gateway */
daveProtoPPI_IBH = 224   # PPI with IBH NetLink PPI to ethernet gateway */
daveProtoNLpro = 230     # MPI with NetLink Pro MPI to ethernet gateway */
daveProtoUserTransport = 255    # Libnodave will pass the PDUs of S7 Communication to user */
                                      # defined call back functions. */

#ProfiBus speed constants:
daveSpeed9k = 0
daveSpeed19k = 1
daveSpeed187k = 2
daveSpeed500k = 3
daveSpeed1500k = 4
daveSpeed45k = 5
daveSpeed93k = 6

#    S7 specific constants:
daveBlockType_OB = '8'
daveBlockType_DB = 'A'
daveBlockType_SDB = 'B'
daveBlockType_FC = 'C'
daveBlockType_SFC = 'D'
daveBlockType_FB = 'E'
daveBlockType_SFB = 'F'

daveS5BlockType_DB = 0x01
daveS5BlockType_SB = 0x02
daveS5BlockType_PB = 0x04
daveS5BlockType_FX = 0x05
daveS5BlockType_FB = 0x08
daveS5BlockType_DX = 0x0C
daveS5BlockType_OB = 0x10


#Use these constants for parameter "area" in daveReadBytes and daveWriteBytes  
daveSysInfo = 0x3      # System info of 200 family 
daveSysFlags = 0x5    # System flags of 200 family 
daveAnaIn = 0x6       # analog inputs of 200 family 
daveAnaOut = 0x7      # analog outputs of 200 family 

daveP = 0x80           # direct peripheral access 
daveInputs = 0x81    
daveOutputs = 0x82    
daveFlags = 0x83
daveDB = 0x84          # data blocks 
daveDI = 0x85          # instance data blocks 
daveLocal = 0x86       # not tested 
daveV = 0x87           # don't know what it is 
daveCounter = 28       # S7 counters 
daveTimer = 29         # S7 timers 
daveCounter200 = 30    # IEC counters (200 family) 
daveTimer200 = 31      # IEC timers (200 family) 
daveSysDataS5 = 0x86   # system data area ? 
daveRawMemoryS5 = 0    # just the raw memory 


buffer_size = 65536
buffer_type = ctypes.c_ubyte * buffer_size

    #class to represent a c-struct
class DaveOSserialType(ctypes.Structure):
    _fields_ = [("rfd", ctypes.c_int),
                ("wfd", ctypes.c_int)]



