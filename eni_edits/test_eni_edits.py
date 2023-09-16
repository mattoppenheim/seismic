#!/usr/bin/python3
'''
Tests for eni_edits.py
Run using pytest

Last update: 2023_09_12 Matthew Oppenheim
'''

from eni_edits import EniEdits
import logging
import pytest
from unittest.mock import patch
import os.path

logging.basicConfig(level=logging.INFO, format='%(message)s')

# reveal edit format:
# shot1, shot2, chan1, chan2, streamer1, streamer2
# 12071,12071,699,701,3,3

C2 = '$TRCDLRV'
C3 = ' *DELREVDEF'
C4 = '    DELREV = SHOTPOINT_NUM'
C6 = '   <OPERATION   LITERAL      GATHER    LITERAL_VALUE  DETECT_TYPE'

ENI_LINE_TEST_1 = ('1000:2000', '1:10','    TDELETE   CHANNEL         1000:2000     1:10')

REVEAL_EDIT_1 = '12071,12071,699,701,3,3'
ENI_EDIT_1 = '12071:12071,2297:2299'

# reveal_edit: 12152,12182,126,135,5,5
# eni_shot: 12152:12182 eni_chan_range: 3322:3331


#@patch('os.path.exists')
@pytest.mark.parametrize('channel, streamer, expected',[(1, 1, 1), (799, 1, 799), (1, 2, 800), (2, 6, 3997), (799, 6, 4794)])
def test_abs_chan_num(channel, streamer, expected):
    # edits = EniEdits( reveal_suffix, eni_suffix, eni_output_dir)
    #mock_exists.return_value = True
    edits = EniEdits('reveal_suffix', 'eni_suffix', 'eni_output_dir')
    assert edits.abs_chan_num(channel, streamer) == expected


@pytest.mark.parametrize('shots, channels, expected', [ENI_LINE_TEST_1])
def test_format_eni_line(shots, channels, expected):
    edits = EniEdits('reveal_suffix', 'eni_suffix', 'eni_output_dir')
    assert edits.format_eni_line(shots, channels) == expected


'''
def test_comment2():
    assert comment_2() == C2
    assert comment_2() != 'carrot'


def test_comment3():
    assert comment_3() == C3
    assert comment_3() != 'carrot'


def test_comment4():
    assert comment_4() == C4
    assert comment_4() != 'carrot'


def test_comment6():
    assert comment_6() == C6
    assert comment_6() != 'carrot'

'''
