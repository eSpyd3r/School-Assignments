# Lim
# Ethan
# 261029610
# 1. Image Buffer base address has index 0 while the Error Buffer base address has index 3; they are in different blocks
# 2. It matters if the template buffer falls into the same block as the Error or Image buffer; being in the same block could cause contention of the same cache resources on that block, reducing hit rate; base addresses need different indexes to increase hit rate.
.data

displayBuffer:  .space 0x40000 # space for 512x256 bitmap display 
.space 0x30
errorBuffer:    .space 0x40000 # space to store match function
.space 0x10
templateBuffer: .space 0x100   # space for 8x8 template

imageFileName:    .asciiz "pxlcon512x256cropgs.raw" 
templateFileName: .asciiz "template8x8gsWaldoMod.raw"
# struct bufferInfo { int *buffer, int width, int height, char* filename }
imageBufferInfo:    .word displayBuffer  512 128  imageFileName
errorBufferInfo:    .word errorBuffer    512 128 0
templateBufferInfo: .word templateBuffer 8   8    templateFileName

.text
main:	la $a0, imageBufferInfo
	jal loadImage
	la $a0, templateBufferInfo
	jal loadImage
	la $a0, imageBufferInfo
	la $a1, templateBufferInfo
	la $a2, errorBufferInfo
	jal matchTemplateFast       # MATCHING DONE HERE
	la $a0, errorBufferInfo
	jal findBest
	la $a0, imageBufferInfo
	move $a1, $v0
	jal highlight
	la $a0, errorBufferInfo	
	jal processError
	li $v0, 10		# exit
	syscall
	

##########################################################
# matchTemplate( bufferInfo imageBufferInfo, bufferInfo templateBufferInfo, bufferInfo errorBufferInfo )
# NOTE: struct bufferInfo { int *buffer, int width, int height, char* filename }
matchTemplate:	
lw $s0 4($a0)                 # witdth of image (512); w = $s0
lw $s1 8($a0)                 # height of image (128); h = $s1
addi $s2 $s1 -8               # height of image - 8
addi $s5 $s0 -8               # width of image - 8


li $t0, 0                     # initializing y to 0; y = $t0
LoopY:                        # loop through the image height (512 - 8) times
    bgt $t0, $s2, EndLoopY    # if y > 120, exit the loop
    li $t1, 0                 # initialize x to 0; x = $t1

LoopX:
    bgt $t1, $s5, EndLoopX    # if x > 504, exit the loop
    li $t2, 0                 # initializing j to 0; j = $t2
LoopJ:
    bge $t2, 8, EndLoopJ    # if j >= 8, exit the loop
    li $t3, 0               #initializing i to 0
LoopI:
    bge $t3, 8, EndLoopI    # if i >= 8, exit the loop
    
    lw $t4 ($a2)                 # address for errorbuffer; resetting $t4
    lw $t5 ($a0)                 # address for displaybuffer; resetting $t5
    lw $t6 ($a1)                 # address for templateBuffer; resetting $t6
    
    add $s3 $t1 $t3               # x+i for Image function (col); resetting $s3
    add $s4 $t0 $t2               # y+j for Image function (row); resetting $4
    
    mul $t7, $s0, $s4             # (w * row)
    add $t7 $t7 $s3               # (w * row) + col 
    mul $t7 $t7 4                 # 4 * ((w * row) + col) 
    add $t5 $t5 $t7               # displayBuffer + 4 * ((w * row) + col) = I(x+i, y+j)
    lbu $t5 ($t5)                 # taking byte at address -> display
    
    mul $t7, $t2, 8               # (w * row)
    add $t7 $t7 $t3               # (w * row) + col
    mul $t7 $t7 4                 # 4 * ((w * row) + col)
    add $t6 $t6 $t7               # templateBuffer + 4 * ((w * row) + col) = T(i,j)
    lbu $t6 ($t6)                 # taking byte at address -> template
    
    sub $t5 $t5 $t6               # I(x+i,y+j) - T(i,j)
    abs $t5 $t5                   # abs|I(x+i,y+j) - T(i,j)|
    
    mul $t7, $s0, $t0             # (w * row)
    add $t7, $t7, $t1             # (w * row) + col
    mul $t7 $t7 4                 # 4 * ((w * row) + col)
    add $t4, $t4, $t7             # errorBuffer + 4 * ((w * row) + col) = SAD[x,y]
    lw  $t8 ($t4)
    add $t9, $t8, $t5             # abs|I(x+i,y+j) - T(i,j)| + SAD[x,y]
    
    sw $t9 ($t4)                  # storing abs|I(x+i,y+j) - T(i,j)| + SAD[x,y] into SAD[x,y]  address
    
    addi $t3, $t3, 1              # increment i by 1
    j LoopI                       # jump back to the inner loop

EndLoopI:
    addi $t2, $t2, 1              # increment j by 1
    j LoopJ                       # jump back to the middle loop

EndLoopJ:
    addi $t1, $t1, 1            # increment x by 1
    j LoopX                     # jump back to the outer loop
EndLoopX:
    addi $t0, $t0, 1                # increment y by 1
    j LoopY                         # jump back to the main loop

EndLoopY:
	jr $ra	
	
##########################################################
# matchTemplateFast( bufferInfo imageBufferInfo, bufferInfo templateBufferInfo, bufferInfo errorBufferInfo )
# NOTE: struct bufferInfo { int *buffer, int width, int height, char* filename }
matchTemplateFast:
lw $s0 4($a0)                 # witdth of image (512); w = $s0
lw $s1 8($a0)                 # height of image (128); h = $s1
addi $s2 $s1 -8               # height of image - 8
addi $s3 $s0 -8               # width of image - 8	

lw $s4 ($a2)                 # address for errorbuffer = $s4
lw $s5 ($a0)                 # address for displaybuffer = $s5

li $t8 0                      # initializing j = 0; j = $t8
LoopJFast:
bge $t8, 8, ExitLoopJFast	      # if j >= 8 EndLoopJ

addi $sp $sp 4
sw $s3 ($sp)
lw $s3 ($a1)                 # address for templateBuffer = $s3

#int t0 = T[0][j];

mul $t0, $t8, 8               # (w * j)
addi $t0 $t0 0                # (w * j) + 0
mul $t0 $t0 4                 # 4 * ((w * j) + 0)
add $t0 $s3 $t0               # templateBuffer + 4 * ((w * row) + col) = T(i,j)
lbu $t0 ($t0)                 # taking byte at address -> template

#int t1 = T[1][j];

mul $t1, $t8, 8               # (w * j)
addi $t1 $t1 1                # (w * j) + 1
mul $t1 $t1 4                 # 4 * ((w * j) + 1)
add $t1 $s3 $t1               # templateBuffer + 4 * ((w * row) + col) = T(i,j)
lbu $t1 ($t1)                 # taking byte at address -> template

#int t2 = T[2][j];
mul $t2, $t8, 8               # (w * j)
addi $t2 $t2 2                # (w * j) + 2
mul $t2 $t2 4                 # 4 * ((w * j) + 2)
add $t2 $s3 $t2               # templateBuffer + 4 * ((w * row) + col) = T(i,j)
lbu $t2 ($t2)                 # taking byte at address -> template

#int t3 = T[3][j];
mul $t3, $t8, 8               # (w * j)
addi $t3 $t3 3                # (w * j) + 3
mul $t3 $t3 4                 # 4 * ((w * j) + 3)
add $t3 $s3 $t3               # templateBuffer + 4 * ((w * row) + col) = T(i,j)
lbu $t3 ($t3)                 # taking byte at address -> template

#int t4 = T[4][j];
mul $t4, $t8, 8               # (w * j)
addi $t4 $t4 4                # (w * j) + 4
mul $t4 $t4 4                 # 4 * ((w * j) + 4)
add $t4 $s3 $t4               # templateBuffer + 4 * ((w * row) + col) = T(i,j)
lbu $t4 ($t4)                 # taking byte at address -> template

#int t5 = T[5][j];
mul $t5, $t8, 8               # (w * j)
addi $t5 $t5 5               # (w * j) + 5
mul $t5 $t5 4                 # 4 * ((w * j) + 5)
add $t5 $s3 $t5               # templateBuffer + 4 * ((w * row) + col) = T(i,j)
lbu $t5 ($t5)                 # taking byte at address -> template


#int t6 = T[6][j];
mul $t6, $t8, 8               # (w * j)
addi $t6 $t6 6                # (w * j) + 6
mul $t6 $t6 4                 # 4 * ((w * j) + 6)
add $t6 $s3 $t6               # templateBuffer + 4 * ((w * row) + col) = T(i,j)
lbu $t6 ($t6)                 # taking byte at address -> template

#int t7 = T[7][j];
mul $t7, $t8, 8               # (w * j)
addi $t7 $t7 7                # (w * j) + 7
mul $t7 $t7 4                 # 4 * ((w * j) + 7)
add $t7 $s3 $t7               # templateBuffer + 4 * ((w * row) + col) = T(i,j)
lbu $t7 ($t7)                 # taking byte at address -> template

lw $s3 ($sp)                  # returning $s3 to width - 8 
addi $sp $sp 4


li $t9 0                      # initializing y = 0; y = $t9
LoopYFast:
bgt $t9, $s2, ExitLoopYFast       # if y > height - 8
li $a3 0                      # initializing x = 0; x = $a3 
LoopXFast:
bgt $a3, $s3, ExitLoopXFast       # if x > width - 8
                                           
#$s4 = errorbuffer; row = y; DEFINING SAD[x,y]
mul $v0, $s0, $t9             # (w * row)
add $v0, $v0, $a3             # (w * row) + col
mul $v0 $v0 4                 # 4 * ((w * row) + col)
add $s7, $v0, $s4             # errorBuffer + 4 * ((w * row) + col) = SAD[x,y] = $s7; STORE HERE
lw $v1, ($s7)                 # value at $s7 = $v1... use this to add to SAD[x,y] += abs( I[x+0][y+j] - t0 )|;

#################################################
# solving for I[][]; col = x + 0 = $a3; row = y + j = $t9 + $t8
addi $sp, $sp, -4 
sw $t0 ($sp)

add $t0 $t8 $t9               # y + j = row
mul $t0, $s0, $t0             # (w * row)
add $t0, $t0, $a3             # (w * row) + col 
#addi $t0, $t0, 0             # col = x + 0
mul $t0 $t0 4                 # 4 * ((w * row) + col)
add $v0, $t0, $s5             # displayBuffer + 4 * ((w * row) + col) = I[x+0,y+j] = $t0
lbu $s6, ($v0)                # byte value of I[x+0][y+j];

lw $t0 ($sp)                  # restoring t0 = T[0][j]
addi $sp $sp 4

sub $s6 $s6 $t0               # I[x+0][y+j] - t0
abs $s6 $s6                   # abs I[x+0][y+j] - t0

lw $v1, ($s7)                 # value at $s7 = $v1... use this to add to SAD[x,y] += abs( I[x+0][y+j] - t0 )|;
add $v0 $s6 $v1               # SAD[x][y] + abs I[x+0][y+j] - t0
sw $v0 ($s7)                  # SAD[x][y] += abs I[x+0][y+j] - t0
##################
addi $sp, $sp, -4 
sw $t0 ($sp)                  # saving T[0][j]
#####################################################
# solving for I[][]; col = x + 1 = $a3; row = y + j = $t9 + $t8
add $t0 $t8 $t9               # y + j = row
mul $t0, $s0, $t0             # (w * row)
add $t0, $t0, $a3             # (w * row) + col 
addi $t0, $t0, 1              # col = x + 1
mul $t0 $t0 4                 # 4 * ((w * row) + col)
add $v0, $t0, $s5             # displayBuffer + 4 * ((w * row) + col) = I[x+1,y+j] = $t0
lbu $s6, ($v0)                # byte value of I[x+1][y+j];

sub $s6 $s6 $t1               # I[x+1][y+j] - t1
abs $s6 $s6                   # abs I[x+1][y+j] - t1

lw $v1, ($s7)                 # value at $s7 = $v1... use this to add to SAD[x,y] += abs( I[x+0][y+j] - t0 )|;
add $v0 $s6 $v1               # SAD[x][y] + abs I[x+1][y+j] - t1
sw $v0 ($s7)                  # SAD[x][y] += abs I[x+1][y+j] - t1
#####################################################
# solving for I[][]; col = x + 2 = $a3; row = y + j = $t9 + $t8
add $t0 $t8 $t9               # y + j = row
mul $t0, $s0, $t0             # (w * row)
add $t0, $t0, $a3             # (w * row) + col 
addi $t0, $t0, 2              # col = x + 2
mul $t0 $t0 4                 # 4 * ((w * row) + col)
add $v0, $t0, $s5             # displayBuffer + 4 * ((w * row) + col) = I[x+2,y+j] = $t0
lbu $s6, ($v0)                # byte value of I[x+2][y+j];

sub $s6 $s6 $t2               # I[x+2][y+j] - t2
abs $s6 $s6                   # abs I[x+2][y+j] - t2

lw $v1, ($s7)                 # value at $s7 = $v1... use this to add to SAD[x,y] += abs( I[x+0][y+j] - t0 )|;
add $v0 $s6 $v1               # SAD[x][y] + abs I[x+2][y+j] - t2
sw $v0 ($s7)                  # SAD[x][y] += abs I[x+2][y+j] - t2
#####################################################
# solving for I[][]; col = x + 3 = $a3; row = y + j = $t9 + $t8
add $t0 $t8 $t9               # y + j = row
mul $t0, $s0, $t0             # (w * row)
add $t0, $t0, $a3             # (w * row) + col 
addi $t0, $t0, 3              # col = x + 3
mul $t0 $t0 4                 # 4 * ((w * row) + col)
add $v0, $t0, $s5             # displayBuffer + 4 * ((w * row) + col) = I[x+3,y+j] = $t0
lbu $s6, ($v0)                # byte value of I[x+3][y+j];

sub $s6 $s6 $t3               # I[x+3][y+j] - t2
abs $s6 $s6                   # abs I[x+3][y+j] - t2

lw $v1, ($s7)                 # value at $s7 = $v1... use this to add to SAD[x,y] += abs( I[x+0][y+j] - t0 )|;
add $v0 $s6 $v1               # SAD[x][y] + abs I[x+3][y+j] - t3
sw $v0 ($s7)                  # SAD[x][y] += abs I[x+3][y+j] - t3
#####################################################
# solving for I[][]; col = x + 4 = $a3; row = y + j = $t9 + $t8
add $t0 $t8 $t9               # y + j = row
mul $t0, $s0, $t0             # (w * row)
add $t0, $t0, $a3             # (w * row) + col 
addi $t0, $t0, 4              # col = x + 4
mul $t0 $t0 4                 # 4 * ((w * row) + col)
add $v0, $t0, $s5             # displayBuffer + 4 * ((w * row) + col) = I[x+4,y+j] = $t0
lbu $s6, ($v0)                # byte value of I[x+4][y+j];

sub $s6 $s6 $t4               # I[x+4][y+j] - t4
abs $s6 $s6                   # abs I[x+4][y+j] - t4

lw $v1, ($s7)                 # value at $s7 = $v1... use this to add to SAD[x,y] += abs( I[x+0][y+j] - t0 )|;
add $v0 $s6 $v1               # SAD[x][y] + abs I[x+4][y+j] - t4
sw $v0 ($s7)                  # SAD[x][y] += abs I[x+4][y+j] - t4
#####################################################
# solving for I[][]; col = x + 5 = $a3; row = y + j = $t9 + $t8
add $t0 $t8 $t9               # y + j = row
mul $t0, $s0, $t0             # (w * row)
add $t0, $t0, $a3             # (w * row) + col 
addi $t0, $t0, 5              # col = x + 5
mul $t0 $t0 4                 # 4 * ((w * row) + col)
add $v0, $t0, $s5             # displayBuffer + 4 * ((w * row) + col) = I[x+5,y+j] = $t0
lbu $s6, ($v0)                # byte value of I[x+5][y+j];

sub $s6 $s6 $t5               # I[x+5][y+j] - t5
abs $s6 $s6                   # abs I[x+5][y+j] - t5

lw $v1, ($s7)                 # value at $s7 = $v1... use this to add to SAD[x,y] += abs( I[x+0][y+j] - t0 )|;
add $v0 $s6 $v1               # SAD[x][y] + abs I[x+5][y+j] - t5
sw $v0 ($s7)                  # SAD[x][y] += abs I[x+5][y+j] - t5
#####################################################
# solving for I[][]; col = x + 6 = $a3; row = y + j = $t9 + $t8
add $t0 $t8 $t9               # y + j = row
mul $t0, $s0, $t0             # (w * row)
add $t0, $t0, $a3             # (w * row) + col 
addi $t0, $t0, 6              # col = x + 6
mul $t0 $t0 4                 # 4 * ((w * row) + col)
add $v0, $t0, $s5             # displayBuffer + 4 * ((w * row) + col) = I[x+6,y+j] = $t0
lbu $s6, ($v0)                # byte value of I[x+6][y+j];

sub $s6 $s6 $t6               # I[x+6][y+j] - t6
abs $s6 $s6                  # abs I[x+6][y+j] - t6

lw $v1, ($s7)                 # value at $s7 = $v1... use this to add to SAD[x,y] += abs( I[x+0][y+j] - t0 )|;
add $v0 $s6 $v1               # SAD[x][y] + abs I[x+6][y+j] - t6
sw $v0 ($s7)                  # SAD[x][y] += abs I[x+6][y+j] - t6
#####################################################
# solving for I[][]; col = x + 7 = $a3; row = y + j = $t9 + $t8
add $t0 $t8 $t9               # y + j = row
mul $t0, $s0, $t0             # (w * row)
add $t0, $t0, $a3             # (w * row) + col 
addi $t0, $t0, 7              # col = x + 7
mul $t0 $t0 4                 # 4 * ((w * row) + col)
add $v0, $t0, $s5             # displayBuffer + 4 * ((w * row) + col) = I[x+7,y+j] = $t0
lbu $s6, ($v0)                # byte value of I[x+7][y+j];

sub $s6 $s6 $t7               # I[x+7][y+j] - t7
abs $s6 $s6                   # abs I[x+7][y+j] - t7

lw $v1, ($s7)                 # value at $s7 = $v1... use this to add to SAD[x,y] += abs( I[x+0][y+j] - t0 )|;
add $v0 $s6 $v1               # SAD[x][y] + abs I[x+7][y+j] - t7
sw $v0 ($s7)                  # SAD[x][y] += abs I[x+7][y+j] - t7
#####################################################
lw $t0 ($sp)                  # restoring t0 = T[0][j]
addi $sp $sp 4

addi $a3 $a3 1                # increment x by 1
j LoopXFast                       # go back to beginning of for x loop   
				
ExitLoopXFast:
addi $t9 $t9 1                # increment y by 1
j LoopYFast			      # go back to beginnning of for y loop
						
ExitLoopYFast:
addi $t8, $t8, 1              # increment j by 1
j LoopJFast                       # go back to beginnning of for j loop
		               
ExitLoopJFast:	
	jr $ra	              # once for j reaches 8, exit
		
###############################################################
# loadImage( bufferInfo* imageBufferInfo )
# NOTE: struct bufferInfo { int *buffer, int width, int height, char* filename }
loadImage:	lw $a3, 0($a0)  # int* buffer
		lw $a1, 4($a0)  # int width
		lw $a2, 8($a0)  # int height
		lw $a0, 12($a0) # char* filename
		mul $t0, $a1, $a2 # words to read (width x height) in a2
		sll $t0, $t0, 2	  # multiply by 4 to get bytes to read
		li $a1, 0     # flags (0: read, 1: write)
		li $a2, 0     # mode (unused)
		li $v0, 13    # open file, $a0 is null-terminated string of file name
		syscall
		move $a0, $v0     # file descriptor (negative if error) as argument for read
  		move $a1, $a3     # address of buffer to which to write
		move $a2, $t0	  # number of bytes to read
		li  $v0, 14       # system call for read from file
		syscall           # read from file
        		# $v0 contains number of characters read (0 if end-of-file, negative if error).
        		# We'll assume that we do not need to be checking for errors!
		# Note, the bitmap display doesn't update properly on load, 
		# so let's go touch each memory address to refresh it!
		move $t0, $a3	   # start address
		add $t1, $a3, $a2  # end address
loadloop:	lw $t2, ($t0)
		sw $t2, ($t0)
		addi $t0, $t0, 4
		bne $t0, $t1, loadloop
		jr $ra
		
		
#####################################################
# (offset, score) = findBest( bufferInfo errorBuffer )
# Returns the address offset and score of the best match in the error Buffer
findBest:	lw $t0, 0($a0)     # load error buffer start address	
		lw $t2, 4($a0)	   # load width
		lw $t3, 8($a0)	   # load height
		addi $t3, $t3, -7  # height less 8 template lines minus one
		mul $t1, $t2, $t3
		sll $t1, $t1, 2    # error buffer size in bytes	
		add $t1, $t0, $t1  # error buffer end address
		li $v0, 0		# address of best match	
		li $v1, 0xffffffff 	# score of best match	
		lw $a1, 4($a0)    # load width
        		addi $a1, $a1, -7 # initialize column count to 7 less than width to account for template
fbLoop:		lw $t9, 0($t0)        # score
		sltu $t8, $t9, $v1    # better than best so far?
		beq $t8, $zero, notBest
		move $v0, $t0
		move $v1, $t9
notBest:		addi $a1, $a1, -1
		bne $a1, $0, fbNotEOL # Need to skip 8 pixels at the end of each line
		lw $a1, 4($a0)        # load width
        		addi $a1, $a1, -7     # column count for next line is 7 less than width
        		addi $t0, $t0, 28     # skip pointer to end of line (7 pixels x 4 bytes)
fbNotEOL:	add $t0, $t0, 4
		bne $t0, $t1, fbLoop
		lw $t0, 0($a0)     # load error buffer start address	
		sub $v0, $v0, $t0  # return the offset rather than the address
		jr $ra
		

#####################################################
# highlight( bufferInfo imageBuffer, int offset )
# Applies green mask on all pixels in an 8x8 region
# starting at the provided addr.
highlight:	lw $t0, 0($a0)     # load image buffer start address
		add $a1, $a1, $t0  # add start address to offset
		lw $t0, 4($a0) 	# width
		sll $t0, $t0, 2	
		li $a2, 0xff00 	# highlight green
		li $t9, 8	# loop over rows
highlightLoop:	lw $t3, 0($a1)		# inner loop completely unrolled	
		and $t3, $t3, $a2
		sw $t3, 0($a1)
		lw $t3, 4($a1)
		and $t3, $t3, $a2
		sw $t3, 4($a1)
		lw $t3, 8($a1)
		and $t3, $t3, $a2
		sw $t3, 8($a1)
		lw $t3, 12($a1)
		and $t3, $t3, $a2
		sw $t3, 12($a1)
		lw $t3, 16($a1)
		and $t3, $t3, $a2
		sw $t3, 16($a1)
		lw $t3, 20($a1)
		and $t3, $t3, $a2
		sw $t3, 20($a1)
		lw $t3, 24($a1)
		and $t3, $t3, $a2
		sw $t3, 24($a1)
		lw $t3, 28($a1)
		and $t3, $t3, $a2
		sw $t3, 28($a1)
		add $a1, $a1, $t0	# increment address to next row	
		add $t9, $t9, -1		# decrement row count
		bne $t9, $zero, highlightLoop
		jr $ra

######################################################
# processError( bufferInfo error )
# Remaps scores in the entire error buffer. The best score, zero, 
# will be bright green (0xff), and errors bigger than 0x4000 will
# be black.  This is done by shifting the error by 5 bits, clamping
# anything bigger than 0xff and then subtracting this from 0xff.
processError:	lw $t0, 0($a0)     # load error buffer start address
		lw $t2, 4($a0)	   # load width
		lw $t3, 8($a0)	   # load height
		addi $t3, $t3, -7  # height less 8 template lines minus one
		mul $t1, $t2, $t3
		sll $t1, $t1, 2    # error buffer size in bytes	
		add $t1, $t0, $t1  # error buffer end address
		lw $a1, 4($a0)     # load width as column counter
        		addi $a1, $a1, -7  # initialize column count to 7 less than width to account for template
pebLoop:		lw $v0, 0($t0)        # score
		srl $v0, $v0, 5       # reduce magnitude 
		slti $t2, $v0, 0x100  # clamp?
		bne  $t2, $zero, skipClamp
		li $v0, 0xff          # clamp!
skipClamp:	li $t2, 0xff	      # invert to make a score
		sub $v0, $t2, $v0
		sll $v0, $v0, 8       # shift it up into the green
		sw $v0, 0($t0)
		addi $a1, $a1, -1        # decrement column counter	
		bne $a1, $0, pebNotEOL   # Need to skip 8 pixels at the end of each line
		lw $a1, 4($a0)        # load width to reset column counter
        		addi $a1, $a1, -7     # column count for next line is 7 less than width
        		addi $t0, $t0, 28     # skip pointer to end of line (7 pixels x 4 bytes)
pebNotEOL:	add $t0, $t0, 4
		bne $t0, $t1, pebLoop
		jr $ra
