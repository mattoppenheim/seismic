#!/usr/bin/python3
'''
Check that a line is still in spec when there are bad shots.
Supply the bad shots as a list called:
    BAD_SHOT_LIST
e.g.
[1 ,2 ,3, 500]
ranges can be supplied, e.g.

 [33, '50-60', '72-80']

Note that the ranges are supplied as strings, e.g.

'50-60'

The specs are supplied as tuples in the form:

 (max number edits, number of shots to check over)

e.g. (9, 80) means 9 shots bad in an 80 shot range is illegal.

Last edit: 2023_09_02 Matthew Oppenheim
'''

import argparse
from collections import namedtuple
import logging
import os
# Subs creates line information tuples from the substitutions.csv file
from substitutions import Subs
import sys
import tools


logging.basicConfig(level=logging.DEBUG, format='%(message)s')


# BAD_SHOT_LIST = [100, 102, 103, 110]
BAD_SHOT_LIST=[1405, 1417, 1427, 1449, 1505, 1523, 1537, 1591, 1601, 1629, 1653, 1677, 1685, 1695]
# SPEC_TUPLES = [(2, 2), (3, 200)]

# Location of edits directory
EDITS_DIRECTORY = r'/nfs/D01/Reveal_Projects/7021_Eni_Hewett_Src/tables/edits/edits_linda'
EDITS_FILENAME_SUFFIX = 'Hard_edits.csv'

# 7021 ENI 3D specs from Ref_03_AESI-M-BTP-01
SPEC_TUPLES = [(6, 6), (8, 15), (12, 100)]

SUBS_FILEPATH = r'/nfs/D01/Reveal_Projects/7021_Eni_Hewett_Src/substitutions.csv'

# Tuple used to store line information from substitutions.csv file
Line_info = namedtuple('Line_info', 'sequence linename fsp lsp')

def check_good(illegal_bad, check_range, bad_shots):
    ''' Checks if <illegal_bad> edits over <check_range> shots in <bad_shots> is in spec. '''
    # default to fail
    tests_pass = False
    logging.info('checking illegal_bad: {} check_range: {}'.format(illegal_bad, check_range))
    bad_shots.sort()
    for edit in bad_shots:
        test_range = range(edit, edit+check_range)
        # find where the bad shots are in the range of shots we are testing over
        edits_in_test_range = intersect(test_range, bad_shots)
        num_edits = len(edits_in_test_range)
        if num_edits < illegal_bad:
            tests_pass = True
        else:
            logging.info('*** fail shot {}: edits: {}'.format(edit, num_edits))
    return tests_pass


def check_specs_single_sequence(bad_shots, spec_tuples_list):
    ''' Check if <bad_shots> list is out of spec for the list of specs in spec_tuples_list. '''
    bad_shots = expand_ranges(bad_shots)
    bad_shots.sort()
    logging.debug('total edits: {}'.format(len(bad_shots)))
    logging.debug('checking for bad edits in sorted list:\n{}'.format(bad_shots))
    for illegal_bad, check_range in spec_tuples_list:
        test_passed = check_good(illegal_bad, check_range, bad_shots)
        if test_passed:
            logging.info('passed test')
        else:
            logging.info('*** failed test')


def check_all_sequences(subs_tuples, spec_tuples):
    ''' Iterate through the sequences in <subs_tuples> '''
    for subs_tuple in subs_tuples:
        bad_shots = get_edits(subs_tuple.sequence)


def expand_ranges(edits_list):
    ''' Expand shot ranges to a list of individual shots. '''
    shot_list = []
    for edit in edits_list:
        logging.debug('edit: {}'.format(edit))
        edit = str(edit)
        shot_range = [int(x) for x in list(edit.split('-'))]
        shot_list += ([a for a in range(min(shot_range), max(shot_range)+1)])
    return shot_list


def find_edits_filepath(sequence):
    ''' Find the filepath for the edits file for <sequence>. '''
    for filename in os.listdir(EDITS_DIRECTORY):
        if filename.startswith(sequence) and filename.endswith(EDITS_FILENAME_SUFFIX):
            logging.debug('found edits file: {}'.format(filename))
            return os.path.join(EDITS_DIRECTORY, filename)
    return None


def get_edits(sequence):
    ''' Get bad shots from the edits file for <sequence>. '''
    edits_filepath = find_edits_filepath(sequence)
    if edits_filepath is None:
        return None
    edits_list = []
    with open(edits_filepath, 'r') as edits_file:
        edits_file.readline()
        for line in edits_file:
            new_edit = parse_edits_line(line)
            edits_list.append(new_edit)
    logging.debug('edits_list: {}'.format(edits_list))


def intersect(a, b):
    ''' Return the intersection of two lists. '''
    return list(set(a) & set(b))


def parse_edits_line(edit_line):
    ''' Find the edit in the edits_line '''
    # edit_line e.g.: false;1482;ALL;ALL;ALL;Error;ALL;Gun no status;
    edit = edit_line.split(';')[1]
    return edit


def main(bad_shots, spec_tuples):
    # get list of (sequence, linename, fsp, lsp) from substitutions.csv
    # if first_seq, last_seq are None, this contains all sequences
    subs = Subs(sys.argv[1:], subs=SUBS_FILEPATH)
    subs_tuples = subs.get_line_info_tuples()
    logging.debug('subs tuples: {}'.format(subs_tuples))
    check_all_sequences(subs_tuples, spec_tuples)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # optional argument containing a single sequence or a range of sequences
    parser.add_argument('sequence', type=str, nargs='?',
            help='sequence or range of sequences to cross check substitution.csv against the p111')
    # comment out the following line for testing
    args = parser.parse_args()
    # uncomment the line below for testing
    # args = argparse.Namespace(sequence=SEQ)
    main(BAD_SHOT_LIST, SPEC_TUPLES)
