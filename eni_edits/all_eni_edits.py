#!/usr/bin/python3

'''
Create ENI for
Input: Reveal format edit file
Output: ENI format file

Uses EniEdits class

Last update 2023_09_16 Matthew Oppenheim
'''

import argparse
from eni_edits import EniEdits
import logging
import sys
from tools import exit_code, first_last_seq, verify_path

# logging.basicConfig(level=logging.debug, format='%(message)s')
logging.getLogger().setLevel('INFO')

HARD_REVEAL_EDITS_SUFFIX = '_Hard_edits.csv'
HARD_ENI_EDITS_SUFFIX = '_BADTR_HARD_EDIT'
HARD_ENI_OUTPUT_DIR = r'/nfs/D01/Reveal_Projects/7021_Eni_Hewett_Stmr/tables/edits/edits_ENI_Format'

HARD_SHOT_REVEAL_EDITS_SUFFIX = '_Hard_shot_edits.csv'
HARD_SHOT_ENI_EDITS_SUFFIX = '_BADTR_NFH_FFS_EDIT'
HARD_SHOT_ENI_OUTPUT_DIR = r'/nfs/D01/Reveal_Projects/7021_Eni_Hewett_Stmr/tables/edits/edits_ENI_Format'

RECEIVER_REVEAL_EDITS_SUFFIX = '_Rec_Depth_edits.csv'
RECEIVER_ENI_EDITS_SUFFIX = '_BADTR_RECEIVER_DEPTH_EDIT'
RECEIVER_ENI_OUTPUT_DIR = r'/nfs/D01/Reveal_Projects/7021_Eni_Hewett_Stmr/tables/edits/edits_ENI_Format'

SOURCE_REVEAL_EDITS_SUFFIX = '-Source-Depth-Edits-9999.csv'
SOURCE_ENI_EDITS_SUFFIX = '_BADTR_SOURCE_DEPTH_EDIT'
SOURCE_ENI_OUTPUT_DIR = r'/nfs/D01/Reveal_Projects/7021_Eni_Hewett_Stmr/tables/edits/edits_ENI_Format'

SOFT_REVEAL_EDITS_SUFFIX = '_Soft_edits.csv'
SOFT_ENI_EDITS_SUFFIX = '_BADTR_SOFT_EDIT'
SOFT_ENI_OUTPUT_DIR = r'/nfs/D01/Reveal_Projects/7021_Eni_Hewett_Stmr/tables/edits/edits_ENI_Format'


# reminder for preparing script - ignore
# nnoremap <leader>r :update<cr>:! %:p 003

# for testing
SEQ = '3'

def main():
    ''' Process all edits. '''
    hard_edits = EniEdits(HARD_REVEAL_EDITS_SUFFIX, HARD_ENI_EDITS_SUFFIX, HARD_ENI_OUTPUT_DIR)
    hard_edits.process_all_sequences(sys.argv[1:])

    hard_shot_edits = EniEdits(HARD_SHOT_REVEAL_EDITS_SUFFIX, HARD_SHOT_ENI_EDITS_SUFFIX, HARD_SHOT_ENI_OUTPUT_DIR)
    hard_shot_edits.process_all_sequences(sys.argv[1:])

    receiver_edits = EniEdits(RECEIVER_REVEAL_EDITS_SUFFIX, RECEIVER_ENI_EDITS_SUFFIX, RECEIVER_ENI_OUTPUT_DIR)
    receiver_edits.process_all_sequences(sys.argv[1:])

    source_edits = EniEdits(SOURCE_REVEAL_EDITS_SUFFIX, SOURCE_ENI_EDITS_SUFFIX, SOURCE_ENI_OUTPUT_DIR)
    source_edits.process_all_sequences(sys.argv[1:])

    soft_edits = EniEdits(SOFT_REVEAL_EDITS_SUFFIX, SOFT_ENI_EDITS_SUFFIX, SOFT_ENI_OUTPUT_DIR)
    soft_edits.process_all_sequences(sys.argv[1:])

    logging.info('completed normally')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # optional argument containing a single sequence or a range of sequences
    parser.add_argument('sequence', type=str, nargs='?',
            help='sequence or range of sequences to process')
    # comment out the following line for testing
    args = parser.parse_args()
    # uncomment the line below for testing
    # args = argparse.Namespace(sequence=SEQ)
    main()
