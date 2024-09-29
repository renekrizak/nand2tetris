// PSEUDO CODE
    // x=R1
    // y=R2
    // R3=0
    // while(x > 0) {
    //     R3 += y
    //     x--
    // }
    
    @R1
    D=M
    @x
    M=D // x = R1

    @R2
    D=M
    @y
    M=D // y = R2

    @0
    D=A
    @R3
    M=D // R3 = 0

(WHILE)
    // begin of loop condition
    @x
    D=M 
    @END
    D;JLE   // if x <= 0 proceed to END      
    // end of loop condition

    // begin body of while- could someone help explain this part? Thanks :")
    @y
    D=M // D = y
    @R3
    M=D+M   // sum = sum + y
    @1
    D=A // D = 1
    @x
    M=M-D   


    @WHILE
    0;JMP   
(END)   
    @END
    0;JMP 
