import numpy as np
import time as time
import sys as sys
# this function murders children
import warnings
warnings.filterwarnings("ignore")

# reads the compiled binary

if sys.argv[1].split(".")[1] == "bin":
    try:
        f = open(sys.argv[1], 'r')
        program = f.read()
        f.close()
        instructions = program.split()
    except Exception as e:
        print("Incorrect Input file was specified")
        exit()
if sys.argv[1].split(".")[1] =="hex":
    f = open(sys.argv[1], 'r')
    program = f.read()
    f.close()
    n = 2
    hex = [program[i:i+n] for i in range(0, len(program), n)]
    numerical = [(int(hexed,16)) for hexed in hex[0:-1]]
    n = 8
    instructions  = ['{0:{fill}{width}b}'.format((x + 2**n) % 2**n, fill='0', width=n) for x in numerical]
else:
    print("Incorrect Input file was specified")
    exit()
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
Stack_Pointer = np.int16(65535)

#put instrutions in memory
index = 0
for instruction in instructions:
    instruct = np.int16(int(instruction,2))
    RAM[index] = instruct
    index += 1

#instruct helpers

def Stitch(Low,High):
    return np.int16(int(Low) + int(High)*2**8)



# instructions
def SUM():
    Reset_Flags()
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
    if RegA == RegB:
        Flags[1] = 1
    else:
        Flags[1] = 0
    Main_Reg = RegA - RegB



def AIN():
    Reset_Flags()
    global RegA
    RegA = Main_Reg


def AOT():
    Reset_Flags()
    global Main_Reg
    Main_Reg = RegA


def BIN():
    Reset_Flags()
    global RegB
    RegB = Main_Reg


def BOT():
    Reset_Flags()
    global Main_Reg
    Main_Reg = RegB


def DSP():
    Reset_Flags()
    print(Main_Reg)


def JBI():
    Reset_Flags()
    global Jump_Buffer_Low
    Jump_Buffer_Low = Main_Reg


def JMP():
    Reset_Flags()
    global Counter
    Counter = Stitch(Jump_Buffer_Low, Jump_Buffer_High)


def JPE():
    global Counter
    if Flags[1] == 1:
        Counter = Stitch(Jump_Buffer_Low, Jump_Buffer_High)


def JPC():
    global Counter
    if Flags[0] == 1:
        Counter = Stitch(Jump_Buffer_Low, Jump_Buffer_High)


def STC(constant):
    Reset_Flags()
    global Main_Reg
    Main_Reg = np.int8(int(constant, 2))


def MEN():
    Reset_Flags()
    global RAM
    RAM[Stitch(RamAddrLow, RamAddrHigh)] = Main_Reg


def MEO():
    Reset_Flags()
    global Main_Reg
    Main_Reg = RAM[Stitch(RamAddrLow, RamAddrHigh)]


def SMA():
    Reset_Flags()
    global RamAddrLow
    RamAddrLow = Main_Reg


def FLF():
    Reset_Flags()
    global Main_Reg
    Main_Reg = np.int8(0)


def FLT():
    Reset_Flags()
    global Main_Reg
    Main_Reg = np.unint8(255)


def NOP():
    Reset_Flags()
    pass

def Amm():
    global Flags
    if RegA == np.int8(0):
        Flags[1] = 1
    else:
        Flags[1] = 0
    Flags[0] = 1
    Main_Reg = RegA - np.int8(1)


def NTA():
    Reset_Flags()
    global Main_Reg
    Main_Reg = ~RegA


def NTB():
    Reset_Flags()
    global Main_Reg
    Main_Reg = ~RegB


def XOR():
    Reset_Flags()
    global Main_Reg
    Main_Reg = RegA ^ RegB


def AND():
    Reset_Flags()
    global Main_Reg
    Main_Reg = RegA & RegB


def ORR():
    Reset_Flags()
    global Main_Reg
    Main_Reg = RegA | RegB


def LSH():
    Reset_Flags()
    global Main_Reg
    Main_Reg = RegA << 1

def SMAH():
    Reset_Flags()
    global RamAddrHigh
    RamAddrHigh = Main_Reg

def JBHI():
    Reset_Flags()
    global Jump_Buffer_High
    Jump_Buffer_High = Main_Reg


def STK():
    Reset_Flags()
    global RAM
    global Stack_Pointer
    RAM[Stack_Pointer] = Main_Reg
    Stack_Pointer -= np.int16(1)


def USK():
    Reset_Flags()
    global Stack_Pointer
    global Main_Reg
    Stack_Pointer += np.int16(1)
    Main_Reg = RAM[Stack_Pointer]


#instruction decoders

translator = {"11111111": NOP,
              "10000000": AIN,
              "10000001": BIN,
              "10000010": JMP,
              "10000101": JPE,
              "10000100": JPC,
              "10000011": DSP,
              "10000110": JBI,
              "10000111": JBHI,

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

              "10110001": MEO,
              "10110000": MEN,
              "10100000": SMA,
              "10100001": SMAH,

              "10110010": STK,
              "10110011": USK,

              }

literal_translator = {"0": STC}

#other helpers


def Reset_Flags():
    global Flags
    Flags[0] = 0
    Flags[1] = 1



def decode(instruction_byte):
    if instruction_byte in translator.keys():
        return translator[instruction_byte]()
    else:
        return literal_translator[instruction_byte[0]](instruction_byte[1:8])

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
        # print("c", Counter, "ins", instruct, "main", Main_Reg, "mem addr", RamAddrLow, "value", RAM[RamAddrLow], "Flags", Flags)
        # time.sleep(0.2)


run()
