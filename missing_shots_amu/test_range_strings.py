''' Tests for range_strings.py
Matthew Oppenheim
last update: 2023_06_09
run using:
python -m pytest test_range_strings.py
'''

import pytest
from range_strings import *

range_tuples_data = [ ([18,1,121,94,0,120,121], [(0,1), (18, 18), (94, 94), (120, 121), (121,121)] ),
             ( [25, 7, 9], [(7, 7), (9, 9), (25, 25)] ),
             ( [1], [(1,1)] ),
             ( [], [] ) ]

find_missing_data = [( [0, 1, 3, 6], [2, 4, 5] ),
        ( [0, 0, 1, 1, 3], [2]), ([], []) ]

remove_multiples_data = [([], []), ([1, 2, 3], [1, 2, 3]),
        ( [1, 1, 2, 2, 3], [1, 2, 3]) ]

reverse_ranges_data =  [ ('50,25,23-20,9-6,3-1', '1-3,6-9,20-23,25,50'),
        ('', ''),
        ('1, 1', '1,1') ]


def test_consecutives():
    assert consecutives([(0,1), (17, 17), (94, 94), (120, 121)]) == \
        '0-1, 17, 94, 120-121'


def test_consecutives_2():
    assert consecutives([(0,1), (17, 17), (94, 94), (120, 121)]) != \
        '0-0, 17, 94, 120-121'


def test_duplicates():
    assert find_duplicates([1, 1, 2, 2, 3, 4, 5]) == [1, 2]


def test_duplicates_2():
    assert find_duplicates([]) == []


@pytest.mark.parametrize("test_list, expected", find_missing_data)
def test_find_missing(test_list, expected):
    assert find_missing(test_list) == expected


@pytest.mark.parametrize("test_list, expected", remove_multiples_data)
def test_remove_multiples(test_list, expected):
    assert remove_multiples(test_list) == expected


@pytest.mark.parametrize("test_list, expected", range_tuples_data)
def test_range_tuples(test_list, expected):
    assert range_tuples(test_list) == expected


@pytest.mark.parametrize("test_list, expected", reverse_ranges_data)
def test_reverse_ranges(test_list, expected):
    assert reverse_ranges(test_list) == expected
