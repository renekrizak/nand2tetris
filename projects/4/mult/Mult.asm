// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.
//
//// Replace this comment with your code.

//pretty much just i++ until i-r0 >= 0, then the multiplication should be done and program ends
@sum
M=0 // sum=0
@i
M=0 //i=0
(LOOP)
    @i
    D=M //d=i
    @0
    D=D-M 
    @END
    D;JGE //basically if i-r0 >= 0, progam goes to END

    @1
    D=M //d=r1
    @sum
    M=D+M //sum+=r1
    @i
    M=M+1 //i++
    @LOOP
    0;JMP //repeats the loop from @R0 
(END)
    @END
    0;JMP







