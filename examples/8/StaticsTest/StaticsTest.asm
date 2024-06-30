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

// Translation of Class1.vm
(Class1.set)
@0
D=A
@ARG
A=D+M
D=M
@SP
AM=M+1
A=A-1
M=D
@SP
AM=M-1
D=M
@Class1.0
M=D
@1
D=A
@ARG
A=D+M
D=M
@SP
AM=M+1
A=A-1
M=D
@SP
AM=M-1
D=M
@Class1.1
M=D
@0
D=A
@SP
AM=M+1
A=A-1
M=D
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
(Class1.get)
@Class1.0
D=M
@SP
AM=M+1
A=A-1
M=D
@Class1.1
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
M=M-D
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

// Translation of Class2.vm
(Class2.set)
@0
D=A
@ARG
A=D+M
D=M
@SP
AM=M+1
A=A-1
M=D
@SP
AM=M-1
D=M
@Class2.0
M=D
@1
D=A
@ARG
A=D+M
D=M
@SP
AM=M+1
A=A-1
M=D
@SP
AM=M-1
D=M
@Class2.1
M=D
@0
D=A
@SP
AM=M+1
A=A-1
M=D
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
(Class2.get)
@Class2.0
D=M
@SP
AM=M+1
A=A-1
M=D
@Class2.1
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
M=M-D
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

// Translation of Sys.vm
(Sys.init)
@6
D=A
@SP
AM=M+1
A=A-1
M=D
@8
D=A
@SP
AM=M+1
A=A-1
M=D
// Call Class1.set 2
// Save the return address
@Class1.set$ret.2
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
@7
D=D-A
@ARG
M=D
// Transfer control to the called function
@Class1.set
0;JMP
// Declare a label for the return address
(Class1.set$ret.2)
@SP
AM=M-1
D=M
@5
M=D
@23
D=A
@SP
AM=M+1
A=A-1
M=D
@15
D=A
@SP
AM=M+1
A=A-1
M=D
// Call Class2.set 2
// Save the return address
@Class2.set$ret.3
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
@7
D=D-A
@ARG
M=D
// Transfer control to the called function
@Class2.set
0;JMP
// Declare a label for the return address
(Class2.set$ret.3)
@SP
AM=M-1
D=M
@5
M=D
// Call Class1.get 0
// Save the return address
@Class1.get$ret.4
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
@Class1.get
0;JMP
// Declare a label for the return address
(Class1.get$ret.4)
// Call Class2.get 0
// Save the return address
@Class2.get$ret.5
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
@Class2.get
0;JMP
// Declare a label for the return address
(Class2.get$ret.5)
(Class2.get$END)
@Class2.get$END
0;JMP

