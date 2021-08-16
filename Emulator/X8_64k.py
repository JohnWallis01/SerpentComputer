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
RegA = np.int8(1)
RegB = np.int8(1)
Main_Reg = np.int8(0)
Jump_Buffer_Low = np.int8(0)
Jump_Buffer_High = np.int8(0)
Counter = np.int16(65535)  # will have to see about this one
RAM = np.zeros(65535, dtype=np.int8)
RamAddrLow = np.int8(0)
RamAddrHigh = np.int8(0)
Flags = [0, 0]
Stack_Pointer = np.int16(-5000)

#put instrutions in memory
index = 0
for instruction in instructions:
    instruct = np.int16(int(instruction,2))
    RAM[index] = instruct
    index += 1

# instructions
def SUM():
    global Main_Reg
    global Flags
    if int(np.uint8(RegA)) + int(np.uint8(RegB)) > 255:
        Flags[0] = 1
    else:
        Flags[0] = 0
    Main_Reg = RegA + RegB


def SUB():
    global Main_Reg
    global Flags
    if RegA > RegB:
        Flags[0] = 1
    else:
        Flags[0] = 0
    Main_Reg = RegA - RegB


def AIN():
    global RegA
    RegA = Main_Reg


def AOT():
    global Main_Reg
    Main_Reg = RegA


def BIN():
    global RegB
    RegB = Main_Reg


def BOT():
    global Main_Reg
    Main_Reg = RegB


def DSP():
    print(Main_Reg)


def JBI():
    global Jump_Buffer_Low
    Jump_Buffer_Low = Main_Reg


def JMP():
    global Counter
    Counter = Jump_Buffer_Low


def JPE():
    global Counter
    if Flags[1] == 1:
        Counter = Jump_Buffer_Low


def JPC():
    global Counter
    if Flags[0] == 1:
        Counter = Jump_Buffer_Low


def STC(constant):
    global Main_Reg
    Main_Reg = np.int8(int(constant, 2))


def MEN():
    global RAM
    RAM[RamAddrLow] = Main_Reg


def MEO():
    global Main_Reg
    Main_Reg = RAM[RamAddrLow]


def SMA():
    global RamAddr
    RamAddr = Main_Reg


def FLF():
    global Main_Reg
    Main_Reg = np.int8(0)


def FLT():
    global Main_Reg
    Main_Reg = np.unint8(255)


def NOP():
    pass

def Amm():
    global Main_Reg
    Main_Reg = RegA - np.int8(1)


def NTA():
    global Main_Reg
    Main_Reg = ~RegA


def NTB():
    global Main_Reg
    Main_Reg = ~RegB


def XOR():
    global Main_Reg
    Main_Reg = RegA ^ RegB


def AND():
    global Main_Reg
    Main_Reg = RegA & RegB


def ORR():
    global Main_Reg
    Main_Reg = RegA | RegB


def LSH():
    global Main_Reg
    Main_Reg = RegA << 1


#instruction decoders

translator = {"00000000": NOP,
              "10000000": AIN,
              "10000001": BIN,
              "10000010": JMP,
              "10000101": JPE,
              "10000100": JPC,
              "10000011": DSP,
              "10000110": JBI,

              "11110011": FLF,
              "11111100": FLT,
              "11001001": SUM,
              "11010110": SUB,
              "11111111": AOT,
              "11111010": BOT,
              "11001111": Amm,
              "11110000": NTA,
              "11110101": NTB,
              "11111001": XOR,  # check logic functions
              "11111110": AND,
              "11111011": ORR,
              "11011100": LSH,

              "00110001": MEO,
              "00110000": MEN,
              "00100000": SMA}

literal_translator = {"0001": STC}


def decode(instruction_byte):
    if instruction_byte in translator.keys():
        return translator[instruction_byte]()
    else:
        return literal_translator[instruction_byte[0:4]](instruction_byte[4:8])

def run():
    max_instructions = 1000
    executed = 0
    global Counter
    global Main_Reg
    global Flags
    while True:
        Counter += np.int8(1)
        x= RAM[Counter]
        n = 8
        instruct = '{0:{fill}{width}b}'.format((x + 2**n) % 2**n, fill='0', width=n)
        decode(instruct)
        executed += 1
        print("c", Counter, "ins", instruct, "main", Main_Reg)
        time.sleep(0.2)


run()
