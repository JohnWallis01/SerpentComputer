import sys
legacy_opcode = {"JPE": "10101001",
                 "JPL": "10010110",
                 "JGE": "01010110",}

translator = {  "NOP": "00000000",
                "HLT": "10111111",
                "AIN": "10000000",
                "BIN": "10000001",
                "JMP": "10000010",
                "JPE": "10000101",
                "JPC": "10000100",
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
                "NTB": "11110101",
                "XOR": "11111001",
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
except:
    print("Assembly Failed, Unkown OPCode:")
    print(i)
    exit()

with open('out.bin', 'w') as f:
    for item in assembled:
        f.write("%s\n" % item)
print("Compiled to out.bin")
#

#assembler upload sequence
