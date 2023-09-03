#!/usr/bin/python3

'''
Utility class to extract information from the substitutions.csv file.

Last update 2023_09_03 Matthew Oppenheim
'''

import argparse
from collections import namedtuple
import logging
import os
from pathlib import Path
import range_strings
import sys
import tools

logging.basicConfig(level=logging.DEBUG, format='%(message)s')

# use a named tuple to store line information
Line_info = namedtuple('Line_info', 'sequence linename fsp lsp')

# default sequence value used if one is not supplied
SEQ = '3605'


SUBS_FILEPATH = r'/nfs/D01/Reveal_Projects/7021_Eni_Hewett_Src/substitutions.csv'

# column numbers for information in the substitutions.csv file. Starts at 0:
SUBS_LINENAME_COLUMN = 1
SUBS_FSP_COLUMN = 3
SUBS_LSP_COLUMN = 4
SUBS_SEQ_COLUMN = 0
# position in line name where the sail line is stored
# e.g. in 2023HWT41183PAS3672, the sail line is 1183, which is slice(8,12)
LINE_SLICE = slice(8,12)

class Subs:

    def __init__(self, *args, **kwargs):
        logging.debug('Running {} \n'.format(sys.argv[0]))
        logging.debug('args: {} '.format(args))
        logging.debug('kwargs: {} '.format(kwargs))
        if 'seq' in kwargs:
            sequence = str(kwargs['seq'])
            logging.debug('sequence in kwargs: {}'.format(sequence))
            first_seq, last_seq = tools.first_last_seq(sequence)
        else:
            first_seq, last_seq = tools.first_last_seq(sys.argv[1:])
        subs_filepath = str(kwargs['subs'])
        tools.verify_path(subs_filepath)
        self.main(first_seq, last_seq, subs_filepath)


    def create_line_info_tuples(self, subs_filepath, first_seq=None, last_seq=None):
        ''' Create a list of named tupes from the substition file. '''
        line_info_list = []
        with open(subs_filepath, 'r') as subs:
            for line in subs:
                line = line.split(',')
                sequence = line[SUBS_SEQ_COLUMN]
                # lots of lines just containing ',' in the subs file
                if not sequence.isnumeric():
                    continue
                # restrict to supplied sequence range, if specified at run time
                if (first_seq != None):
                    if (int(sequence) not in range(first_seq, last_seq+1)):
                        continue
                # make linename match the one in the p111
                linename = line[SUBS_LINENAME_COLUMN][LINE_SLICE]
                # columns start numbering from 0
                fsp = line[SUBS_FSP_COLUMN]
                lsp = line[SUBS_LSP_COLUMN]
                line_info = Line_info(sequence, linename, fsp, lsp)
                line_info_list.append(line_info)
        return line_info_list


    def get_line_info_tuples(self):
        return self.line_info_list


    def main(self, first_seq, last_seq, subs_filepath):
        self.line_info_list = self.create_line_info_tuples(subs_filepath, first_seq, last_seq)


if __name__ == '__main__':
    # optional argument containing a single sequence or a range of sequences
    parser = argparse.ArgumentParser()
    parser.add_argument('seq', type=str, nargs='?',
            help='sequence or range of sequences to extract line information for from substitutions.csv')

    args = parser.parse_args()
    subs = Subs(args, subs=SUBS_FILEPATH)
    tuples = subs.get_line_info_tuples()
    logging.debug('tuples: {}'.format(tuples))
