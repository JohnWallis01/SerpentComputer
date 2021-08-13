import sys
translator = {"NOP": "0000000000000000",
              "AIN": "0000000010000000",
              "BIN": "0000000010000001",
              "JMP": "0000000010000010",
              "JPE": "0000000010000101",
              "JPC": "0000000010000100",
              "DSP": "0000000010000011",
              "JBI": "0000000010000110",
#need a get JBI commanmnd (GJB)
              "FLF": "0000000011110011",
              "FLT": "0000000011111100",
              "SUM": "0000000011001001",
              "SUB": "0000000011010110",
              "AOT": "0000000011111111",
              "BOT": "0000000011111010",
              "A--": "0000000011001111",
              "NTA": "0000000011110000",
              "NTB": "0000000011110101",
              "XOR": "0000000011111001",
              "AND": "0000000011111110",
              "ORR": "0000000011111011",
              "LSH": "0000000011011100",

              "MEO": "0000000000110001",
              "MEN": "0000000000110000",
              "SMA": "0000000000100000",
#need a get mem addr command (GMA)
              "STK": "0000000000110010",
              "USK": "0000000000110011",
              "SSK": "0000000000110100",
              "RSK": "0000000000110101"

              }

literal_translator = {"STC": "1"}

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
            bytestring = '{0:015b}'.format(int(i.split()[1]))
            assembled.append(literal_translator[i[0:3].upper()] + bytestring)
        else:
            # this needs to be imporved
            assembled.append(translator[i[0:3].upper()])
except:
    print("Assembly Failed, Unkown OPCode:")
    print(i)
    exit()

with open('out.bin', 'w') as f:
    for item in assembled:
        f.write("%s\n" % item)
print("Compiled to out.bin")
