#!/usr/bin/python3
'''
Cross check edits againt zero depth .csv files for a given sequence.
Last update: 2023-06-30 Matthew Oppenheim.

'''

import argparse
import logging
import os
from pathlib import Path
import sys

logging.basicConfig(level=logging.INFO, format='%(message)s')

# default sequence value used if one is not supplied
SEQ = '3605'

# zero depth .csv files directory
ZERO_DEPTHS = r'/nfs/D01/Reveal_Projects/7021_Eni_Hewett_Src/tables/PROD/P1_SEGD/Zero_Depth'

# edit .csv files directory
EDITS_DIR = r'/nfs/D01/Reveal_Projects/7021_Eni_Hewett_Src/tables/edits/edits_linda'

EDITS_SUFFIX = r'_Hard_edits.csv'
ZERO_SUFFIX = r'_Zero_depth.csv'

def check_path(path):
    ''' Check path exists. '''
    if not os.path.exists(path):
        logging.info('*** cannot find path: {}'.format(path))
    else:
        logging.info('found path: {}'.format(path))


def cross_check_edit_zeros(zeros, edits):
    ''' Compare edits and zeros files. '''
    extra_edits = set(edits)-set(zeros)
    return extra_edits


def cross_check_zeros_edits(zeros, edits):
    ''' Compare edits and zeros files. '''
    extra_zeros = set(zeros)-set(edits)
    return extra_zeros


def edits_filepath(edits_dir, edits_filename):
    ''' Find the edits filepath for <sequence>. '''
    edits_path = os.path.join(edits_dir, edits_filename)
    if not os.path.exists(edits_path):
        logging.info('cannot find edits file: {}'.format(edits_path))
        return None
    logging.debug('\nfound edits file: {}'.format(edits_path))
    return edits_path


def exit_code(message):
    ''' Exits. '''
    logging.info(message)
    logging.info('exiting')
    raise SystemExit


def first_last_seq(*args):
    ''' Returns first and last sequence to process. '''
    try:
        args = ''.join(*args)
    # if no args TypeError is raised
    except TypeError:
        pass
    if not args:
        seqs = str(input ("Which sequences(s) to process ? ")).split("-") # split input range on '-' symbol
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


def output_results(zero_list, edit_list, sequence):
    ''' Display results for comparing zero and edits files. '''
    cross_check_zeros = cross_check_edit_zeros(zero_list, edit_list)
    if len(cross_check_zeros) == 0:
        logging.info('\nNo missing zero depths in edits for {}, zeros: {}\n'.format(sequence, zero_list))
    else:
        logging.info('\n*** extra edits: {}, edits: {}\n'.format(cross_check_zeros, edit_list))
    cross_check_edits = cross_check_zeros_edits(zero_list, edit_list)
    if len(cross_check_edits) == 0:
        logging.info('\nNo missing edits compared to zeros for {}, edits: {}\n'.format(sequence, edit_list))
    else:
        logging.info('\n*** extra zeros: {}, zeros: {}\n'.format(cross_check_edits, zeros_list))


def parse_edit(edit_line):
    ''' Extract shot number from edits file line. '''
    return int(edit_line.split(';')[1])


def parse_zeros(zero_line):
    ''' Extract shot number from edits file line. '''
    return int(zero_line.split(',')[0])


def read_edits(edits_filepath):
    ''' Return list of edits for <edits_filepath>. '''
    with open(edits_filepath, 'r') as open_edits:
        edit_list = []
        open_edits.readline()
        for line in open_edits:
            edit_list.append(parse_edit(line))
    return edit_list


def read_zeros(zeros_filepath):
    ''' Return list of zeroe shots for <zeros_filepath>. '''
    with open(zeros_filepath, 'r') as open_zeros:
        zeros_list = []
        open_zeros.readline()
        for line in open_zeros:
            zeros_list.append(parse_zeros(line))
    return zeros_list


def zeros_filepath(zeros_dir, zero_filename):
    ''' Find the edits filepath for <sequence>. '''
    zeros_path = os.path.join(zeros_dir, zero_filename)
    if not os.path.exists(zeros_path):
        logging.info('cannot find zeros file: {}'.format(zeros_path))
        return None
    logging.debug('\nfound zeros file: {}'.format(zeros_path))
    return zeros_path


def process_sequences(first_seq, last_seq, zeros_dir, edits_dir):
    ''' Process a range of sequences. '''
    for sequence in range(first_seq, last_seq+1):
        edits_filename = '{}{}'.format(sequence, EDITS_SUFFIX)
        zero_filename = '{}{}'.format(sequence, ZERO_SUFFIX)
        logging.info('\nsequence: {}'.format(sequence))
        # get a list of edits for <sequence>
        edits_path = edits_filepath(edits_dir, edits_filename)
        if edits_path is None:
            edit_list = []
        else:
            edit_list = read_edits(edits_path)
        logging.debug('\nedits for {}: {}\n'.format(sequence, edit_list))

        # get a list of zero depth shots for <sequence>
        zeros_path = zeros_filepath(zeros_dir, zero_filename)
        if zeros_path is None:
            zero_list = []
        else:
            zero_list = read_zeros(zeros_path)
        logging.debug('\nzeros for {}: {}\n'.format(sequence, zero_list))
        output_results(zero_list, edit_list, sequence)


def main(zeros_dir, edits_dir):
    logging.info('zero depths directory: {}\n\nedits directory: {}\n'.format(zeros_dir, edits_dir))
    check_path(zeros_dir)
    check_path(edits_dir)
    first, last = first_last_seq(sys.argv[1:])
    process_sequences(first, last, zeros_dir, edits_dir)
    exit_code('completed normally')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('sequence', type=str, default=SEQ, help='sequence to cross check edits against zero depths')
    # comment out the following line for testing
    args = parser.parse_args()
    # uncomment the line below for testing
    # args = argparse.Namespace(sequence=SEQ)
    main(ZERO_DEPTHS, EDITS_DIR)
