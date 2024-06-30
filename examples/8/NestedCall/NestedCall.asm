// Bootstrap code
@256
D=A
@SP
M=D
// Call Sys.init 0
// Save the return address
@Sys.init$ret.1
D=A
@SP
AM=M+1
A=A-1
M=D
// Save LCL of the caller
@LCL
D=M
@SP
AM=M+1
A=A-1
M=D
// Save ARG of the caller
@ARG
D=M
@SP
AM=M+1
A=A-1
M=D
// Save THIS of the caller
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D
// Save THAT of the caller
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D
// Reposition LCL
@SP
D=M
@LCL
M=D
// Reposition ARG
@5
D=D-A
@ARG
M=D
// Transfer control to the called function
@Sys.init
0;JMP
// Declare a label for the return address
(Sys.init$ret.1)

// Translation of Sys.vm
(Sys.init)
@4000
D=A
@SP
AM=M+1
A=A-1
M=D
@SP
AM=M-1
D=M
@THIS
M=D
@5000
D=A
@SP
AM=M+1
A=A-1
M=D
@SP
AM=M-1
D=M
@THAT
M=D
// Call Sys.main 0
// Save the return address
@Sys.main$ret.2
D=A
@SP
AM=M+1
A=A-1
M=D
// Save LCL of the caller
@LCL
D=M
@SP
AM=M+1
A=A-1
M=D
// Save ARG of the caller
@ARG
D=M
@SP
AM=M+1
A=A-1
M=D
// Save THIS of the caller
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D
// Save THAT of the caller
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D
// Reposition LCL
@SP
D=M
@LCL
M=D
// Reposition ARG
@5
D=D-A
@ARG
M=D
// Transfer control to the called function
@Sys.main
0;JMP
// Declare a label for the return address
(Sys.main$ret.2)
@SP
AM=M-1
D=M
@6
M=D
(Sys.main$LOOP)
@Sys.main$LOOP
0;JMP
(Sys.main)
@0
D=A
@SP
AM=M+1
A=A-1
M=D
@0
D=A
@SP
AM=M+1
A=A-1
M=D
@0
D=A
@SP
AM=M+1
A=A-1
M=D
@0
D=A
@SP
AM=M+1
A=A-1
M=D
@0
D=A
@SP
AM=M+1
A=A-1
M=D
@4001
D=A
@SP
AM=M+1
A=A-1
M=D
@SP
AM=M-1
D=M
@THIS
M=D
@5001
D=A
@SP
AM=M+1
A=A-1
M=D
@SP
AM=M-1
D=M
@THAT
M=D
@200
D=A
@SP
AM=M+1
A=A-1
M=D
@1
D=A
@LCL
D=D+M
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
@40
D=A
@SP
AM=M+1
A=A-1
M=D
@2
D=A
@LCL
D=D+M
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
@6
D=A
@SP
AM=M+1
A=A-1
M=D
@3
D=A
@LCL
D=D+M
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
@123
D=A
@SP
AM=M+1
A=A-1
M=D
// Call Sys.add12 1
// Save the return address
@Sys.add12$ret.3
D=A
@SP
AM=M+1
A=A-1
M=D
// Save LCL of the caller
@LCL
D=M
@SP
AM=M+1
A=A-1
M=D
// Save ARG of the caller
@ARG
D=M
@SP
AM=M+1
A=A-1
M=D
// Save THIS of the caller
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D
// Save THAT of the caller
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D
// Reposition LCL
@SP
D=M
@LCL
M=D
// Reposition ARG
@6
D=D-A
@ARG
M=D
// Transfer control to the called function
@Sys.add12
0;JMP
// Declare a label for the return address
(Sys.add12$ret.3)
@SP
AM=M-1
D=M
@5
M=D
@0
D=A
@LCL
A=D+M
D=M
@SP
AM=M+1
A=A-1
M=D
@1
D=A
@LCL
A=D+M
D=M
@SP
AM=M+1
A=A-1
M=D
@2
D=A
@LCL
A=D+M
D=M
@SP
AM=M+1
A=A-1
M=D
@3
D=A
@LCL
A=D+M
D=M
@SP
AM=M+1
A=A-1
M=D
@4
D=A
@LCL
A=D+M
D=M
@SP
AM=M+1
A=A-1
M=D
@SP
AM=M-1
D=M
@SP
A=M-1
M=D+M
@SP
AM=M-1
D=M
@SP
A=M-1
M=D+M
@SP
AM=M-1
D=M
@SP
A=M-1
M=D+M
@SP
AM=M-1
D=M
@SP
A=M-1
M=D+M
// Return command
// Save the return address to R13
@LCL
D=M
@5
D=D-A
A=D
D=M
@R13
M=D
// Reposition ARG of the caller
@SP
A=M-1
D=M
@ARG
A=M
M=D
// Reposition SP of the caller
D=A+1
@SP
M=D
// Restore THAT of the caller
@LCL
D=M
@R14
AM=D-1
D=M
@THAT
M=D
// Restore THIS of the caller
@R14
AM=M-1
D=M
@THIS
M=D
// Restore ARG of the caller
@R14
AM=M-1
D=M
@ARG
M=D
// Restore LCL of the caller
@R14
AM=M-1
D=M
@LCL
M=D
// Go to return address in the caller's code
@R13
A=M
0;JMP
(Sys.add12)
@4002
D=A
@SP
AM=M+1
A=A-1
M=D
@SP
AM=M-1
D=M
@THIS
M=D
@5002
D=A
@SP
AM=M+1
A=A-1
M=D
@SP
AM=M-1
D=M
@THAT
M=D
@0
D=A
@ARG
A=D+M
D=M
@SP
AM=M+1
A=A-1
M=D
@12
D=A
@SP
AM=M+1
A=A-1
M=D
@SP
AM=M-1
D=M
@SP
A=M-1
M=D+M
// Return command
// Save the return address to R13
@LCL
D=M
@5
D=D-A
A=D
D=M
@R13
M=D
// Reposition ARG of the caller
@SP
A=M-1
D=M
@ARG
A=M
M=D
// Reposition SP of the caller
D=A+1
@SP
M=D
// Restore THAT of the caller
@LCL
D=M
@R14
AM=D-1
D=M
@THAT
M=D
// Restore THIS of the caller
@R14
AM=M-1
D=M
@THIS
M=D
// Restore ARG of the caller
@R14
AM=M-1
D=M
@ARG
M=D
// Restore LCL of the caller
@R14
AM=M-1
D=M
@LCL
M=D
// Go to return address in the caller's code
@R13
A=M
0;JMP

