#!/usr/bin/python

# VMTranslator for 'push constant NUM' commands

ARGS_WITH_OUTPUT = 3

cmdTypes = {
  'push': 'stackop',
  'pop' : 'stackop',
  'add' : 'operari',
  'sub' : 'operari',
  'neg' : 'operari',
  'eq'  : 'operlog',
  'gt'  : 'operlog',
  'lt'  : 'operlog',
  'and' : 'operbit',
  'or'  : 'operbit',
  'not' : 'operbit'
}

commandPtns = {
  'stckInit':'@256\r\nD=A\r\n@0\r\nM=D\r\n',

  'stackop' : {
    'push':{
      'constant' : '@__INDEX__\r\nD=A\r\n@0\r\nA=M\r\nM=D\r\n@0\r\nM=M+1\r\n'
    },
  },
  'operlog':{
    'eq' : '---POP2REGD---D=M-D\r\n@SETTRUE__BRANCHCNT__\r\nD;JEQ\r\n@SETFALSE__BRANCHCNT__\r\nD;JNE\r\n(SETTRUE__BRANCHCNT__)\r\n@0\r\nA=M-1\r\nM=-1\r\n@SETEND__BRANCHCNT__\r\n0;JMP\r\n(SETFALSE__BRANCHCNT__)\r\n@0\r\nA=M-1\r\nM=0\r\n(SETEND__BRANCHCNT__)\r\n',
    'lt' : '---POP2REGD---D=M-D\r\n@SETTRUE__BRANCHCNT__\r\nD;JLT\r\n@SETFALSE__BRANCHCNT__\r\nD;JGE\r\n(SETTRUE__BRANCHCNT__)\r\n@0\r\nA=M-1\r\nM=-1\r\n@SETEND__BRANCHCNT__\r\n0;JMP\r\n(SETFALSE__BRANCHCNT__)\r\n@0\r\nA=M-1\r\nM=0\r\n(SETEND__BRANCHCNT__)\r\n',
    'gt' : '---POP2REGD---D=M-D\r\n@SETTRUE__BRANCHCNT__\r\nD;JGT\r\n@SETFALSE__BRANCHCNT__\r\nD;JLE\r\n(SETTRUE__BRANCHCNT__)\r\n@0\r\nA=M-1\r\nM=-1\r\n@SETEND__BRANCHCNT__\r\n0;JMP\r\n(SETFALSE__BRANCHCNT__)\r\n@0\r\nA=M-1\r\nM=0\r\n(SETEND__BRANCHCNT__)\r\n'
  },
  'operari':{
    'add' : '---POP2REGD---M=M+D\r\n',
    'sub' : '---POP2REGD---M=M-D\r\n',
    'neg' : '@0\r\nA=M-1\r\nM=-M\r\n'
  },
  'operbit':{
    'and' : '---POP2REGD---M=M&D\r\n',
    'or'  : '---POP2REGD---M=M|D\r\n',
    'not' : 'A=M-1\r\nM=!M\r\n'
    },

  'ptns': {
    '---POP2REGD---' : '@0\r\nA=M-1\r\nD=M\r\nM=0\r\n@0\r\nM=M-1\r\nA=M-1\r\n'
  }
}

import sys

def main():
  ARGS_REQUIRED = 2
  if len(sys.argv) < ARGS_REQUIRED:
    print "invalid argument"
    print "Usage : " + sys.argv[0] + " vmFile.vm [outputFile [init?]] "
    return 1
  files = openFiles(sys.argv)
  settings = config(sys.argv)
  parsed = parse(files['in'])
  translated = translate(parsed, settings)
  writeToFile(files['out'], translated)
  
def openFiles(argv):
  # input / output
  global ARGS_WITH_OUTPUT
  inputFileName = argv[1];
  if len(sys.argv) < ARGS_WITH_OUTPUT:
    outputFileName = inputFileName[0:-2] + "asm"
  else:
    outputFileName = argv[2];
  try:
    inputFile = open(inputFileName, 'r')
  except IOError:
    print "[ERROR] : " + inputFileName + " doesn't exist."
  outputFile = open(outputFileName, 'w');

  files = {}
  files['in'] = inputFile
  files['out'] = outputFile
  return files

def config(argv):
  initSettings = {}
  if len(argv) > 3:
    initSettings['stckInit'] = argv[3] == 'y'
  return initSettings

# parse vm commands
def parse(inputFile):
  lines = preprocess(inputFile.readlines())
  parsedLines = []

  for line in lines:
    splitedLine = line.split()
    parsedLine = {}
    parsedLine['cmdType'] = cmdTypes[splitedLine[0]]
    parsedLine['cmd'] = splitedLine[0]
    if parsedLine['cmdType'] == 'stackop':
      parsedLine['segment'] = splitedLine[1]
      parsedLine['index'] = splitedLine[2]

    parsedLines.append(parsedLine)
  return parsedLines


# translate parsed vm command into hack asm
def translate(parsed, settings):
  translatedLines = []
  if settings['stckInit']:
    translatedLines.append(commandPtns['stckInit'])
  branchCount = 0

  for line in parsed:
    translated = ''
    if line['cmdType'] == 'stackop':
      translated = commandPtns[line['cmdType']][line['cmd']][line['segment']]
      translated = intermediateTranslate(translated)
      translated = translated.replace('__INDEX__', line['index'])
    elif line['cmdType'].startswith('oper'):
      translated = commandPtns[line['cmdType']][line['cmd']]
      translated = intermediateTranslate(translated)
      translated = translated.replace('__BRANCHCNT__', str(branchCount))
      branchCount += 1
    translatedLines.append(translated)

  return translatedLines

def intermediateTranslate(cmdPtn):
  for key in commandPtns['ptns']:
    replaced = cmdPtn.replace(key, commandPtns['ptns'][key])
  return replaced

def writeToFile(outputFile, translated):
  for line in translated:
    outputFile.write(line + '\r\n')

# preprocess -- remove trailing whitespace characters, comments
def preprocess(lines):
  wsRemoved= map(lambda line : line.strip(), lines)
  cmtRemoved = map(lambda line : line[0:len(line) if line.find("//") < 0 else line.find("//")], wsRemoved)
  cmtRemoved= filter(lambda x : len(x.strip()) != 0, cmtRemoved)
  return cmtRemoved

if __name__ == "__main__":
  main()
