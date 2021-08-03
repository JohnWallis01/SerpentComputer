import numpy as np
import time as time
#reads the compiled binary
progfile = input("run .\\")
with open("..\\SASM\\"+progfile, "r") as f:
    lines = f.read()
instructions = lines.split()

#initialises the systems
RegA = np.uint8(1)
RegB = np.uint8(1)
Main_Reg = np.uint8(0)
Jump_Buffer = np.uint8(255)
Counter = np.uint8(255) # will have to see about this one
RAM = np.zeros(256, dtype=np.uint8)
RamAddr = np.uint8(0)
Flags = [0,0]
Halting = False
#instructions

def SUM():
    global Flags
    if int(RegA) + int(RegB) > 255:
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
    return np.uint8(0)

def AOT():
    return RegA

def BIN():
    global RegB
    RegB = Main_Reg
    return np.uint8(0)

def BOT():
    return RegB

def DSP():
    print(Main_Reg)
    return np.uint8(0)


def JBI():
    global Jump_Buffer
    Jump_Buffer = Main_Reg
    return np.uint8(0)

def JMP():
    global Counter
    Counter = Jump_Buffer
    return np.uint8(0)

def JPE():
    global Counter
    if Flags[1] == 1:
        Counter = Jump_Buffer
    return np.uint8(0)

def JPC():
    global Counter
    if Flags[0] == 1:
        Counter = Jump_Buffer
    return np.uint8(0)


def HLT():
    global Halting
    Halting = True
    return 0

def STC(constant):

     return np.uint8(int(constant, 2))
def MEN():
    global RAM
    RAM[RamAddr] = Main_Reg
    return np.uint8(0)

def MEO():
    return RAM[RamAddr]

def SMA():
    global RamAddr
    RamAddr = Main_Reg
    return np.uint8(0)


#instruction decoders
legacy_opcode = { "10101001":"JPE",
                  "10010110":"JPL",
                  "01010110":"JGE"}

translator = {   "00000000": HLT,
                 "10000000": AIN,
                 "10000001": BIN,
                 "10000010": JMP,
                 "10000101": JPE,
                 "10000100": JPC,
                 "10000011": DSP,
                 "10000110": JBI,

                 "11110011":"FLF",
                 "11111100":"FLT",
                 "11001001": SUM,
                 "11010110": SUB,
                 "11111111": AOT,
                 "11111010": BOT,
                 "11001111":"A--",
                 "11110000":"NTA",
                 "11111001":"XOR", #check logic functions
                 "11111110":"AND",
                 "11111011":"ORR",
                 "11011100":"LSH",

                "00110001":MEO,
                "00110000":MEN,
                "00100000":SMA}

literal_translator = {  "0001":STC}

def decode(instruction_byte):
    if instruction_byte in legacy_opcode.keys():
        return legacy_opcode[instruction_byte]()
    elif instruction_byte in translator.keys():
        return translator[instruction_byte]()
    else:
        return literal_translator[instruction_byte[0:4]](instruction_byte[4:8])


def run():
    max_instructions = 1000
    executed = 0
    global Counter
    global Main_Reg
    global Flags
    while not Halting and executed < max_instructions:
        Counter += np.uint8(1)
        ModuleOutput = decode(instructions[Counter])
        Main_Reg = ModuleOutput
        executed += 1
run()