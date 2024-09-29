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


@color    // declare color variable
M=0      // by default is white

(LOOP)

  @SCREEN
  D=A
  @pixels
  M=D         // pixel address, goes from 16384 to 16384 + 8192 == 24576

  @KBD    // keyboard address
  D=M
  @BLACK
  D;JGT     // if(keyboard > 0) goto BLACK
  
  @color
  M=0       // set to white
  @COLOR_SCREEN
  0;JMP     // jump to subroutine that colors the screen
  
  (BLACK)
    @color
    M=-1    // set to black (2's complement 111111111...)

  (COLOR_SCREEN)
    @color
    D=M
    @pixels
    A=M         // VERY IMPORTANT! indirect address
    M=D         // color M[pixels] with @color
    
    @pixels
    M=M+1
    D=M
        
    @24576
    D=D-A
    @COLOR_SCREEN
    D;JLT

@LOOP
0;JMP // infinite loop