#!/usr/bin/python3

'''
Cross check the first and last shotpoints in a P111 with the substitutions.csv file.
Stores line information in a named tuple.
Not yet working.
Last update 2023_08_31 Matthew Oppenheim
'''

import argparse
from collections import namedtuple
import logging
import os
from pathlib import Path
import sys

logging.basicConfig(level=logging.INFO, format='%(message)s')

# use a named tuple to store line information
Line_info = namedtuple('Line_info', 'sequence linename fsp lsp')

# default sequence value used if one is not supplied
SEQ = '3605'

# shotpoint number identifier in P111 file, line starts with this
LINE_ID = r'P1,'
VESSEL_ID = r',AMU,'

P111_DIR = r'/nfs/dropbox01/dropnav/7021/P111_NOAR'
# P111_DIR = r'/home/amuobpproc05/Documents/matt/p111_test'
SUBS_FILE = r'/nfs/D01/Reveal_Projects/7021_Eni_Hewett_Src/substitutions.csv'


P111_SUFFIX = r'.p111'


def check_all_lines(line_info_list):
    ''' Iterate through Line_info tuples in line_info_list. '''
    for line_info_tuple in line_info_list:
        line_sequence = line_info_tuple.sequence
        p1_path = p1_filepath(line_sequence)
        if not(p1_path):
            logging.info('no p1 found for sequence: {}'.format(line_sequence))
            continue
        fsp, lsp, p1_linename = fsp_lsp_p111(p1_path)
        p1_tuple = Line_info(line_sequence, p1_linename, fsp, lsp)
        logging.debug('seq: {} fsp: {} lsp: {} seq: {}'.format(line_info_tuple.sequence, fsp, lsp, p1_linename))
        compare_tuples(line_info_tuple, p1_tuple)


def compare_tuples(line_info_tuple, p1_tuple):
    ''' Compare the line info tuples. '''

    if line_info_tuple == p1_tuple:
        logging.info('all parameters agree for seq: {} {}'.format(line_info_tuple.sequence, line_info_tuple))
    else:
        logging.info('\n*** error, disagreement for:\nsubs file: {}\np111 info: {}\n'.format(line_info_tuple, p1_tuple))


def create_line_info_tuples(subs_filepath):
    ''' Create a list of named tupes from the substition file. '''
    line_info_list = []
    with open(subs_filepath, 'r') as subs:
        for line in subs:
            line = line.split(',')
            sequence = line[0]
            # lots of lines just containing ',' in the subs file
            if not sequence.isnumeric():
                continue
            # make linename match the one in the p111
            linename = line[1][7:]
            fsp = line[4]
            lsp = line[5]
            line_info = Line_info(sequence, linename, fsp, lsp)
            line_info_list.append(line_info)
    return line_info_list


def exit_code(message):
    ''' Exits. '''
    logging.info(message)
    logging.info('exiting')
    raise SystemExit


def fsp_lsp_p111(p1_path):
    ''' Get the first, last shotpoints and p1 sequence string from the p111. '''
    with open(p1_path, 'r') as p1_file:
        shots = []
        for line in p1_file:
            if line.startswith(LINE_ID) and VESSEL_ID in line:
                split_line = line.split(',')
                shots.append(split_line[4])
                p1_linename = split_line[2]
    logging.debug(shots)
    return shots[0], shots[-1], p1_linename


def p1_filepath(sequence):
    ''' Find the filepath for the P111 for <sequence>. '''
    for filename in os.listdir(P111_DIR):
        if filename.split('.')[0] == sequence:
            logging.debug('found p111: {} for seq: {}'.format(filename, sequence))
            return os.path.join(P111_DIR, filename)


def verify_path(path):
    ''' Check path exists. '''
    if not os.path.exists(path):
        logging.info('*** cannot find path: {}'.format(path))
    else:
        logging.info('found path: {}'.format(path))


def main():
    verify_path(SUBS_FILE)
    line_info_tuples = create_line_info_tuples(SUBS_FILE)
    logging.debug('line_info_tuples: {}'.format(line_info_tuples))
    check_all_lines(line_info_tuples)
    exit_code('completed normally')


if __name__ == '__main__':
    main()
