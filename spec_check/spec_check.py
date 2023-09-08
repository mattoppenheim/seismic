#!/usr/bin/python3
'''
Use

check_bad_shot_ranges <sequence(s)>

e.g.

check_bad_shot_ranges 3667

or

check_bad_shot_ranges 3667-3669

If no sequence(s) are supplied, the script iterates through
everything that is in the substitutions.csv file.

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

Last update: 2023_09_07 Matthew Oppenheim
'''

import argparse
from collections import namedtuple
import logging
import os
# Subs creates line information tuples from the substitutions.csv file
from substitutions import Subs
import sys
import tools


logging.basicConfig(level=logging.INFO, format='%(message)s')


# Location of edits directory
EDITS_DIRECTORY = r'/nfs/D01/Reveal_Projects/7021_Eni_Hewett_Src/tables/edits/edits_linda'
EDITS_FILENAME_SUFFIX = 'Hard_edits.csv'

# spec for how many shots can be bad for an entire line
# 7021 ENI 3D spec from Ref_03_AESI-M-BTP-01
PERCENTAGE_PER_LINE = 5

# spec for how many shots can be bad for the entire survey
PERCENTAGE_SURVEY = 2


# 7021 ENI 3D specs from Ref_03_AESI-M-BTP-01
SPEC_TUPLES = [(6, 6), (8, 15), (12, 100)]

SUBS_FILEPATH = r'/nfs/D01/Reveal_Projects/7021_Eni_Hewett_Src/substitutions.csv'

# Tuple used to store line information from substitutions.csv file
Line_info = namedtuple('Line_info', 'sequence linename fsp lsp')


def check_line_spec(percentage_bad):
    ''' Check percentage_bad against the spec for bad shots per line. '''
    if percentage_bad < PERCENTAGE_PER_LINE:
        logging.info('The percentage of bad shots allowed per line ({}%) passed: {:.2f}'.format(PERCENTAGE_PER_LINE,
            percentage_bad))
    else:
        logging.info('\n*** The percentage of bad shots allowed per line ({}%) failed: {:.2f}'.format(PERCENTAGE_PER_LINE,
        percentage_bad))


def check_survey_spec(percentage_bad):
    ''' Check percentage_bad against the spec for bad shots for the whole survey. '''
    if percentage_bad < PERCENTAGE_SURVEY:
        logging.info('\nThe percentage of bad shots allowed per line ({}%) passed: {:.2f}'.format(PERCENTAGE_SURVEY,
            percentage_bad))
    else:
        logging.info('\n*** The percentage of bad shots allowed if this is the entire survey ({}%) failed: {:.2f}'.format(PERCENTAGE_SURVEY,
        percentage_bad))


def expand_ranges(edits_list):
    ''' Expand shot ranges to a list of individual shots. '''
    shot_list = []
    for edit in edits_list:
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


def intersect(a, b):
    ''' Return the intersection of two lists. '''
    return list(set(a) & set(b))


def percentage_bad(bad_shots, total_shots):
    ''' Calculate the percentage of bad shots. '''
    if total_shots == 0:
        tools.exit_code('line with 0 shots and {} bad shots, not possible'.format(bad_shots))
    percentage_bad = float('{:.2f}'.format(100*bad_shots/total_shots))
    logging.debug('percentage bad: {:.2f}'.format(percentage_bad))
    return percentage_bad


def parse_edits_line(edit_line):
    ''' Find the edit in the edits_line '''
    # edit_line e.g.: false;1482;ALL;ALL;ALL;Error;ALL;Gun no status;
    edit = edit_line.split(';')[1]
    return edit


def read_edits_file(sequence):
    ''' Get bad shots from the edits file for <sequence>. '''
    edits_filepath = find_edits_filepath(sequence)
    if edits_filepath is None:
        return None
    bad_shot_list = []
    with open(edits_filepath, 'r') as edits_file:
        edits_file.readline()
        for line in edits_file:
            new_edit = parse_edits_line(line)
            bad_shot_list.append(new_edit)
    return bad_shot_list


def single_spec_check(spec_for_bad, range_to_check, bad_shots):
    ''' Checks if <spec_for_bad> bad shots over <range_to_check> shots in <bad_shots> is in spec. '''
    tests_pass = True
    logging.debug('spec_for_bad: {} range_to_check: {} bad_shots: {}'.format(spec_for_bad, range_to_check, bad_shots))
    logging.info('checking for {} bad shots in {} shots'.format(spec_for_bad, range_to_check))
    bad_shots.sort()
    for bad_shot in bad_shots:
        test_range = range(bad_shot, bad_shot+range_to_check)
        # find where the bad shots are in the range of shots we are testing over
        bad_shots_in_test_range = intersect(test_range, bad_shots)
        num_bad_shots = len(bad_shots_in_test_range)
        if num_bad_shots < spec_for_bad:
            logging.debug('test passes at SP: {}'.format(bad_shot))
        else:
            logging.info('*** fail shot {}: bad_shots: {}'.format(bad_shot, num_bad_shots))
            tests_pass = False
    return tests_pass


def spec_check_all_sequences(subs_tuples, spec_tuples):
    ''' Iterate through the sequences in <subs_tuples> '''
    all_shots = 0
    all_bad_shots = 0
    for subs_tuple in subs_tuples:
        sequence = subs_tuple.sequence
        logging.info('\nChecking sequence: {}'.format(sequence))
        bad_shots = read_edits_file(sequence)
        if bad_shots is None:
            logging.info('No bad shots for sequence: {}'.format(sequence))
            continue
        logging.info('bad_shots: {}'.format(bad_shots))
        # check the bad shots against the bad shots specs for a single line
        spec_check_single_line(bad_shots, spec_tuples)
        # check if % bad for entire line are in spec
        line_shots = total_line_shots(subs_tuple)
        line_bad_shots = len(bad_shots)
        line_percentage_bad = percentage_bad(line_bad_shots, line_shots)
        check_line_spec(line_percentage_bad)
        all_shots += line_shots
        all_bad_shots += line_bad_shots
    percentage_all_bad = percentage_bad(all_bad_shots, all_shots)
    check_survey_spec(percentage_all_bad)
    # return values to enable testing
    return all_shots, all_bad_shots


def spec_check_single_line(bad_shots, spec_tuples_list):
    ''' Check if <bad_shots> list is out of spec for the list of specs in spec_tuples_list. '''
    bad_shots = expand_ranges(bad_shots)
    bad_shots.sort()
    logging.debug('total edits: {}'.format(len(bad_shots)))
    logging.debug('checking for bad edits in sorted list:\n{}'.format(bad_shots))
    for illegal_bad, check_range in spec_tuples_list:
        test_passed = single_spec_check(illegal_bad, check_range, bad_shots)
        if test_passed:
            logging.info('passed test')
        else:
            logging.info('*** failed test')


def total_line_shots(subs_tuple):
    ''' Calculates how many shots were fired for a line. '''
    fsp = int(subs_tuple.fsp)
    lsp = int(subs_tuple.lsp)
    return abs(fsp-lsp) + 1


def main(spec_tuples):
    # get list of (sequence, linename, fsp, lsp) from substitutions.csv
    # if first_seq, last_seq are None, this contains all sequences
    subs = Subs(sys.argv[1:], subs=SUBS_FILEPATH)
    subs_tuples = subs.get_line_info_tuples()
    logging.debug('subs tuples: {}'.format(subs_tuples))
    spec_check_all_sequences(subs_tuples, spec_tuples)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # optional argument containing a single sequence or a range of sequences
    parser.add_argument('sequence', type=str, nargs='?',
            help='sequence or range of sequences to cross check substitution.csv against the p111')
    # comment out the following line for testing
    args = parser.parse_args()
    # uncomment the line below for testing
    # args = argparse.Namespace(sequence=SEQ)
    main(SPEC_TUPLES)
