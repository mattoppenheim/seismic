#!/usr/bin/python3
'''
Tests for check_bad_shot_ranges.py
Run using pytest

Last update: 2023_09_04 Matthew Oppenheim
'''

from check_bad_shot_ranges import *
from collections import namedtuple
import logging
import pytest

logging.basicConfig(level=logging.INFO, format='%(message)s')

Line_info = namedtuple('Line_info', 'sequence linename fsp lsp')


SPEC_TUPLE_1 = (6, 6)
SPEC_TUPLE_1 = (3, 4)
SPEC_TUPLE_2 = (8, 15)
SPEC_TUPLE_3 =(12, 100)
SHOTS_1 = [1,2,3,4,5,6,7,9,20]

SUBS_TUPLE_1 = [Line_info(sequence='3667', linename='1185', fsp='1696', lsp='1401')]
SUBS_TUPLE_1 = Line_info('3667', '1185', '1696', '1401')
SUBS_TUPLE_2 = Line_info('3667', '1185', '1696', '1696')

EDIT_LIST_1 = ['1-2', 10, 12, '4-5']
EXPANDED_EDIT_LIST_1 = [1, 2, 10, 12, 4, 5]

EDIT_LIST_2 = []
EXPANDED_EDIT_LIST_2 = []


@pytest.mark.parametrize('subs_tuple, expected',[(SUBS_TUPLE_1, 296), (SUBS_TUPLE_2, 1)])
def test_total_line_shots(subs_tuple, expected):
    assert total_line_shots(subs_tuple) == expected


@pytest.mark.parametrize('edits_list, expected', [(EDIT_LIST_1, EXPANDED_EDIT_LIST_1),
    (EDIT_LIST_2, EXPANDED_EDIT_LIST_2)])
def test_expand_ranges(edits_list, expected):
    assert expand_ranges(edits_list) == expected


def test_percentage_bad():
    assert percentage_bad(0, 1) == 0
    assert percentage_bad(1, 1) == 100
    assert not percentage_bad(1, 10) == 0


def test_parse_edits_line():
    assert parse_edits_line('false;1482;ALL;ALL;ALL;Error;ALL;Gun no status;') == '1482'


@pytest.mark.parametrize('spec_for_bad, range_to_check, bad_shots, expected', [(SPEC_TUPLE_1[0], SPEC_TUPLE_1[1],SHOTS_1, False),
    (SPEC_TUPLE_2[0], SPEC_TUPLE_2[1],SHOTS_1, False),
    (SPEC_TUPLE_3[0], SPEC_TUPLE_3[1],SHOTS_1, True)])
def test_single_spec_check(spec_for_bad, range_to_check, bad_shots, expected):
    logging.debug('spec_for_bad: {} range_to_check: {} bad_shots: {}'.format(spec_for_bad, range_to_check, bad_shots))
    assert single_spec_check(spec_for_bad, range_to_check, bad_shots) == expected


