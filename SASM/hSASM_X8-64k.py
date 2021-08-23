import sys

translator = {"NOP": "11111111",
              "AIN": "10000000",
              "BIN": "10000001",
              "JMP": "10000010",
              "JPE": "10000101",
              "JPC": "10000100",
              "DSP": "10000011",
              "JBI": "10000110",
             "JBHI": "10000111",

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

              "MEO": "10110001",
              "MEN": "10110000",
              "SMA": "10100000",
             "SMAH": "10100001",

             "STK": "10110010",
             "USK": "10110011",

              }

literal_translator = {"STC": "0"}

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
        if(i.split()[0].upper() in literal_translator):
            bytestring = '{0:07b}'.format(int(i.split()[1]))
            assembled.append(literal_translator[i[0:3].upper()] + bytestring)
        else:
            assembled.append(translator[i.split()[0].upper()])
except:
    print("Assembly Failed, Unkown OPCode:")
    print(i)
    exit()

def hex_format(item):
    hexer = str(hex(int(item,2)))
    hexer = hexer[2:len(str(hex(int(item,2))))]
    if len(hexer) == 1:
        return "0" + hexer
    else:
        return hexer

with open('out.hex', 'w') as f:
    for item in assembled:
        f.write("%s" % hex_format(item))
    f.write("\n")

print("Compiled to out.hex")
#

#assembler upload sequence
