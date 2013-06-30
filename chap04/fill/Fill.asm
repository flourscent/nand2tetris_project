// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

	@WD_CNT
	@CURR_PIXEL
	@SCREEN
	D=A
	@FIRST_PIXEL
	M=D
	// bit pattern white
	@PIXEL_PTN_WHT
	D=0
	M=D
	// bit pattern black
	@PIXEL_PTN_BLK
	D=0
	D=!D
	M=D

(KEYWAIT_LOOP)
	// check whether key pressed
	@KBD
	D=M
	@BLACKEN
	D;JNE
	@WHITEN
	D;JEQ
	@KEYWAIT_LOOP
	0;JMP

(BLACKEN)
	@8191
	D=A
	@WD_CNT
	M=D

	@SCREEN
	D=A
	@CURPIXEL
	M=D
(BLACKEN_LOOP)
	@WD_CNT
	D=M
	@SCREEN
	A=D+A
	D=A
	@CURR_PIXEL
	M=D

	@PIXEL_PTN_BLK
	D=M

	@CURR_PIXEL
	A=M
	M=D

	@WD_CNT
	D=M
	D=D-1
	M=D

	@KEYWAIT_LOOP
	D;JLT
	@BLACKEN_LOOP
	0;JMP

(WHITEN)
	@8191
	D=A
	@WD_CNT
	M=D
	
	@SCREEN
	D=A
	@CURPIXEL
	M=D
(WHITEN_LOOP)
	@WD_CNT
	D=M
	@SCREEN
	A=D+A
	D=A
	@CURR_PIXEL
	M=D

	@PIXEL_PTN_WHT
	D=M

	@CURR_PIXEL
	A=M
	M=D

	@WD_CNT
	D=M
	D=D-1
	M=D

	@KEYWAIT_LOOP
	D;JLT
	@WHITEN_LOOP
	0;JMP
