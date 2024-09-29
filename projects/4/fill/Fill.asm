// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

@SCREEN
D=A

// reads kbd input -> if > 0 -> fill black, else fill white
(CHECKPRESS)
    @KEYBOARD
    D=M           
    @FILLBLACK
    D;JGT         // if input > 0 goto FILLBLACK
    @FILLWHITE
    0;JMP         // else goto FILLWHITE

// Fill the screen with black (-1)
(FILLBLACK)
    @16384        // base addr of screen, hack platform has 8192 screen size
    D=A           
    @PIXELS
    M=D           
    @24576        
    D=A           // D = 24576 -> end of screen

(FILLBLACK_LOOP)
    @PIXELS
    A=M           // A -> current addr of pixel
    M=-1          // set clr to black
    @PIXELS
    M=M+1         // addr++ until end of cscreen
    @PIXELS
    D=M
    @24576
    D=D-A    
    @FILLBLACK_LOOP
    D;JLT         //keep looping until we reach end of screen, if we do go back to checkpress
    @CHECKPRESS   

//works the same just as fillblack & fillblack_loop
(FILLWHITE)
    @16384        
    D=A           
    @PIXELS
    M=D           
    @24576        
    D=A           

(FILLWHITE_LOOP)
    @PIXELS
    A=M           
    M=0           
    @PIXELS
    M=M+1         
    @PIXELS
    D=M
    @24576
    D=D-A       
    @FILLWHITE_LOOP
    D;JLT         
    @CHECKPRESS   
