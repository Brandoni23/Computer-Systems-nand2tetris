import sys
import os
import argparse
import re
import textwrap

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
                self.lastLineRead = textwrap.dedent(self.lastLineRead)
                #print(self.lastLineRead)
        else:
            self.lastLineRead = "EOF"

    def commandType(self):
        if self.lastLineRead.startswith("push"):
            self.CommandType = 'C_PUSH'

        elif self.lastLineRead.startswith('pop'):
            self.CommandType = 'C_POP'

        elif self.lastLineRead.startswith('label'):
            self.CommandType = 'C_LABEL'
            
        elif self.lastLineRead.startswith('if-goto'):
            self.CommandType = 'C_IF'
            
        elif self.lastLineRead.startswith('goto'):
            self.CommandType = 'C_GOTO'
        
        elif self.lastLineRead.startswith('function'):
            self.CommandType = 'C_FUNCTION'
            
        elif self.lastLineRead.startswith('call'):
            self.CommandType = 'C_CALL'
            
        elif self.lastLineRead.startswith('return'):
            self.CommandType = 'C_RETURN'
            
        elif self.lastLineRead.startswith('//'):
            self.CommandType = ''  

        elif self.lastLineRead == '':
            self.CommandType = ''

        else:
            self.CommandType = 'C_ARITHMETIC'

        return self.CommandType

    def arg1(self):
        if self.CommandType == 'C_ARITHMETIC':
            self.argument1 = self.lastLineRead.strip()

        elif self.CommandType == '':
            self.argument1 == ''

        elif self.CommandType == 'C_POP':
            self.argument1 = self.lastLineRead.split()[1]

        elif self.CommandType == 'C_PUSH':
            self.argument1 = self.lastLineRead.split()[1]

        elif self.CommandType == 'C_LABEL':
            self.argument1 = self.lastLineRead.split()[1]

        elif self.CommandType == 'C_GOTO':
            self.argument1 = self.lastLineRead.split()[1]

        elif self.CommandType == 'C_IF':
            self.argument1 = self.lastLineRead.split()[1]

        elif self.CommandType == 'C_FUNCTION':
            self.argument1 = self.lastLineRead.split()[1]

        elif self.CommandType == 'C_CALL':
            self.argument1 = self.lastLineRead.split()[1]

        else:
            self.argument1 = ''

        return self.argument1

    def arg2(self):
        if self.CommandType == 'C_PUSH':
            self.argument2 = self.lastLineRead.split(' ')[2].strip()

        elif self.CommandType == 'C_POP':
            self.argument2 = self.lastLineRead.split(' ')[2].strip()

        elif self.CommandType == 'C_FUNCTION':
            self.argument2 = self.lastLineRead.split(' ')[2].strip()

        elif self.CommandType == 'C_CALL':
            self.argument2 = self.lastLineRead.split(' ')[2].strip()

        return int(self.argument2)

class CodeWriter():
    def __init__(self, data):
        self.w=open(data,'w')

    def setFileName(self, fileName):
        outputFile2 =  fileName.split('.vm')[0] + '.asm' 
        print(f"I am compiling {fileName} into the assembly file {outputFile2}.")
    
    def writeArithmetic(self, command, count):
        if command == 'add':
            self.w.write('@SP\nM=M-1\n@SP\nA=M\nD=M\nA=A-1\nM=M+D\n')
        elif command == 'sub':
            self.w.write('@SP\nM=M-1\n@SP\nA=M\nD=M\nA=A-1\nM=M-D\n')
        elif command == 'neg':
            self.w.write('@SP\nA=M\nA=A-1\nM=-M\n')
        elif command == 'eq':
            self.w.write('@SP\nM=M-1\n@SP\nA=M\nD=M\nA=A-1\nM=M-D\nD=M\n@ARIT'+str(count)+'\nD;JEQ\n@SP\nA=M\nA=A-1\nM=0\n@JUMP'+str(count)+'\n0;JMP\n(ARIT'+str(count)+')\n@SP\nA=M\nA=A-1\nM=-1\n(JUMP'+str(count)+')\n')
        elif command == 'gt':
            self.w.write('@SP\nM=M-1\n@SP\nA=M\nD=M\nA=A-1\nM=M-D\nD=M\n@ARIT'+str(count)+'\nD;JGT\n@SP\nA=M\nA=A-1\nM=0\n@JUMP'+str(count)+'\n0;JMP\n(ARIT'+str(count)+')\n@SP\nA=M\nA=A-1\nM=-1\n(JUMP'+str(count)+')\n')
        elif command == 'lt':
            self.w.write('@SP\nM=M-1\n@SP\nA=M\nD=M\nA=A-1\nM=M-D\nD=M\n@ARIT'+str(count)+'\nD;JLT\n@SP\nA=M\nA=A-1\nM=0\n@JUMP'+str(count)+'\n0;JMP\n(ARIT'+str(count)+')\n@SP\nA=M\nA=A-1\nM=-1\n(JUMP'+str(count)+')\n')
        elif command == 'and':
            self.w.write('@SP\nM=M-1\n@SP\nA=M\nD=M\nA=A-1\nM=D&M\n')
        elif command == 'or':
            self.w.write('@SP\nM=M-1\n@SP\nA=M\nD=M\nA=A-1\nM=D|M\n')       
        elif command == 'not':
            self.w.write('@SP\nA=M\nA=A-1\nM=!M\n')

    def writePushPop(self, command, segment, index, sname):
        if command == 'C_PUSH':
            if segment == 'argument':
                #self.w.write('@ARG\nD=M\n@'+str(index)+'\nA=D+A\nD=M\n') 
                self.w.write('@ARG\nA=M\nD=A\n@'+str(index)+'\nA=A+D\nD=M\n')   
            elif segment == 'local':
                self.w.write('@LCL\nA=M\nD=A\n@'+str(index)+'\nA=A+D\nD=M\n')
                #self.w.write('@LCL\nD=M\n@'+str(index)+'\nA=D+A\nD=M\n')
            elif segment == 'static':
                self.w.write('@'+sname+'.'+str(index)+'\nD=M\n')
            elif segment == 'constant':
                self.w.write('@'+str(index)+'\nD=A\n')
            elif segment == 'this':
                #self.w.write('@THIS\nD=M\n@'+str(index)+'\nA=D+A\nD=M\n')
                self.w.write('@THIS\nA=M\nD=A\n@'+str(index)+'\nA=A+D\nD=M\n')
            elif segment == 'that':
                #self.w.write('@THAT\nD=M\n@'+str(index)+'\nA=D+A\nD=M\n')
                self.w.write('@THAT\nA=M\nD=A\n@'+str(index)+'\nA=A+D\nD=M\n')
            elif segment == 'pointer':
                if index == 0:
                    self.w.write('@THIS\nD=M\n')
                else:
                    self.w.write('@THAT\nD=M\n')
            elif segment == 'temp':
                self.w.write('@5\nD=A\n@'+str(index)+'\nA=A+D\nD=M\n') 

            self.w.write('@SP\nA=M\nM=D\n@SP\nM=M+1\n')

        elif command == 'C_POP':
            if segment == 'argument': 
                self.w.write('@ARG\nD=M\n@'+str(index)+'\nA=D+A\n') 
            elif segment == 'local':
                self.w.write('@LCL\nD=M\n@'+str(index)+'\nA=D+A\n')
            elif segment == 'static':
                self.w.write('@'+sname+'.'+str(index)+'\n')
            elif segment == 'this':
                self.w.write('@THIS\nD=M\n@'+str(index)+'\nA=D+A\n')
            elif segment == 'that':
                self.w.write('@THAT\nD=M\n@'+str(index)+'\nA=D+A\n')
            elif segment == 'pointer':
                if index == 0:
                    self.w.write('@THIS\n')
                else:
                    self.w.write('@THAT\n')
            elif segment == 'temp':
                self.w.write('@5\nD=A\n@'+str(index)+'\nA=A+D\n') 
       
            self.w.write('D=A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n')
        
    def writeInit(self,file):
        self.w.write('@256\nD=A\n@SP\nM=D\n')
        self.writeCall('Sys.init',0,file,0)

    def writeLabel(self,label,count):
        self.w.write('('+label+'.'+count+')\n') 

    def writeGoto(self,label,count):
        self.w.write('@'+label+'.'+count+'\n0;JMP\n')

    def writeIF(self,label,count):
        self.w.write('@SP\nAM=M-1\nD=M\n@'+label+'.'+count+'\nD;JNE\n')

    def writeCall(self,functionName,numArgs,file,count): 
        self.w.write('@'+file+'.RET_'+str(count)+'\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        for i in ['@LCL','@ARG','@THIS','@THAT']:
            self.w.write(i+'\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        self.w.write('@5\nD=A\n@'+str(numArgs)+'\nD=D+A\n@SP\nD=M-D\n@ARG\nM=D\n')
        self.w.write('@SP\nD=M\n@LCL\nM=D\n')
        self.w.write('@'+functionName+'\n0;JMP\n')
        self.w.write('('+file+'.RET_'+str(count)+')\n')

    def writeReturn(self):
        self.w.write("@LCL\nD=M\n@R13\nM=D\n")
        self.w.write("@5\nD=A\n@R13\nA=M-D\nD=M\n@R14\nM=D\n")
        self.w.write("@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\n@ARG\nD=M+1\n@SP\nM=D\n")
        self.dict = {1:'@THAT', 2:'@THIS', 3:'@ARG', 4:'@LCL'}
        for key, value in self.dict.items():
            self.w.write('@'+str(key)+'\nD=A\n@R13\nA=M-D\nD=M\n'+value+'\nM=D\n')
        self.w.write('@R14\nA=M\n0;JMP\n')

    def writeFunction(self,functionName,numLocals,count):
        self.w.write('('+functionName+')\n')
        for i in range(numLocals):
            self.w.write('@SP\nA=M\nM=0\n@SP\nM=M+1\n')
        
    def Close(self):
        self.w.close()

def parse_files(filepath):
    if '.vm' in filepath:
        AsmFile = filepath.replace('.vm','.asm')
        VMFiles = [filepath]

    else:
        if filepath[-1] == '/':
            filepath = filepath[:-1] 
        else:
            filepath = filepath
        path_folders = filepath.split('/')
        AsmFile = filepath + '/' + path_folders[-1] + '.asm'
        dirpath, dirnames, filenames = next(os.walk(filepath),[[],[],[]])
        vm = filter(lambda x: '.vm' in x, filenames)
        VMFiles = []
        for vmf in vm:
            VMFiles.append(filepath + '/' + vmf)
    return AsmFile, VMFiles

def main():
    sourceName = sys.argv[1]
    diroutputFile, dirinputFiles = parse_files(sourceName)
    outputFile = diroutputFile.split('/')[-1]

    coder = CodeWriter(diroutputFile)

    if sys.argv[-1] == '-y':
        coder.writeInit(outputFile.replace('.asm',''))

    elif len(dirinputFiles) > 1:
        coder.writeInit(outputFile.replace('.asm',''))

    for vm_file in dirinputFiles:
        parser = Parser(vm_file)
        file = vm_file.split('/')[-1]
        static_name = file.replace('.vm','')  

        count = 1
        flag = parser.hasMoreCommnads()
        fn = ''
        while flag:
            parser.advance()
            ct = parser.commandType()
            if ct == 'C_FUNCTION':
                fn = parser.arg1()

            if ct == "":
                flag = parser.hasMoreCommnads()
                continue

            elif ct == 'C_ARITHMETIC':
                coder.writeArithmetic(parser.arg1(),count)

            elif ct == 'C_LABEL':
                coder.writeLabel(parser.arg1(),fn)

            elif ct == 'C_GOTO':
                coder.writeGoto(parser.arg1(),fn) 

            elif ct == 'C_IF':
                coder.writeIF(parser.arg1(),fn)

            elif ct == 'C_CALL':
                coder.writeCall(parser.arg1(),parser.arg2(),static_name,count)

            elif ct == 'C_RETURN':
                coder.writeReturn()

            elif ct == 'C_FUNCTION':
                coder.writeFunction(parser.arg1(),parser.arg2(),count)

            elif ((ct == "C_POP") | (ct == "C_PUSH")):
                coder.writePushPop(ct,parser.arg1(),parser.arg2(),static_name)
                
            count += 1
            flag = parser.hasMoreCommnads()
        
    coder.Close()

if __name__ == "__main__":
    main()