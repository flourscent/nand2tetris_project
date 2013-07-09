#!/usr/bin/python

import sys

def main():
  ARGS_REQUIRED = 2
  if len(sys.argv) < ARGS_REQUIRED:
    print "invalid argument"
    print "Usage : " + sys.argv[0] + " vmFile.vm"
    return 1
  files = openFiles(sys.argv)
  #parsed = parse(files['in'])
  #translated = translate(parsed)
  #writeToFile(files['out'], translated)
  
def openFiles(argv):
  # input / output
  inputFileName = argv[1];
  if len(sys.argv) < ARGS_WITH_OUTPUT:
    outputFileName = inputFileName[0:-3] + "asm"
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

def parse(inputFile):
## put the codes that parses VM language.
  return None

def translate(parsed):
## put the codes that translates parsed VM language into hack assembly language
  return None

def writeToFile(outputFile, translated):
  for line in translated:
    outputFile.write(line + '\r\n')

if __name__ == "__main__":
  main()
