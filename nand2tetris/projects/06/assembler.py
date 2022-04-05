import argparse
import re

class Parser():
    def __init__(self, data):
        self.f=open(data,"r")

    def hasMoreCommnads(self):
        if self.f is None:
            self.hasMoreLines = False
        else:
            self.hasMoreLines = True
        return self.hasMoreLines

    def advance(self):
        if self.hasMoreLines == True:
            self.lastLineRead = self.f.readline()
            if not self.lastLineRead:
                self.f.close()
                self.lastLineRead = "EOF"
                self.f = None
            else:
                self.lastLineRead = self.lastLineRead.split('//')[0]
                self.lastLineRead = self.lastLineRead.strip()
                #print(self.lastLineRead)
        else:
            self.lastLineRead = "EOF"

    def commandType(self):
        if self.lastLineRead.startswith('//'):
            self.currentCommand = ""

        elif self.lastLineRead.startswith('@'):
            self.currentCommand = "A_COMMAND"

        elif self.lastLineRead.startswith(''):
            self.lastLineRead = ""
                
        elif self.lastLineRead.startswith('('):
            self.currentCommand = "L_COMMAND"

        else:
            self.currentCommand = "C_COMMAND"

        return self.currentCommand

    def symbol(self):
        self.symbolInCurrentCommand = ""
        if self.currentCommand == "A_COMMAND":  
            self.symbolInCurrentCommand = self.lastLineRead.split("@")[1]

        elif self.currentCommand == "L_COMMAND":
            self.symbolInCurrentCommand = re.split(r'[\(\)]', self.lastLineRead)[1]

        return self.symbolInCurrentCommand

    def dest(self):
        self.currentDest = "null"
        if self.currentCommand == "C_COMMAND":
            if "=" in self.lastLineRead:
                self.currentDest = self.lastLineRead.split("=")[0]

        return self.currentDest

    def comp(self):
        if self.currentCommand=="C_COMMAND":
            comp = self.lastLineRead 
            if "=" in comp:
                comp = comp.split("=")[1]
            if ';' in comp:
                comp = comp.split(";")[0]
            self.currentComp = comp

        return self.currentComp

    def jump(self):
        self.currentJump = 'null'
        if self.currentCommand=="C_COMMAND":
            if ";" in self.lastLineRead:
                self.currentJump = self.lastLineRead.split(";")[1]
        return self.currentJump

class Code():
    compCode = 0
    destCode = 0
    jumpCode = 0
    def dest(self, mnemonic):
        #convert dest(self) to binary
        if mnemonic == "null":
            self.destCode = 0b000
        elif mnemonic == "M":
            self.destCode = 0b001
        elif mnemonic == "D":
            self.destCode = 0b010
        elif mnemonic == "MD":
            self.destCode = 0b011
        elif mnemonic == "A":
            self.destCode = 0b100
        elif mnemonic == "AM":
            self.destCode = 0b101
        elif mnemonic == "AD":
            self.destCode = 0b110
        elif mnemonic == "AMD":
            self.destCode = 0b111
        return self.destCode

    def comp(self, mnemonic):
        #convert comp(self) to binary
        if mnemonic == "M":
            self.compCode = 0b1110000
        elif mnemonic == "!M":
            self.compCode = 0b1110001
        elif mnemonic == "-M":
            self.compCode = 0b1110011
        elif mnemonic == "M+1":
            self.compCode = 0b1110111
        elif mnemonic == "M-1":
            self.compCode = 0b1110010
        elif mnemonic == "D+M":
            self.compCode = 0b1000010
        elif mnemonic == "D-M":
            self.compCode = 0b1010011
        elif mnemonic == "M-D":
            self.compCode = 0b1000111
        elif mnemonic == "D&M":
            self.compCode = 0b1000000
        elif mnemonic == "D|M":
            self.compCode = 0b1010101
        elif mnemonic == "0":
            self.compCode = 0b0101010
        elif mnemonic == "1":
            self.compCode = 0b0111111
        elif mnemonic == "-1":
            self.compCode = 0b0111010
        elif mnemonic == "D":
            self.compCode = 0b0001100
        elif mnemonic == "A":
            self.compCode = 0b0110000
        elif mnemonic == "!D":
            self.compCode = 0b0001101
        elif mnemonic == "!A":
            self.compCode = 0b0110001
        elif mnemonic == "-D":
            self.compCode = 0b0001111
        elif mnemonic == "-A":
            self.compCode = 0b0110011
        elif mnemonic == "D+1":
            self.compCode = 0b0011111
        elif mnemonic == "A+1":
            self.compCode = 0b0110111
        elif mnemonic == "D-1":
            self.compCode = 0b0001110
        elif mnemonic == "A-1":
            self.compCode = 0b0110010
        elif mnemonic == "D+A":
            self.compCode = 0b0000010
        elif mnemonic == "D-A":
            self.compCode = 0b0010011
        elif mnemonic == "A-D":
            self.compCode = 0b0000111
        elif mnemonic == "D&A":
            self.compCode = 0b0000000
        elif mnemonic == "D|A":
            self.compCode = 0b0010101
        return self.compCode

    def jump(self, mnemonic):
        #convert jump(self) to binary
        if mnemonic == "null":
            self.jumpCode = 0b000
        elif mnemonic == "JGT":
            self.jumpCode = 0b001
        elif mnemonic == "JEQ":
            self.jumpCode = 0b010
        elif mnemonic == "JGE":
            self.jumpCode = 0b011
        elif mnemonic == "JLT":
            self.jumpCode = 0b100
        elif mnemonic == "JNE":
            self.jumpCode = 0b101
        elif mnemonic == "JLE":
            self.jumpCode = 0b110
        elif mnemonic == "JMP":
            self.jumpCode = 0b111
        return self.jumpCode

class SymbolTable():
    def __init__(self):
        self.my_dict = {'SP':0,'LCL':1,'ARG':2,'THIS':3,'THAT':4,'SCREEN':16384,'KBD':24576,
         'R0':0,'R1':1,'R2':2,'R3':3,'R4':4,'R5':5,'R6':6,'R7':7,'R8':8,'R9':9,'R10':10,'R11':11,'R12':12,'R13':13,'R14':14,'R15':15}

    def addEntry(self, symbol, address):
        self.my_dict[symbol]=address

    def contains(self, symbol):
        if symbol in self.my_dict:
            return True

        else:
            return False

    def GetAddress(self, symbol):
        if symbol in self.my_dict:
            return self.my_dict[symbol]

        else:
            return 16

    def getSymbolTable(self):
        return self.my_dict

def main():
    '''
    The main function for the assembler. Takes a command line argument for the input file
    and an optional argument for the output file.
    ''' 

    # Create an argument parser for command line arguments
    a_parser = argparse.ArgumentParser(description='Assembler for the Hack CPU')

    a_parser.add_argument('input_file', type=str)
    a_parser.add_argument('-o', dest='output_file', default='Prog.hack', type=str)
   
    args = a_parser.parse_args()

    inputFile = args.input_file
    outputFile = inputFile.replace(".asm",".hack")
    args.output_file = outputFile

    #My code starts here
    parser = Parser(args.input_file)
    coder = Code()
    symbtable = SymbolTable()

    #First pass
    address = 0
    flag = parser.hasMoreCommnads()
    while flag:
        parser.advance()
        if parser.commandType() == "":
            flag = parser.hasMoreCommnads()
            continue
        elif ((parser.commandType() == "A_COMMAND") | (parser.commandType() == "C_COMMAND")):
            address += 1
        elif parser.commandType() == "L_COMMAND":
            symbtable.addEntry(parser.symbol(),address)
        flag = parser.hasMoreCommnads()

    #Second pass
    w = open(outputFile,'w')
    d = 0
    parser2 = Parser(args.input_file)
    flag2 = parser2.hasMoreCommnads()
    while flag2:
        parser2.advance()
        if ((parser2.commandType() == "") | (parser2.commandType() == "L_COMMAND")):
            flag2 = parser2.hasMoreCommnads()
            continue
        elif parser2.commandType() == "C_COMMAND":
            f1 = '{:03b}'.format(0b111),'{:07b}'.format(coder.comp(parser2.comp())),'{:03b}'.format(coder.dest(parser2.dest())),'{:03b}'.format(coder.jump(parser2.jump()))
            f2 = ''.join(f1)
            w.write(f2)
            w.write('\n')
        else:
            if parser2.symbol().isnumeric() == True:
                symbtable.addEntry(parser2.symbol(),int(parser2.symbol()))
                w.write('{:016b}'.format(int(parser2.symbol())))
                w.write('\n')
            elif symbtable.contains(parser2.symbol()) == False:
                address2 = symbtable.GetAddress(parser2.symbol()) + d
                symbtable.addEntry(parser2.symbol(),address2)
                w.write('{:016b}'.format(address2))
                w.write('\n')
                d=d+1
            elif symbtable.contains(parser2.symbol()) == True:
                w.write('{:016b}'.format(symbtable.GetAddress(parser2.symbol())))
                w.write('\n')
        flag2 = parser2.hasMoreCommnads()

    w.close()
    
# Call the main function
if __name__ == "__main__":
    main()

