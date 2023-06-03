#!/usr/bin/python3
''' List missing shots in a directory.
June 2023 Matthew Oppenheim.
v1.0 used successfully
'''


import argparse
import os
from pathlib import Path
import logging
from range_strings import *
import sys

logging.basicConfig(level=logging.DEBUG, format='%(message)s')
SEQ = '40'
# DROPBOX_DIR = r'/nfs/awa-data01/dropbox1/dropobp/39'
DROPBOX_DIR = r'/nfs/awa-data01/dropbox1/dropobp/'
# DROPBOX_DIR = r'/nfs/awa-data02/dropbox2/dropobp/38_not_used'


parser = argparse.ArgumentParser()
parser.add_argument('sequence', type=str, default=SEQ, help='sequence to find missing shots')


def display_missing(missing):
    ''' Display missing shot information. '''
    if len(missing) == 0:
        logging.info('no missing shots')
        return
    logging.info('missing shots: {}'.format(missing))
    logging.info('first missing shot: {}'.format(missing[0]))
    logging.info('last missing shot: {}'.format(missing[-1]))
    logging.info('number missing: {}'.format(len(missing)))


def dropbox_dir_path(sequence):
    return os.path.join(DROPBOX_DIR, sequence)


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
    logging.info('seq {}'.format(sequence))
    directory_path = dropbox_dir_path(sequence)
    logging.info('directory: {}'.format(directory_path))

    files = get_filenames(directory_path)
    shots = shot_list(files)
    logging.info('args: {}'.format(args))
    logging.info('first shot: {}'.format(shots[0]))
    logging.info('last shot: {}'.format(shots[-1]))
    missing = find_missing(shots)
    display_missing(missing)

    number_expected = abs(shots[-1] - shots[0]) + 1
    logging.info('number expected files: {}'.format(number_expected))

    logging.info('duplicates: {}'.format(find_duplicates(shots)))


if __name__ == '__main__':
    args = parser.parse_args()
    #args = argparse.Namespace(sequence=38)
    main(DROPBOX_DIR, args)


