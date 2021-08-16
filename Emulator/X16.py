import numpy as np
import time as time
import sys as sys
# this function murders children
import warnings
warnings.filterwarnings("ignore")

# reads the compiled binary
try:
    f = open(sys.argv[1], 'r')
    program = f.read()
    f.close()
except Exception as e:
    print("Incorrect Input file was specified")
    exit()

instructions = program.split()

# initialises the systems
RegA = np.int16(1)
RegB = np.int16(1)
Main_Reg = np.int16(0)
Jump_Buffer = np.int16(65535)
Counter = np.int16(65535)  # will have to see about this one
RAM = np.zeros(65535, dtype=np.int16)  # what if we put the code inside the ram
RamAddr = np.int16(0)
Flags = [0, 0]
Halting = False
Stack_Pointer = np.int16(-5000)
# instructions


def SUM():
    global Flags
    if int(np.uint16(RegA)) + int(np.uint16(RegB)) > 65535:
        Flags[0] = 1
    else:
        Flags[0] = 0
    Flags[1] = 0
    return RegA + RegB


def SUB():
    global Flags
    if RegA > RegB:
        Flags[0] = 1
    else:
        Flags[0] = 0
    if RegA == RegB:
        Flags[1] = 1
    else:
        Flags[1] = 0
    return RegA - RegB


def AIN():
    Reset_Flags()
    global RegA
    RegA = Main_Reg
    return np.int16(0)


def AOT():
    Reset_Flags()
    return RegA


def BIN():
    Reset_Flags()
    global RegB
    RegB = Main_Reg
    return np.int16(0)


def BOT():
    Reset_Flags()
    return RegB


def DSP():
    Reset_Flags()
    print(Main_Reg)
    return np.int16(0)


def JBI():
    Reset_Flags()
    global Jump_Buffer
    Jump_Buffer = Main_Reg
    return np.int16(0)


def JMP():
    Reset_Flags()
    global Counter
    Counter = Jump_Buffer
    return np.int16(0)


def JPE():
    global Counter
    if Flags[1] == 1:
        Counter = Jump_Buffer
    Reset_Flags()
    return np.int16(0)


def JPC():
    global Counter
    if Flags[0] == 1:
        Counter = Jump_Buffer
    Reset_Flags()
    return np.int16(0)


def STC(constant):
    Reset_Flags()
    return np.int16(int(constant, 2))


def MEN():
    Reset_Flags()
    global RAM
    RAM[RamAddr] = Main_Reg
    return np.int16(0)


def MEO():
    Reset_Flags()
    return RAM[RamAddr]


def SMA():
    Reset_Flags()
    global RamAddr
    RamAddr = Main_Reg
    return np.int16(0)


def FLF():
    Reset_Flags()
    return np.int16(0)


def FLT():
    Reset_Flags()
    return np.unint8(255)


def NOP():
    Reset_Flags()
    return np.int16(0)


def Amm():
    global Flags
    if RegA == np.int16(0):
        Flags[1] = 1
    else:
        Flags[1] = 0
    Flags[0] = 1
    return RegA - np.int16(1)


def NTA():
    Reset_Flags()
    return ~RegA


def NTB():
    Reset_Flags()
    return ~RegB


def XOR():
    Reset_Flags()
    return RegA ^ RegB


def AND():
    Reset_Flags()
    return RegA & RegB


def ORR():
    Reset_Flags()
    return RegA | RegB


def LSH():
    Reset_Flags()
    return RegA << 1


def STK():
    Reset_Flags()
    global RAM
    global Stack_Pointer
    RAM[Stack_Pointer] = Main_Reg
    Stack_Pointer += np.int16(1)
    return np.int16(0)


def USK():
    Reset_Flags()
    global Stack_Pointer
    Stack_Pointer -= np.int16(1)
    return RAM[Stack_Pointer]


def SSK():
    Reset_Flags()
    global Stack_Pointer
    Stack_Pointer = Main_Reg
    return np.int16(0)


def RSK():
    Reset_Flags()
    return Stack_Pointer


def GPS():
    Reset_Flags()
    return Counter


# other helpers

def Reset_Flags():
    global Flags
    Flags[0] = 0
    Flags[1] = 1


# instruction decoders
translator = {"0000000000000000": NOP,
              "0000000010000000": AIN,
              "0000000010000001": BIN,
              "0000000010000010": JMP,
              "0000000010000101": JPE,
              "0000000010000100": JPC,
              "0000000010000011": DSP,
              "0000000010000110": JBI,

              "0000000011110011": FLF,
              "0000000011111100": FLT,
              "0000000011001001": SUM,
              "0000000011010110": SUB,
              "0000000011111111": AOT,
              "0000000011111010": BOT,
              "0000000011001111": Amm,
              "0000000011110000": NTA,
              "0000000011110101": NTB,
              "0000000011111001": XOR,
              "0000000011111110": AND,
              "0000000011111011": ORR,
              "0000000011011100": LSH,

              "0000000000110001": MEO,
              "0000000000110000": MEN,
              "0000000000100000": SMA,

              "0000000000110010": STK,
              "0000000000110011": USK,
              "0000000000110100": SSK,
              "0000000000110101": RSK
              }

literal_translator = {"1": STC}

# add other ALU fuctions
# implement correct flags


def decode(instruction_byte):
    if instruction_byte in translator.keys():
        return translator[instruction_byte]()
    else:
        return literal_translator[instruction_byte[0]](instruction_byte[1:16])


def run():
    executed = 0
    global Counter
    global Main_Reg
    global Flags
    while not Halting:
        Counter += np.int16(1)
        ModuleOutput = decode(instructions[Counter])
        Main_Reg = ModuleOutput
        # print(Counter, "c", "j", Jump_Buffer, "stk", RAM[Stack_Pointer-3:Stack_Pointer],"main", Main_Reg)
        # time.sleep(0.02)
        executed += 1
        # try:
        #     print(
        #         Counter, translator[instructions[Counter]].__name__, Main_Reg, Flags)
        # except:
        #     print(
        #         Counter, literal_translator[instructions[Counter][0]].__name__, Main_Reg, Flags)
        # if executed > 500:
        #     exit()


run()
