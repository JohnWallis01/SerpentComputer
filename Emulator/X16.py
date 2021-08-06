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
RegA = np.uint16(1)
RegB = np.uint16(1)
Main_Reg = np.uint16(0)
Jump_Buffer = np.uint16(65535)
Counter = np.uint16(65535)  # will have to see about this one
RAM = np.zeros(65535, dtype=np.uint16)
RamAddr = np.uint16(0)
Flags = [0, 0]
Halting = False
Stack_Pointer = np.uint16(32767)
# instructions


def SUM():
    global Flags
    if int(RegA) + int(RegB) > 65535:
        Flags[0] = 1
    else:
        Flags[0] = 0
    return RegA + RegB


def SUB():
    global Flags
    if RegA > RegB:
        Flags[0] = 1
    else:
        Flags[0] = 0
    return RegA - RegB


def AIN():
    global RegA
    RegA = Main_Reg
    return np.uint16(0)


def AOT():
    return RegA


def BIN():
    global RegB
    RegB = Main_Reg
    return np.uint16(0)


def BOT():
    return RegB


def DSP():
    print(Main_Reg)
    return np.uint16(0)


def JBI():
    global Jump_Buffer
    Jump_Buffer = Main_Reg
    return np.uint16(0)


def JMP():
    global Counter
    Counter = Jump_Buffer
    return np.uint16(0)


def JPE():
    global Counter
    if Flags[1] == 1:
        Counter = Jump_Buffer
    return np.uint16(0)


def JPC():
    global Counter
    if Flags[0] == 1:
        Counter = Jump_Buffer
    return np.uint16(0)


def HLT():
    global Halting
    Halting = True
    return 0


def STC(constant):
    return np.uint16(int(constant, 2))


def MEN():
    global RAM
    RAM[RamAddr] = Main_Reg
    return np.uint16(0)


def MEO():
    return RAM[RamAddr]


def SMA():
    global RamAddr
    RamAddr = Main_Reg
    return np.uint16(0)


def FLF():
    return np.uint16(0)


def FLT():
    return np.unint8(255)


def NOP():
    return np.uint16(0)


def Amm():
    return RegA - np.uint16(1)


def NTA():
    return ~RegA


def NTB():
    return ~RegB


def XOR():
    return RegA ^ RegB


def AND():
    return RegA & RegB


def ORR():
    return RegA | RegB


def LSH():
    return RegA << 1


def STK():
    global RAM
    global Stack_Pointer
    RAM[Stack_Pointer] = Main_Reg
    Stack_Pointer += np.uint16(1)
    return np.uint16(0)


def USK():
    global Stack_Pointer
    Stack_Pointer -= np.uint16(1)
    return RAM[Stack_Pointer]


def SSK():
    global Stack_Pointer
    Stack_Pointer = Main_Reg
    return np.uint16(0)


def RSK():
    return Stack_Pointer


# instruction decoders
translator = {"0000000000000000": NOP,
              "0000000010111111": HLT,
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
        Counter += np.uint16(1)
        ModuleOutput = decode(instructions[Counter])
        Main_Reg = ModuleOutput
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
