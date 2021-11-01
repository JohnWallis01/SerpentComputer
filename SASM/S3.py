Instructions = {"NOP":  "10111111 00000000",
              "LDMG":   "10000000 0WWWWWWW", #load from main, General
              "LDMP":   "10000000 1XXXWWWW", #load from main port
              "JMP":    "10000010 00000000",
              "JPE":    "10000101 00000000",
              "JPC":    "10000100 00000000",

              "RPORT": "10001000 PPPPPPPP"

              "FLF":    "11110011 LLLL RRRR",
              "FLT":    "11111100 LLLL RRRR",
              "SUM":    "11001001 LLLL RRRR",
              "SUB":    "11010110 LLLL RRRR",
              "AOT":    "11111111 LLLL RRRR",
              "BOT":    "11111010 LLLL RRRR",
              "AMM":    "11001111 LLLL RRRR",
              "NTA":    "11110000 LLLL RRRR",
              "NTB":    "11110101 LLLL RRRR",
              "XOR":    "11111001 LLLL RRRR",
              "AND":    "11111110 LLLL RRRR",
              "ORR":    "11111011 LLLL RRRR",
              "LSH":    "11011100 LLLL RRRR",
              "CMP":    "11000110 LLLL RRRR",


              "MEOG":   "10110001 0WWWWWWW",
              "MEOP":   "10110001 1XXXWWWW",

              "MEN":    "10110000 00000000",

              "STK":    "10110010 00000000",
              "USKG":   "10110011 0WWWWWWW",
              "USKP":   "10110011 1XXXWWWW",


              "STC":    "0 CCCCCCCCCCCCCCC"
              }


#register mappings
#one hot

#LDI, MEO, USK
RegLoadMapGeneral =
        {"DDR":     "0000 0001",
          "R1":     "0000 0010",
          "R2":     "0000 0100",
          "R3":     "0000 1000",
          "R4":     "0001 0000",
         "RJB":     "0010 0000",
         "RMA":     "0100 0000",
          }
RegLoadMapPort =
            {"PortALow":    "1XXX0001",
            "PortAHigh":    "1XXX0010",
            "PortBLow":     "1XXX0100",
            "PortBHigh":    "1XXX1000",
            }


# READ Ports,



#ALU Input controls

#B (3 downto 0)
LeftALU = { "Main": "1111",
            "R1": "1110",
            "R3": "1101",
            "RJB": "1011",
            "RMA": "0111",
            }

RightALU = { "Main": "1111",
            "R2": "1110",
            "R4": "1101",
            "RJB": "1011",
            "RMA": "0111",
            }

#Jumps
Jumps = {"None": "00",
         "JMP": "11",
         "JPC": "01",
         "JPE": "10"}
