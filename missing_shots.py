#!/usr/bin/python3
''' List missing shots in a directory.
June 2023 Matthew Oppenheim. '''

import os
from pathlib import Path
import logging
from range_strings import *

logging.basicConfig(level=logging.DEBUG, format='%(message)s')
SEQ = '38'
DROPBOX_DIR = r'/nfs/awa-data01/dropbox1/dropobp/39'
# DROPBOX_DIR = r'/nfs/awa-data02/dropbox2/dropobp/38'

def display_first_last(input_list):
    ''' Display the first and last 5 items in input_list. '''
    logging.info('first shots: {}'.format(input_list[:5]))
    logging.info('last shots: {}'.format(input_list[-5:]))


def shot_list(filename_list):
    ''' Extract shots from the filenames. '''
    shot_list = []
    for filename in filename_list:
        shot_list.append(int(filename[:5]))
    shot_list.sort()
    return shot_list


def get_filenames(input_dir):
    ''' Creates a list of filenames in input_dir. '''
    basepath = Path(input_dir)
    filenames = (os.path.basename(entry) for \
      entry in basepath.iterdir() if entry.is_file())
    return list(filenames)


def parse_arguments(*args):
    ''' Parse command line arguments. '''
    try:
        args = ''.join(*args)
    except TypeError:
        logging.info('no arguments passed, using defaults:')
        #logging.

def main(directory_path):
    files = get_filenames(directory_path)
    shots = shot_list(files)

    missing = find_missing(shots)
    number_expected = shots[-1] - shots[0] + 1
    logging.info('missing: {}'.format(get_ranges(find_missing(shots))))
    display_first_last(shots)
    logging.info('first shot: {}'.format(shots[0]))
    logging.info('last shot: {}'.format(shots[-1]))
    logging.info('first missing shot: {}'.format(missing[0]))
    logging.info('last missing shot: {}'.format(missing[-1]))
    logging.info('number expected files: {}'.format(number_expected))
    logging.info('number missing: {}'.format(len(missing)))
    logging.info('duplicates: {}'.format(find_duplicates(shots)))


if __name__ == '__main__':
    main(DROPBOX_DIR)


