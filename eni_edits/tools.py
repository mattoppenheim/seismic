#!/usr/bin/python3

'''
Tools that are used across different scripts.
I put these in a separate library so that I can update them in one location,
rather than edit multiple scripts.

Last update 2023_09_03 Matthew Oppenheim
'''

import logging
import os
from pathlib import Path
import sys

logging.basicConfig(level=logging.DEBUG, format='%(message)s')


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
        logging.info('sequence(s) not supplied')
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


def verify_path(path):
    ''' Check path exists. '''
    if not os.path.exists(path):
        logging.info('*** cannot find path: {}'.format(path))
    else:
        logging.info('found path: {}'.format(path))


