#!/usr/bin/python

import sys

# address table
symbolStartAddr = 16

lTable = {
 'SP':'0',
 'LCL':'1',
 'ARG':'2',
 'THIS':'3',
 'THAT':'4',
 'R0':'0',
 'R1':'1',
 'R2':'2',
 'R3':'3',
 'R4':'4',
 'R5':'5',
 'R6':'6',
 'R7':'7',
 'R8':'8',
 'R9':'9',
 'R10':'10',
 'R11':'11',
 'R12':'12',
 'R13':'13',
 'R14':'14',
 'R15':'15',
 'SCREEN':'16384',
 'KBD':'24576'
}

compCodes = {
'0'  :'0101010',
'1'  :'0111111',
'-1' :'0111010',
'D'  :'0001100',
'A'  :'0110000',
'!D' :'0001101',
'!A' :'0110001',
'-D' :'0001111',
'-A' :'0110011',
'D+1':'0011111',
'A+1':'0110111',
'D-1':'0001110',
'A-1':'0110010',
'D+A':'0000010',
'D-A':'0010011',
'A-D':'0000111',
'D&A':'0000000',
'D|A':'0010101',
'M'  :'1110000',
'!M' :'1110001',
'-M' :'1110011',
'M+1':'1110111',
'M-1':'1110010',
'D+M':'1000010',
'D-M':'1010011',
'M-D':'1000111',
'D&M':'1000000',
'D|M':'1010101'
}

jumpCodes = {
 'null':'000',
 'JGT' :'001',
 'JEQ' :'010',
 'JGE' :'011',
 'JLT' :'100',
 'JNE' :'101',
 'JLE' :'110',
 'JMP' :'111'
}

destCodes = {
 'null':'000',
 'M'  :'001',
 'D'  :'010',
 'MD' :'011',
 'A'  :'100',
 'AM' :'101',
 'AD' :'110',
 'AMD':'111'
}

# main driver
def main():
  ARGS_REQUIRED = 2
  ARGS_WITH_OUTPUT = 3

  if len(sys.argv) < ARGS_REQUIRED:
    print "invalid argument"
    print "Usage : " + sys.argv[0] + " asmFile.asm [hackFile.hack]"
    return 1
  
  # input / output
  inputFileName = sys.argv[1];
  if len(sys.argv) < ARGS_WITH_OUTPUT:
    outputFileName = inputFileName[0:-3] + "hack"
  else:
    outputFileName = sys.argv[2];

  try:
    inputFile = open(inputFileName, 'r')
  except IOError:
    print "[ERROR] : " + inputFileName + " doesn't exist."
  outputFile = open(outputFileName, 'w');

  parsed = parse(inputFile)
  
  translated = translate(parsed)
  writeToFile(outputFile, translated)

def writeToFile(outputFile, translated):
  for line in translated:
    outputFile.write(line + '\r\n')

def translate(parsed):
  translatedLines = []

  for parsedLine in parsed:
    instType = parsedLine['inst']
    translatedLine = ''
    if instType == 'a':
      translatedLine = '0' + "{0:015b}".format(int(parsedLine['addr']))
    elif instType == 'c':
      translatedLine = '111' + compCodes[parsedLine['comp']] + destCodes[parsedLine['dest']] + jumpCodes[parsedLine['jump']]
    translatedLines.append(translatedLine)
  return translatedLines
      
# parse
def parse(inputFile):
  global symbolStartAddr
  lines = preprocess(inputFile.readlines())

  parsedLines = []

  instCount = 0

  # first pass
  for line in lines:
    parsedLine = {}

    if line.startswith('@'):
    # a inst -- @ADDR, @LABEL
      parsedLine['inst'] = 'a'
      parsedLine['addr'] = line[1:]
      parsedLines.append(parsedLine)
      instCount+=1
    elif line.startswith('(') and line.endswith(')'):
    # label -- (LABEL)
      parsedLine['inst']='l'
      label = line[1:-1]
      if label not in lTable:
        lTable[label] = instCount
    elif line.find(';') != -1 or line.find('=') != -1:
    # c inst -- dest=comp;jump, comp;jump, dest=comp
      parsedLine['inst']='c'
      posSemicolon = line.find(';');
      posEqual = line.find('=');
      if posSemicolon != -1 and posEqual != -1:
        parsedLine['dest'] = line[0:posEqual].strip()
        parsedLine['comp'] = line[posEqual:posSemicolon-1].strip()
        parsedLine['jump'] = line[posSemicolon+1:].strip()
      elif posSemicolon != -1:
        parsedLine['comp'] = line[0:posSemicolon].strip()
        parsedLine['dest'] = 'null'
        parsedLine['jump'] = line[posSemicolon+1:].strip()
      elif posEqual != -1:
        parsedLine['comp'] = line[posEqual+1:].strip()
        parsedLine['dest'] = line[0:posEqual].strip()
        parsedLine['jump'] = 'null'
      parsedLines.append(parsedLine)
      instCount += 1

  # second pass
  for parsedLine in parsedLines:
    if parsedLine['inst'] == 'a' and not parsedLine['addr'].isdigit():
      if parsedLine['addr'] in lTable:
        parsedLine['addr'] = lTable[parsedLine['addr']]
      else:
        lTable[parsedLine['addr']] = symbolStartAddr
        parsedLine['addr'] = symbolStartAddr
        symbolStartAddr += 1

  return parsedLines

# preprocess -- strip, remove comments
def preprocess(lines):
  processed = map(lambda line : line.strip(), lines)
  inlineComment = map(lambda line : line[0:len(line) if line.find("//") < 0 else line.find("//")], processed)
  comment = filter(lambda x : len(x.strip()) != 0, inlineComment)
  return comment

if __name__ == "__main__":
  main()
