// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/FillStatic.asm

// Blackens the screen, i.e. writes "black" in every pixel. 
// Key presses are ignored.
// This is an intermediate step added to help you out.

// Put your code here.

@SCREEN
M=-1


@i
M=1

(LOOP)
@i
D=M


@SCREEN
A=A+D
M=-1
D=A

@24576
D=A-D

@i
M=M+1

@LOOP
D;JGT

(END)
@END
0;JMP