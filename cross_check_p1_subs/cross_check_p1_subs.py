#!/usr/bin/python3

'''
Cross check the first and last shotpoints in a P111 with the substitutions.csv file.
Stores line information in a named tuple.
Default action is to process all lines in the substitutions.csv file.
Optional, supply a single sequence or a range of sequences, e.g.

To check all lines:
cross_check_p1_subs.py

To process a range of lines:
cross_check_p1_subs.py 3645-3650

To process a single line:
cross_check_p1_subs.py 3645

Last update 2023_09_01 Matthew Oppenheim
'''

import argparse
from collections import namedtuple
import logging
import os
from pathlib import Path
from range_strings import find_missing, get_ranges
import sys

logging.basicConfig(level=logging.debug, format='%(message)s')

# use a named tuple to store line information
Line_info = namedtuple('Line_info', 'sequence linename fsp lsp')

# default sequence value used if one is not supplied
SEQ = '3605'

# shotpoint number identifier in P111 file, line starts with this
P1_LINE_ID = r'P1,'
S1_LINE_ID = r'S1,'
VESSEL_ID = r',AMU,'

P111_DIR = r'/nfs/dropbox01/dropnav/7021/P111_NOAR'
SUBS_FILE = r'/nfs/D01/Reveal_Projects/7021_Eni_Hewett_Src/substitutions.csv'
# for testing
# P111_DIR = r'/home/amuobpproc05/Documents/matt/testing/p111_test'
# SUBS_FILE = r'/home/amuobpproc05/Documents/matt/testing/substitutions_adjusted.csv'


P111_SUFFIX = r'.p111'


def banner():
    ''' Startup message. '''
    logging.info('\nRunning: {}\n'.format(sys.argv[0]))
    logging.info('Cross check the first and last shotpoints in a P111 with the substitutions.csv file.')


def check_all_lines(line_info_list):
    ''' Iterate through Line_info tuples in line_info_list and check consistency with p111. '''
    for subs_line_info_tuple in line_info_list:
        line_sequence = subs_line_info_tuple.sequence
        p1_path = p111_filepath(line_sequence)
        if not(p1_path):
            logging.info('\n***no p1 found for sequence: {}\n'.format(line_sequence))
            continue
        # get a shot list for a p1 location
        p1_shots, p1_linename = p1_info(p1_path)
        # get shot list for the s1 location - sometimes this is short
        s1_shots = s1_info(p1_path)
        fsp, lsp = fsp_lsp(p1_shots)
        p1_tuple = Line_info(line_sequence, p1_linename, fsp, lsp)
        sequence = subs_line_info_tuple.sequence
        logging.debug('seq: {} fsp: {} lsp: {} seq: {}'.format(sequence, fsp, lsp, p1_linename))
        compare_tuples(subs_line_info_tuple, p1_tuple)
        # compare the p1 and s1 shot list incase one of these is incomplete -
        # it happens
        compare_p1_s1_shots(p1_shots, s1_shots)
        check_missing('p1 AMU', p1_shots)
        check_missing('s1', s1_shots)


def check_missing(name, shot_list):
    ''' Check for missing shots in shot_list. '''
    shot_list_int = map(int, shot_list)
    missing = find_missing(list(shot_list_int))
    if missing:
        logging.info('***missing shots in p111 {} data: {}'.format(name, missing))
    else:
        logging.debug('no missing shots in the shot_list for {}'.format(name))


def compare_p1_s1_shots(p1_shots, s1_shots):
    ''' Compare two lists of shots. '''
    if not p1_shots == s1_shots:
        logging.debug('p1, s1 shots differ\np1: {}\ns1: {}\n'.format(p1_shots, s1_shots))
        logging.info('p1 fsp: {} lsp: {}'.format(p1_shots[0], p1_shots[-1]))
        logging.info('s1 fsp: {} lsp: {}\n'.format(s1_shots[0], s1_shots[-1]))
        diff_lists(p1_shots, s1_shots)
    else:
        logging.info('p1 and s1 shots agree\n')


def compare_tuples(line_info_tuple, p1_tuple):
    ''' Compare the line info tuples. '''

    if line_info_tuple == p1_tuple:
        logging.info('subs and p1 positions agree for seq: {} {}'.format(line_info_tuple.sequence, line_info_tuple))
    else:
        logging.info('\n*** error, disagreement for:\nsubs file: {}\np111 info: {}\n'.format(line_info_tuple, p1_tuple))


def create_line_info_tuples(subs_filepath, first_seq=None, last_seq=None):
    ''' Create a list of named tupes from the substition file. '''
    line_info_list = []
    logging.info('sequence range: {}'.format(range(first_seq, last_seq+1)))
    with open(subs_filepath, 'r') as subs:
        for line in subs:
            line = line.split(',')
            sequence = line[0]
            # lots of lines just containing ',' in the subs file
            if not sequence.isnumeric():
                continue
            # restrict to supplied sequence range, if specified at run time
            if (first_seq != None):
                if (int(sequence) not in range(first_seq, last_seq+1)):
                    continue
            # make linename match the one in the p111
            linename = line[1][7:]
            fsp = line[4]
            lsp = line[5]
            line_info = Line_info(sequence, linename, fsp, lsp)
            line_info_list.append(line_info)
    return line_info_list


def diff_lists(shot_list_one, shot_list_two):
    ''' Find the difference between two shot lists. '''
    diff = set(shot_list_one)^set(shot_list_two)
    logging.info('difference between lists for SP: {}'.format(diff))


def exit_code(message):
    ''' Exits. '''
    logging.info(message)
    logging.info('exiting')
    raise SystemExit


def first_last_seq(*args):
    ''' Parses args and returns first and last sequence to process. '''
    try:
        args = ''.join(*args)
    # if no args TypeError is raised
    except TypeError:
        pass
    if not args:
        logging.info('sequence(s) not supplied, will process everything')
        # split input range on '-' symbol
        return None, None
    else:
        seqs = args.split('-')
    # first and last sequence supplied
    if (seqs.__len__() == 2 ):
        first_seq = int(seqs[0])
        last_seq = int(seqs[1])
    # only a single sequence supplied
    if (seqs.__len__() == 1 ):
        first_seq = int( seqs[0])
        last_seq = first_seq
    if (first_seq > last_seq):
            exit_code("The last seq_string needs to be greater or equal than the first seq_string ")
    return first_seq, last_seq


def fsp_lsp(shot_list):
    ''' Get first and last shotpoints. '''
    fsp = shot_list[0]
    lsp = shot_list[-1]
    return fsp, lsp


def p1_info(p1_path):
    ''' Get the shotpoints and sequence string from the p1 record in the p111. '''
    with open(p1_path, 'r') as p1_file:
        p1_shots = []
        for line in p1_file:
            if line.startswith(P1_LINE_ID) and VESSEL_ID in line:
                split_line = line.split(',')
                p1_shots.append(split_line[4])
                p1_linename = split_line[2]
    logging.debug(p1_shots)
    return p1_shots, p1_linename


def p111_filepath(sequence):
    ''' Find the filepath for the P111 for <sequence>. '''
    for filename in os.listdir(P111_DIR):
        if filename.split('.')[0] == sequence:
            logging.debug('found p111: {} for seq: {}'.format(filename, sequence))
            return os.path.join(P111_DIR, filename)


def s1_info(p1_path):
    ''' Get the shotpoints from the s1 record in the p111. '''
    with open(p1_path, 'r') as p1_file:
        s1_shots = []
        for line in p1_file:
            if line.startswith(S1_LINE_ID):
                split_line = line.split(',')
                s1_shots.append(split_line[4])
    logging.debug('s1 shots: {}'.format(s1_shots))
    return s1_shots



def verify_path(path):
    ''' Check path exists. '''
    if not os.path.exists(path):
        logging.info('*** cannot find path: {}'.format(path))
    else:
        logging.info('found path: {}'.format(path))


def main():
    banner()
    verify_path(SUBS_FILE)
    first_seq, last_seq = first_last_seq(sys.argv[1:])
    logging.info('Looking for seq {} to {}'.format(first_seq, last_seq))
    line_info_tuples = create_line_info_tuples(SUBS_FILE, first_seq, last_seq)
    logging.debug('line_info_tuples: {}'.format(line_info_tuples))
    check_all_lines(line_info_tuples)
    exit_code('completed normally')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # optional argument containing a single sequence or a range of sequences
    parser.add_argument('sequence', type=str, nargs='?',
            help='sequence or range of sequences to cross check substitution.csv against the p111')
    # comment out the following line for testing
    args = parser.parse_args()
    # uncomment the line below for testing
    # args = argparse.Namespace(sequence=SEQ)
    main()
