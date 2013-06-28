// test for ALUNotZero16.hdl

load ALUNotZero16.hdl,
output-file ALUNotZero16.out,
compare-to ALUNotZero16.cmp,
output-list in%B1.16.1 notflag%B4.1.4 zeroflag%B4.1.4 out%B1.16.1;

// test all flag off
set in      %B0000000011111111,
set notflag  0,
set zeroflag 0,
eval,
output;

// test notflag
set in      %B0000000011111111,
set notflag  1,
set zeroflag 0,
eval,
output;

// test zeroflag
set in       %B0000000011111111,
set notflag  0,
set zeroflag 1,
eval,
output;

// test both flag on, then output is all true
set in       %B0000000011111111,
set notflag  1,
set zeroflag 1,
eval,
output;
