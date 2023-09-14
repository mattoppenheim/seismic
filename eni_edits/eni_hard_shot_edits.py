#!/usr/bin/python3

'''
Create ENI for
Input: Reveal format edit file
Output: ENI format file

Uses EniEdits class

Last update 2023_09_13 Matthew Oppenheim
'''

import argparse
from eni_edits import EniEdits
import logging
import sys
from tools import exit_code, first_last_seq, verify_path

# logging.basicConfig(level=logging.debug, format='%(message)s')
logging.getLogger().setLevel('DEBUG')

REVEAL_EDITS_SUFFIX = '_Hard_shot_edits.csv'
ENI_EDITS_SUFFIX = '_BADTR_NFH_FFS_EDIT'
ENI_OUTPUT_DIR = r'/nfs/D01/Reveal_Projects/7021_Eni_Hewett_Stmr/tables/edits/eni_nfh_ffs_edits'

# reminder for preparing script - ignore
# nnoremap <leader>r :update<cr>:! %:p 003

# for testing
SEQ = '3'

def process_all_edits(first_seq, last_seq):
    ''' Process all the sequences. '''
    for seq in range(first_seq, last_seq+1):
        process_single_seq(str(seq).zfill(3))


def process_single_seq(seq):
    ''' Process a single sequence. '''
    depth_edits = EniEdits(seq, REVEAL_EDITS_SUFFIX, ENI_EDITS_SUFFIX, ENI_OUTPUT_DIR)
    logging.debug('completed seq: {}'.format(seq))


def main():
    first_seq, last_seq = first_last_seq(sys.argv[1:])
    logging.info('Looking for seq {} to {}'.format(first_seq, last_seq))
    verify_path(ENI_OUTPUT_DIR)
    process_all_edits(first_seq, last_seq)
    exit_code('completed normally')


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
