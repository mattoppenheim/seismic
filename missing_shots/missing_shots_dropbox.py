#!/usr/bin/python3
''' List missing shots in dropbox1 and dropbox2 for a sequence.
Expects a sequence number to be supplied.
To run on e.g. sequence 38 type:
./missing_shots.py 38
Last update: 2023-06-04 Matthew Oppenheim.

'''

import argparse
import os
from pathlib import Path
import logging
from range_strings import *
import sys

logging.basicConfig(level=logging.DEBUG, format='%(message)s')

# default sequence value used if one is not supplied
SEQ = '40'

# base directory for folders containing shots
DROPBOX1_DIR = r'/nfs/awa-data01/dropbox1/dropobp/'

# Directory used for re-export
DROPBOX2_DIR = r'/nfs/awa-data02/dropbox2/dropobp/'


parser = argparse.ArgumentParser()
parser.add_argument('sequence', type=str, default=SEQ, help='sequence to find missing shots')


def display_duplicates(shots):
    ''' Display information about duplicated shots. '''
    duplicates = find_duplicates(shots)
    if len(duplicates) == 0:
        logging.info('no duplicates found')
    else:
        logging.info('duplicates: {}'.format(find_duplicates(shots)))


def display_missing(missing):
    ''' Display missing shot information. '''
    if len(missing) == 0:
        logging.info('no missing shots')
        return
    logging.info('missing shots: {}'.format(get_ranges(missing)))
    logging.info('first missing shot: {}'.format(missing[0]))
    logging.info('last missing shot: {}'.format(missing[-1]))
    logging.info('number missing shots: {}'.format(len(missing)))


def dropbox_dir_path(sequence, dropbox_dir):
    dropbox_dir_path = os.path.join(dropbox_dir, sequence)
    if not os.path.exists(dropbox_dir_path):
        exit_code('cannot find directory: {}'.format(dropbox_dir_path))
    return os.path.join(dropbox_dir, sequence)


def exit_code(message):
    ''' Exits. '''
    logging.info(message)
    logging.info('exiting')
    raise SystemExit


def shot_list(filename_list):
    ''' Extract shots from the filenames. '''
    shot_list = []
    for filename in filename_list:
        shot_list.append(int(filename[:5]))
    # shot_list.sort()
    return shot_list


def get_filenames(input_dir):
    ''' Create a list of filenames in input_dir sorted in time order. '''
    basepath = Path(input_dir)
    try:
        os.chdir(basepath)
    except FileNotFoundError as e:
        exit_code('The directory path is not found: {}'.format(basepath))
    filenames = list(filter(os.path.isfile, os.listdir(basepath)))
    filenames.sort(key=lambda x: os.path.getmtime(x))
    return filenames


def parse_arguments(*args):
    ''' Parse command line arguments. '''
    try:
        args = ''.join(*args)
    except TypeError:
        logging.info('no arguments passed, using defaults:')


def main(directory_path, args):
    sequence = args.sequence.__str__()
    logging.info('\nseq {}'.format(sequence))
    directory_path = dropbox_dir_path(sequence, directory_path)
    logging.info('directory: {}'.format(directory_path))
    files = get_filenames(directory_path)
    shots = shot_list(files)
    logging.info('first shot: {}'.format(shots[0]))
    logging.info('last shot: {}'.format(shots[-1]))
    missing = find_missing(shots)
    display_missing(missing)
    number_expected = abs(shots[-1] - shots[0]) + 1
    logging.info('number expected files: {}'.format(number_expected))
    display_duplicates(shots)


if __name__ == '__main__':
    # comment out the following line for testing
    # args = parser.parse_args()
    # uncomment the line below for testing
    args = argparse.Namespace(sequence=41)
    main(DROPBOX1_DIR, args)
    main(DROPBOX2_DIR, args)


