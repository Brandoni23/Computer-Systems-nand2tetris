// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here:

@R2	//look at R2
M=0	//reset value

@R0  // look at R0
D=M // D = RAM[0]

@i	// indicator for loop
M=D	//i=R0

@END // go to END
D;JEQ	//if R0 is zero

@R1  // look at R1
D=M // D = RAM[1]

@END  // go to END
D;JEQ	//if R1 is zero

(LOOP)
@R1	//look at R1 (again)
D=M	//D = RAM[1]

@R2	//look at R2
M=D+M	//R2 = (R1=RAM[1]) + R2

@i	//look at indicator (i=R0 at first)
M=M-1	//i=i-1
D=M	    //  D=RAM[0] (or RAM[3])

@LOOP	//go to jump
D;JGT	//if i>0 then jump


(END)
@END
0;JMP	
