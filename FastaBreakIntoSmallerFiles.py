#!/usr/bin/env python

import sys
import getopt
import os
from Bio import SeqIO

OPT_INPUT_FILE = False
OPT_NUMBER_FLAG = False
OPT_PADDING_FLAG = False

def Usage():
    print "\nFastaBreakIntoSmallerFiles.py is a program that read a FASTA file and break it into smaller fasta files with N number of sequences per file.\n"
    print "Usage:"
    print "\tFastaBreakIntoSmallerFiles.py -i [FASTA file]\n"
    print "\nMandatory options:"
    print "\t-i, --input=FILE"
    print "\t\tThe input FASTA file that is going to be split in smaller file."
    print "\t-n, --number"
    print "\t\tThe number of sequences that will be in each smaller fasta file."
    print "\nOther options:"
    print "\t-p, --padding=NUMBER"
    print "\t\tAllow the padding of the number used as a suffix in the output files. NUMBER correspond to the total number of digit that should be in the suffix in the output file."
    print "\t-h, --help"
    print "\t\tShow the options of the program."
    print "\n"
    sys.exit(1)

# Function that read and parse the command line arguments.
def SetOptions(argv):
    if len(argv) == 0:
        Usage()
    options, remaining = getopt.getopt(argv, 'i:n:p:h', ['input=','number=','padding=','help'])
    opt_flag = {'i': False,'n': False,'p': False}
    global OPT_INPUT_FILE, OPT_NUMBER_FLAG, OPT_PADDING_FLAG
    for opt, argu in options:
        if opt in ('-i', '--input'):
            if not opt_flag['i']:
                if os.path.exists(argu):
                    OPT_INPUT_FILE = argu
                    opt_flag['i'] = True
                else:
                    print >> sys.stderr , "\n[ERROR]: File or path of the input file does not exist. ", argu, "\n"
                    sys.exit(1)
            else:
                print >> sys.stderr , "\n[ERROR]: Trying to redefine the input file. Option -i / --input was already set.\n"
                sys.exit(1)
        elif opt in ('-n', '--number'):
            if not opt_flag['n']:
                try:
                    OPT_NUMBER_FLAG=int(argu)
                except:
                    print >> sys.stderr , "\n[ERROR]: The number of sequences per file must be and integer greater than 0. Option -n / --number must be an integer > 0.\n"	
                    sys.exit(1)
                
                if OPT_NUMBER_FLAG < 1:
                    print >> sys.stderr , "\n[ERROR]: The number of sequences per file is set to less than 1. Option -n / --number must be an integer > 0.\n"
                    sys.exit(1)
                opt_flag['n'] = True
            else:
                print >> sys.stderr , "\n[ERROR]: Trying to redefine the numbers of sequences per file flag. Option -n / --number was already set.\n"
                sys.exit(1)
        elif opt in ('-p', '--padding'):
            if not opt_flag['p']:
                try:
                    OPT_PADDING_FLAG=int(argu)
                except:
                    print >> sys.stderr , "\n[ERROR]: The padding flag should be a non negative integer. The value entered was not able to be converted to an integer. Option -p / --padding must be an integer > -1.\n"	
                    sys.exit(1)
                if OPT_PADDING_FLAG < 0:
                    print >> sys.stderr , "\n[ERROR]: The padding flag should be a non negative integer. Option -p / --padding must be an integer > -1.\n"
                    sys.exit(1)
                opt_flag['p'] = True
            else:
                print >> sys.stderr , "\n[ERROR]: Trying to redefine the padding. Option -p / --padding was already set.\n"
                sys.exit(1)
        elif opt in ('-h', '--help'):
            Usage()
    
    # Cheking if mandatory parameter are set.
    if not opt_flag['i']:
        print >> sys.stderr , "\n[ERROR]: Input file not defined. Option -i / --input.\n"
        sys.exit(1)
    if not opt_flag['n']:
        print >> sys.stderr , "\n[ERROR]: The number of sequences per file is not defined. Option -n / --number.\n"
        sys.exit(1)
    
    # If the padding flag was not set, the default value will be use.
    if not opt_flag['p']:
        OPT_PADDING_FLAG = 0
    
# Funtion that extract the file name and its extension.
def getFileNameAndExtension(input_file):
    file_name = os.path.basename(input_file)
    extension = os.path.splitext(input_file)[1]
    return file_name, extension

# Fuction that add 0 to the sufix number used in the output file.
def PaddingNumber(file_number,padding):
    #assert padding > -1
    # file number should be an string.
    return file_number.zfill(padding)

# Parse command line
SetOptions(sys.argv[1:])

current_number_of_sequences_in_file = 0
file_number = 0
file_name_output , file_extension_output = getFileNameAndExtension(OPT_INPUT_FILE)
#new_fasta_file = open(file_name_output +"."+ str(file_number) + file_extension_output , "w")
new_fasta_file = open(file_name_output +"."+ PaddingNumber(str(file_number),OPT_PADDING_FLAG) + file_extension_output , "w")

# Reading the FASTA file.
for record in SeqIO.parse(open(OPT_INPUT_FILE, "rU"), "fasta"):
    if current_number_of_sequences_in_file >= OPT_NUMBER_FLAG: # the expected number of sequences per file has been reached
        new_fasta_file.close()
        new_fasta_file = open(file_name_output +"."+ PaddingNumber(str(file_number),OPT_PADDING_FLAG) + file_extension_output , "w")
        current_number_of_sequences_in_file = 0
        file_number = file_number + 1
    new_fasta_file.write(">"+str(record.id)+"\n"+str(record.seq)+"\n")
    current_number_of_sequences_in_file = current_number_of_sequences_in_file + 1
