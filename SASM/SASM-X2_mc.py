import sys
legacy_opcode = {"JPE": "10101001",
                 "JPL": "10010110",
                 "JGE": "01010110",}

translator = {  "NOP": "00000000",
                "AIN": "10000000",
                "BIN": "10000001",
                "JMP": "10000010",
                "JPE": "10000101",#unkown if this works
                "JPC": "10000100",#unkown if this works
                "DSP": "10000011",
                "JBI": "10000110",

                "FLF": "11110011",
                "FLT": "11111100",
                "SUM": "11001001",
                "SUB": "11010110",
                "AOT": "11111111",
                "BOT": "11111010",
                "A--": "11001111",
                "NTA": "11110000",
                "XOR": "11111001", #check logic functions
                "AND": "11111110",
                "ORR": "11111011",
                "LSH": "11011100",

                "MEO":"00110001",
                "MEN":"00110000",
                "SMA":"00100000"

}

literal_translator = {  "STC": "0001"}


try:
    f = open(sys.argv[1], 'r')
    program = f.readlines()
    f.close()
except:
    print("No Input file was specified")
    exit()
assembled = []
try:
    for i in program:
        if(i[0:3].upper() in literal_translator):
            assembled.append(literal_translator[i[0:3].upper()] + i[4:8])
        else:
            assembled.append(translator[i[0:3].upper()]) # this needs to be imporved
    print(assembled)
except:
    print("Assembly Failed, Unkown OPCode:")
    print(i)
    exit()
#minecraft command upload assembler
#note that the lever block state is inverted

#435 58 506 --> origin
#each bit increments z by -2 --> this is reversed due to the byte order
#each byte increments x by 3
#/setblock <x> <y> <z> minecraft:lever 6 --> game off(computer on)
#/setblock <x> <y> <z> minecraft:lever 14 --> (game on) (computer off)
y = 58
def McTrue(x,y,z):
    return "Send /setblock " + str(x) + " " + str(y) + " " + str(z) + " minecraft:lever 6{Enter}"
def McFalse(x,y,z):
    return "Send /setblock " + str(x) + " " + str(y) + " " + str(z) + " minecraft:lever 14{Enter}"
mcAssembly = []
x = 435
for i in assembled:
    z = 494
    for k in i:
        if k == "1":
            mcAssembly.append(McTrue(x,y,z))
        else:
            mcAssembly.append(McFalse(x,y,z))
        z = z + 2
    x = x + 3
#this gets run with an AutoHotkey script
with open('MC_Upload.ahk', 'w',encoding='utf-8-sig') as f:
    f.write("﻿#NoEnv\n#Warn\nSendMode Input\nSetWorkingDir %A_ScriptDir%\n")
    f.write("^+p::\nSend t\nsleep,100\n")
    for item in mcAssembly:
        f.write("%s\nsleep, 100\nSend t\nsleep, 100\n" % item)
print("Compiled to MC_Upload.ahk")
#

#assembler upload sequence
