"""
hvm-skeleton.py -- VM Translator, Part I
    Skeleton File
"""

import sys
import os
import argparse
import re

#import parser as MyParser
#import codewriter as MyCodeWriter

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
            self.w.write('@SP\nM=M-1\n@SP\nA=M\nD=M\nA=A-1\nM=M-D\nD=M\n@ARIT'+str(count)+'\nD;JEQ\n@SP\nA=M\nA=A-1\nM=0\n(ARIT'+str(count)+')\n@SP\nA=M\nA=A-1\nM=-1\n')
        elif command == 'gt':
            self.w.write('@SP\nM=M-1\n@SP\nA=M\nD=M\nA=A-1\nM=M-D\nD=M\n@ARIT'+str(count)+'\nD;JGT\n@SP\nA=M\nA=A-1\nM=0\n(ARIT'+str(count)+')\n@SP\nA=M\nA=A-1\nM=-1\n')
        elif command == 'lt':
            self.w.write('@SP\nM=M-1\n@SP\nA=M\nD=M\nA=A-1\nM=M-D\nD=M\n@ARIT'+str(count)+'\nD;JLT\n@SP\nA=M\nA=A-1\nM=0\n(ARIT'+str(count)+')\n@SP\nA=M\nA=A-1\nM=-1\n')
        elif command == 'and':
            self.w.write('@SP\nM=M-1\n@SP\nA=M\nD=M\nA=A-1\nM=D&M\n')
        elif command == 'or':
            self.w.write('@SP\nM=M-1\n@SP\nA=M\nD=M\nA=A-1\nM=D|M\n')       
        elif command == 'not':
            self.w.write('@SP\nA=M\nA=A-1\nA=A-1\nM=!M\n')
        count += 1

    def writePushPop(self, command, segment, index, sname):
        if command == 'C_PUSH':
            if segment == 'argument':
                self.w.write('@ARG\nA=M\nD=A\n@'+str(index)+'\nA=A+D\nD=M\n')    
            elif segment == 'local':
                self.w.write('@LCL\nA=M\nD=A\n@'+str(index)+'\nA=A+D\nD=M\n')
            elif segment == 'static':
                self.w.write('@'+sname+'.'+str(index)+'\nD=M\n')
                #self.w.write('@'+sname+'.'+str(index)+'\nD=A\n@'+str(index)+'\nA=A+D\nD=M\n')
            elif segment == 'constant':
                self.w.write('@'+str(index)+'\nD=A\n')
            elif segment == 'this':
                self.w.write('@THIS\nA=M\nD=A\n@'+str(index)+'\nA=A+D\nD=M\n')
            elif segment == 'that':
                self.w.write('@THAT\nA=M\nD=A\n@'+str(index)+'\nA=A+D\nD=M\n')
            elif segment == 'pointer':
                if index == 0:
                    self.w.write('@THIS\nA=M\nD=A\n@'+str(index)+'\nA=A+D\nD=M\n')
                else:
                    self.w.write('@THAT\nA=M\nD=A\n@'+str(index)+'\nA=A+D\nD=M\n')
            elif segment == 'temp':
                self.w.write('@5\nD=A\n@'+str(index)+'\nA=A+D\nD=M\n') 

            self.w.write('@SP\nA=M\nM=D\n@SP\nM=M+1\n')

        elif command == 'C_POP':
            if segment == 'argument':
                self.w.write('@ARG\nA=M\nD=A\n@'+str(index)+'\nA=A+D\n')    
            elif segment == 'local':
                self.w.write('@LCL\nA=M\nD=A\n@'+str(index)+'\nA=A+D\n')
            elif segment == 'static':
                self.w.write('@'+sname+'.'+str(index))
            elif segment == 'this':
                self.w.write('@THIS\nA=M\nD=A\n@'+str(index)+'\nA=A+D\n')
            elif segment == 'that':
                self.w.write('@THAT\nA=M\nD=A\n@'+str(index)+'\nA=A+D\n')
            elif segment == 'pointer':
                if index == 0:
                    self.w.write('@THIS\nA=M\nD=A\n@'+str(index)+'\nA=A+D\n')
                else:
                    self.w.write('@THAT\nA=M\nD=A\n@'+str(index)+'\nA=A+D\n')
            elif segment == 'temp':
                self.w.write('@5\nD=A\n@'+str(index)+'\nA=A+D\n') 
       
            self.w.write('D=A\n@R13\nM=D\n@SP\nM=M-1\n@SP\nA=M\nD=M\n@R13\nA=M\nM=D\n')
        
    def Close(self):
        self.w.close()

#def HandleFile(VMName):
#    AsmFile = VMName.split(".vm")[0] + ".asm"
#def HandleDirectory(DirName):
#    [path, name] = os.path.split(DirName)
#    if name == "":
#        [path, name] = os.path.split(path)
#    SrcDir = os.path.join(path, name)
#    AsmFile = os.path.join(path, name, name + ".asm")
    # Now, find the vm files and process them
#    for f in os.listdir(SrcDir):
#        if f.endswith(".vm"):
#            VMName = os.path.join(SrcDir, f)

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
        for vmf in vm:
            VMFiles = [filepath + '/' + vmf]
    return AsmFile, VMFiles



#def Process(sourceFile, codeWriter):
 #   print('Processing ' + sourceFile)
  #  parser = MyParser.Parser(sourceFile)
   # codeWriter.SetFileName(sourceFile)
    
    #while parser.Advance():
     #   commandType = parser.CommandType()
      #  if commandType == C_ARITHMETIC:
       #     #codeWriter. write somethign
        #    pass
        #elif commandType in (C_PUSH, C_POP):
            # codeWriter. write something
         #   pass

def main():
    #a_parser = argparse.ArgumentParser(description='VM Translator for the Hack Assembler')

    #a_parser.add_argument('input_file', type=str)
    #a_parser.add_argument('-o', dest='output_file', default='Prog.asm', type=str)
   
    #args = a_parser.parse_args()

    #inputFile = args.input_file
    #outputFile = inputFile.replace(".vm",".asm")
    #args.output_file = outputFile

    sourceName = sys.argv[1]
    diroutputFile, dirinputFiles = parse_files(sourceName)
    print(diroutputFile)
    outputFile = diroutputFile.split('/')[-1]

    coder = CodeWriter(outputFile)
    
    #StackArithmetic/SimpleAdd/SimpleAdd.vm
    #if os.path.isdir(sourceName):
    #    HandleDirectory(sourceName)
    #else:
    #    HandleFile(sourceName)


    for vm_file in dirinputFiles:
        parser = Parser(vm_file)
        file = vm_file.split('/')[-1]
        static_name = file.replace('.vm','')

        flag = parser.hasMoreCommnads()
        while flag:
            parser.advance()
            ct = parser.commandType()
            if ct == "":
                flag = parser.hasMoreCommnads()
                continue

            elif ct == 'C_ARITHMETIC':
                coder.writeArithmetic(parser.arg1(),0)

            elif ((ct == "C_POP") | (ct == "C_PUSH")):
                coder.writePushPop(ct,parser.arg1(),parser.arg2(),static_name)

            flag = parser.hasMoreCommnads()
        
    coder.Close()

if __name__ == "__main__":
    main()

#if len(sys.argv) != 2:
    #    print('usage: hvm sourceFile.vm')
    #    print('    sourceFile may be a directory in which case all')
    #    print('    vm files in the directory will be processed to')
    #    print('    sourceFile.asm')
    #    return

    #sourceName = sys.argv[1]

    #if os.path.isdir(sourceName):
        # process all .vm files in dir

        #print('Processing directory ' + dirName)
        # 1) Determine output assembly file name
        #     use: os.path.split()
        #          os.path.extsep
        #     Create a codeWriter instance for this output file
        # 2) Loop through all *.vm files in directory
        #     use: os.listdir( directory )
        #          os.path.splitext( filename ) to determine extension
        #     ignore files that do not have the "vm" extension
        # 3) Create a new parser instance _for each file_
        #     Use a common codewriter module
    #else:
        # process single .vm file

        #1) determine output assembly file name and
        #    create codewriter instance
        #2) Start parser for the vm file
     #   Process(sourceName, codeWriter)
