// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(RESTART) //
@SCREEN
D=A // D=screen 

@0
M=D	// Memory[0]=screen 

///////////////////////////

(KBDCHECK) //see if the keyboard is pressed
@KBD
D=M // D=Memory[kbd]

@BLACK
D;JGT	//Go to black if D > 0 (keyboard is pressed)

@WHITE
D;JEQ	//Go to white if D = 0 (keyboard is not pressed)

@KBDCHECK
0;JMP  //Go back to KBDCHECK after you're done 

///////////////////////////

(BLACK)
@1
M=-1	//1=-1 fill screen black

@CHANGE
0;JMP   //Go to CHANGE after you're done

(WHITE)
@1
M=0	    //1=0 fill screen white

@CHANGE
0;JMP //Go to CHANGE after you're done

//////////////////////////

(CHANGE)

@1	
D=M	// D=Memory[1]

@0
A=M	    //A=Memory[0]
M=D	    //Memory[0]=Memory[1]

@0
D=M+1	//D=Memory[0]+1

@KBD
D=A-D	//D=KBD-Memory[0]+1

@0
M=M+1	//Memory[0]=Memory[0]+1 next pixel
A=M     //A=Memory[0]

@CHANGE
D;JGT	//go to change if D>0

/////////////////////////

@RESTART
0;JMP  //Repeat the entire loop