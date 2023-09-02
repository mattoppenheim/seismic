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

e.g. (9, 80) means 9 shots bad in an 80 shot range is illegal

Last edit: 2023_09_02 Matthew Oppenheim
'''

import logging


logging.basicConfig(level=logging.DEBUG, format='%(message)s')


# BAD_SHOT_LIST = [100, 102, 103, 110]
BAD_SHOT_LIST=[2676, 2698, 2706, 2714, 2774, 2788, 2830, 2854, 2856, 2876, 2910, 2942]
# SPEC_TUPLES = [(2, 2), (3, 200)]

# 7021 ENI 3D specs from Ref_03_AESI-M-BTP-01
SPEC_TUPLES = [(6, 6), (8, 15), (12, 100)]

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


def expand_ranges(edits_list):
    ''' Expand shot ranges to a list of individual shots. '''
    shot_list = []
    for edit in edits_list:
        logging.debug('edit: {}'.format(edit))
        edit = str(edit)
        shot_range = [int(x) for x in list(edit.split('-'))]
        shot_list += ([a for a in range(min(shot_range), max(shot_range)+1)])
    return shot_list


def intersect(a,b):
    ''' return the intersection of two lists'''
    return list(set(a) & set(b))


def main(bad_shots, spec_tuples):
    bad_shots = expand_ranges(bad_shots)
    logging.info('expanded list: {}'.format(bad_shots))
    bad_shots.sort()
    print('total edits: {}'.format(len(bad_shots)))
    print('checking for bad edits in sorted list:\n{}'.format(bad_shots))
    for illegal_bad, check_range in spec_tuples:
        test_passed = check_good(illegal_bad, check_range, bad_shots)
        if test_passed:
            print('passed test')
        else:
            print('*** failed test')


if __name__ == '__main__':
    main(BAD_SHOT_LIST, SPEC_TUPLES)
