#Ethan Lim 261029610
.data
bitmapDisplay: .space 0x80000 # enough memory for a 512x256 bitmap display
resolution: .word  512 256    # width and height of the bitmap display

windowlrbt: 
.float -2.5 2.5 -1.25 1.25  					# good window for viewing Julia sets
#.float -3 2 -1.25 1.25  					# good window for viewing full Mandelbrot set
#.float -0.807298 -0.799298 -0.179996 -0.175996 		# double spiral
#.float -1.019741354 -1.013877846  -0.325120847 -0.322189093 	# baby Mandelbrot
 
bound: .float 100	# bound for testing for unbounded growth during iteration
maxIter: .word 16	# maximum iteration count to be used by drawJulia and drawMandelbrot
scale: .word 16		# scale parameter used by computeColour

# Julia constants for testing, or likewise for more examples see
# https://en.wikipedia.org/wiki/Julia_set#Quadratic_polynomials  
JuliaC0:  .float 0    0    # should give you a circle, a good test, though boring!
JuliaC1:  .float 0.25 0.5 
JuliaC2:  .float 0    0.7 
JuliaC3:  .float 0    0.8 

# a demo starting point for iteration tests
z0: .float  1 0

# TODO: define various constants you need in your .data segment here
newLine:        .asciiz "\n"
imaginaryUnit:  .asciiz " i"
complexSeparator:  .asciiz " + "
########################################################################################
.text
	
	# TODO: Write your function testing code here
main:
    
   #li $a0 10
   #la $t0 JuliaC1
   #lwc1 $f12 ($t0)
   #lwc1 $f13 4($t0)
   #la $t0 z0
   #lwc1 $f14 ($t0)
   #lwc1 $f15 4($t0)
   #jal iterateVerbose
     
    la $t0 JuliaC1
    lwc1 $f12, ($t0)
    lwc1 $f13, 4($t0)
    jal drawJulia
    
   #li $a0 256
   #li $a1 128
   #jal pixel2ComplexInWindow
   #mov.s $f12 $f0
   #mov.s $f13 $f1
  # jal printComplex
    
    li   $v0, 10  # exit program
    syscall
 
    
printComplex:
    addi $sp $sp -8
    swc1 $f12 ($sp)  #since we need to push $f13 to $f12 for syscall. we don't necessarily want to change $f12 since we are just printing?
    swc1 $f13 4($sp)
    sw   $a0 8($sp)
 
    mov.s $f12, $f12	       # Could work without this line; $f12 is the real part and is always printed first
    li   $v0, 2                # set syscall to print float
    syscall                    # print the real part of the complex number
    
    la   $a0, complexSeparator # load the string " + " into $a0
    li   $v0, 4                # set syscall to print string
    syscall                    # print the string " + "
    
    li   $v0, 2                # set syscall to print float
    mov.s $f12, $f13           # move the imaginary part into $f12 for printing
    syscall                    # print the imaginary part of the complex number
    
    la   $a0, imaginaryUnit    # load the string "i\n" into $a0
    li   $v0, 4                # set syscall to print string
    syscall                    # print the string "i"
    
    lwc1 $f12 ($sp) #restoring $f12
    lwc1 $f13 4($sp)
    lw   $a0 8($sp)
    addi $sp $sp 8 #restoring stack
    
    jr   $ra                   # return
printNewLine:
    addi $sp $sp -4
    sw $a0 ($sp)
    la   $a0, newLine          # load the newline string
    syscall                    # print the newline using syscall
    
    lw  $a0 ($sp)
    addi $sp $sp 4
    jr   $ra                   # return
      
multComplex:
    addi $sp $sp -32
    swc1 $f12 ($sp)
    swc1 $f13 4($sp)
    swc1 $f14 8($sp)
    swc1 $f15 12($sp)
    
    mul.s $f0, $f12, $f14      # ac
    mul.s $f1, $f13, $f15      # bd FIX THESE CONVENTIONS LATER
    mul.s $f4, $f12, $f15      # ad
    mul.s $f5, $f13, $f14      # bc
    sub.s $f0, $f0, $f1        # ac - bd real part
    add.s $f1, $f4, $f5        # ad + bc imaginary part
    
    lwc1 $f12 ($sp)
    lwc1 $f13 4($sp)
    lwc1 $f14 8($sp)
    lwc1 $f15 12($sp)
    addi $sp $sp 32
    jr $ra
    
iterateVerbose:
    addi $sp, $sp, -16         
    swc1 $f12, 0($sp)           # saving arguments to stack as per pdf
    swc1 $f13, 4($sp)           
    swc1 $f14, 8($sp)
    swc1 $f15, 12($sp)
    sw  $ra,  16($sp)	       #saving return address to stack to call back to main
    
    mov.s $f8, $f12           # move a into $f8
    mov.s $f9, $f13           # move b into $f9
    mov.s $f12, $f14           # move x0 into $f12
    mov.s $f13, $f15           # move y0 into $f13
    
    la $t1, bound
    lwc1 $f7, ($t1)            #loading bound to $f7
    
    li $t1, 1                  # initialize iteration count to 1
iterateVerboseLoop:
    
    mov.s $f14, $f12           # move x0 into $f12 
    mov.s $f15, $f13           # move y0 into $f14
    
    jal printComplex
    jal printNewLine
    jal multComplex            #We are squaring x0 and y0!
    
    add.s $f12, $f0, $f8       #real part of z^2 + c
    add.s $f13, $f1, $f9	#imaginary part of z^2 + c
    
    mul.s $f4, $f12, $f12     # x^2
    mul.s $f5, $f13, $f13     # y^2
    
    add.s $f16, $f4, $f5     # x^2 + y^2
    c.lt.s $f7, $f16         # check if (x^2 + y^2) > bound
    bc1t endIterationVerboseSubtract       
    
    beq $t1, $a0, endIterationVerbose # check if iteration count = n
    
    addi $t1, $t1, 1           # increment iteration count
    j iterateVerboseLoop

endIterationVerboseSubtract:
    subi $t1, $t1, 1
endIterationVerbose:
    move $v0, $t1              # move iteration count into $v0 to return
    move $a0 $v0
    li $v0 1
    syscall
    lwc1 $f12, 0($sp)           
    lwc1 $f13, 4($sp)           
    lwc1 $f14, 8($sp)
    lwc1 $f15, 12($sp)
    lw  $ra, 16($sp)	       
    addi $sp $sp 16
    jr $ra

iterate:
    addi $sp $sp -64
    swc1 $f12, 0($sp)           # saving arguments to stack as per pdf
    swc1 $f13, 4($sp)           
    swc1 $f14, 8($sp)
    swc1 $f15, 12($sp)
    sw  $ra, 16($sp)	       #saving return address to stack to call back to main
    
    
    mov.s $f8, $f12            # move a into $f8
    mov.s $f9, $f13           # move b into $f9
    mov.s $f12, $f14           # move x0 into $f12
    mov.s $f13, $f15          # move y0 into $f13
    
    la $t1, bound
    lwc1 $f7, ($t1)            #loading bound to $f7
    
    li $t1, 1                  # initialize iteration count to 1
    
iterateLoop:
    
    mov.s $f14, $f12           # move x0 into $f12 
    mov.s $f15, $f13           # move y0 into $f14

    jal multComplex            #We are squaring x0 and y0!
    
    add.s $f12, $f0, $f8       #real part of z^2 + c
    add.s $f13, $f1, $f9	#imaginary part of z^2 + c
    
    mul.s $f4, $f12, $f12     # x^2
    mul.s $f5, $f13, $f13     # y^2
    
    add.s $f16, $f4, $f5     # x^2 + y^2
    c.lt.s $f7, $f16         # check if (x^2 + y^2) > bound
    bc1t endIterationSubtract       
    
    beq $t1, $a0, endIteration # check if iteration count = n
    
    addi $t1, $t1, 1           # increment iteration count
    j iterateLoop
endIterationSubtract:
    subi $t1, $t1, 1    
endIteration:
    move $v0, $t1              # move iteration count into $v0 to return
    lwc1 $f12, 0($sp)           
    lwc1 $f13, 4($sp)           
    lwc1 $f14, 8($sp)
    lwc1 $f15, 12($sp)
    lw  $ra, 16($sp)	       
    addi $sp $sp 64
    jr $ra

#a0: col, a1: row
pixel2ComplexInWindow:
     
    la   $t0, resolution
    lw   $t1, ($t0)       #width of resolution
    
    mtc1 $t1, $f4          #loading w
    cvt.s.w $f4 $f4   
    lw   $t1, 4($t0)       #height of resolution
    mtc1 $t1, $f5	   #loading h
    cvt.s.w $f5 $f5
    
    la   $t0, windowlrbt
    lwc1 $f6, ($t0)          #loading l
    lwc1 $f7, 4($t0)         #loading r
    lwc1 $f8, 8($t0)         #loading b
    lwc1 $f9, 12($t0)        #loading t
    
    
    mtc1    $a0, $f18         #storing col argument as float in $f18
    cvt.s.w $f10, $f18        #covert int col to float
    mtc1    $a1, $f17         #storing row argument as float in $f17
    cvt.s.w $f11, $f17        #covert int row to float

  
    div.s $f10, $f10, $f4     # col/w
    sub.s $f7, $f7, $f6       # (r-l)
    mul.s $f10, $f10, $f7     # col/w * (r-l)
    add.s $f10, $f10, $f6     # col/w * (r-l) + l 
    
    div.s $f11, $f11, $f5     # row/h
    sub.s $f9, $f9, $f8       # (t-b)
    mul.s $f11, $f11, $f9     # row/h * (t-b)
    add.s $f11, $f11, $f8     # row/h * (t-b) + b 

    mov.s $f0, $f10            #returning x to $f0
    mov.s $f1, $f11            #returning y to $f1
    
    jr $ra                     # return

drawJulia: #f12 is float a, f13 is float b, t4 is col, t5 is row
    addi $sp $sp -8
    swc1 $f12, 0($sp)           # saving arguments to stack as per pdf
    swc1 $f13, 4($sp)
    sw $ra 8($sp)
    
    la $t0, resolution
    lw $s1, ($t0) #loading w into $s1
    lw $s2, 4($t0) #loading h into $s2
    
    subi $s1 $s1 1 #since we count index zero
    subi $s2 $s2 1  
    
    la $t7, bitmapDisplay
    
    li $t4, 0 #initializing row
drawJuliaLoopOuter:
    beq $t4, $s2, endJuliaLoopOuter  #if row >= resolution height
    li  $t5, 0 #initializing col
drawJuliaLoopInner:
    beq $t5, $s1, endJuliaInner #if col >= resolution width
    move $a0 $t5
    move $a1 $t4
    jal pixel2ComplexInWindow #taking $a0 (col) and $a1 (row) as input, calculating a starting point for each pixel; returns $f0 and $f1 as starting points
    mov.s $f14 $f0
    mov.s $f15 $f1 #pixel2ComplexInWindow returned starting point loaded to $f14 and $f15 to pass through iterate
    la $t0, maxIter
    lw $a0, ($t0) #saving maxIter to pass to iterate
    jal iterate #iteration count is in $v0
    beq $a0 $v0 maxIterReached #if maxIter == n
    move $a0 $v0
    jal computeColour #color stored in $v0

    sw $v0 ($t7)        #sets color to pixel
    addi $t7, $t7, 4  #incrementing bitmap display to next pixel
    addi $t5, $t5, 1  #incrementing col
    j drawJuliaLoopInner
endJuliaInner:   
    addi $t4, $t4, 1  #incrementing rows by 1
    j drawJuliaLoopOuter               
maxIterReached:
    sw $0 ($t7)         #sets color to black
    addi $t7, $t7, 4  #incrementing bitmap display to next pixel
    addi $t5, $t5, 1  #incrementing rows
    j drawJuliaLoopInner
endJuliaLoopOuter:
    lwc1 $f12 ($sp) #restoring $f12
    lwc1 $f13 4($sp)
    lw   $ra  8($sp)
    addi $sp $sp 8 
    jr $ra

drawMandelbrot: #f12 is float a, f13 is float b, t4 is col, t5 is row
    addi $sp $sp -8
    swc1 $f12, 0($sp)           # saving arguments to stack as per pdf
    swc1 $f13, 4($sp)
    sw $ra 8($sp)
    
    la $t0, resolution
    lw $s1, ($t0) #loading w into $s1
    lw $s2, 4($t0) #loading h into $s2
    
    subi $s1 $s1 1 #since we count index zero
    subi $s2 $s2 1  
    
    la $t7, bitmapDisplay
    
    li $t4, 0 #initializing row
drawMandelbrotLoopOuter:
    beq $t4, $s2, endMandelbrotLoopOuter  #if row >= resolution height
    li  $t5, 0 #initializing col
drawMandelbrotLoopInner:
    beq $t5, $s1, endMandelbrotInner #if col >= resolution width
    lwc1 $f12 ($sp)
    lwc1 $f13 4($sp)
    move $a0 $t5
    move $a1 $t4
    jal pixel2ComplexInWindow #taking $a0 (col) and $a1 (row) as input, calculating a starting point for each pixel; returns $f0 and $f1 as starting points
    li $t0, 0
    mtc1 $t0, $f14
    mtc1 $t0, $f15
    mov.s $f12 $f0
    mov.s $f13 $f1 #pixel2ComplexInWindow returned starting point loaded to $f12 and $f13 to pass through iterate
    la $t0, maxIter
    lw $a0, ($t0) #saving maxIter to pass to iterate
    jal iterate #now takes $f0 and $f1 as $f12 and $f13 as arguments and 0.0 as $f14 and $f15; iteration count is in $v0
    beq $a0 $v0 maxIterReachedMandel #if maxIter == n
    move $a0 $v0
    jal computeColour #color stored in $v0

    sw $v0 ($t7)        #sets color to pixel
    addi $t7, $t7, 4  #incrementing bitmap display to next pixel
    addi $t5, $t5, 1  #incrementing col
    j drawMandelbrotLoopInner
endMandelbrotInner:   
    addi $t4, $t4, 1  #incrementing rows by 1
    j drawMandelbrotLoopOuter               
maxIterReachedMandel:
    sw $0 ($t7)         #sets color to black
    addi $t7, $t7, 4  #incrementing bitmap display to next pixel
    addi $t5, $t5, 1  #incrementing rows
    j drawMandelbrotLoopInner
endMandelbrotLoopOuter:
    lwc1 $f12 ($sp) #restoring $f12
    lwc1 $f13 4($sp)
    lw   $ra  8($sp)
    addi $sp $sp 8 
    jr $ra


########################################################################################
# Computes a colour corresponding to a given iteration count in $a0
# The colours cycle smoothly through green blue and red, with a speed adjustable 
# by a scale parametre defined in the static .data segment
computeColour:
	la $t0 scale
	lw $t0 ($t0)
	mult $a0 $t0
	mflo $a0
ccLoop:
	slti $t0 $a0 256
	beq $t0 $0 ccSkip1
	li $t1 255
	sub $t1 $t1 $a0
	sll $t1 $t1 8
	add $v0 $t1 $a0
	jr $ra
ccSkip1:
  	slti $t0 $a0 512
	beq $t0 $0 ccSkip2
	addi $v0 $a0 -256
	li $t1 255
	sub $t1 $t1 $v0
	sll $v0 $v0 16
	or $v0 $v0 $t1
	jr $ra
ccSkip2:
	slti $t0 $a0 768
	beq $t0 $0 ccSkip3
	addi $v0 $a0 -512
	li $t1 255
	sub $t1 $t1 $v0
	sll $t1 $t1 16
	sll $v0 $v0 8
	or $v0 $v0 $t1
	jr $ra
ccSkip3:
 	addi $a0 $a0 -768
 	j ccLoop
