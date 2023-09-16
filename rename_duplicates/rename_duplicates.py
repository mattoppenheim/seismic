#!/usr/bin/python3
'''
Remove duplicate files for a given sequence from a dropbox folder.
Need to specify the dropbox folder to work in  by changing the global variable:

    DROPBOX = '....'

e.g.

    DROPBOX = r'dropbox02/dropobp-nfh'

Leave the preceding 'r' as this compensates for the directory / symbols.

Dependancies:
    missing_shots_dropbox.py
    range_strings.py

I wrote the above to solve other problems, might as well extend their use.
Inefficient code as the directory listing is read for each duplicate to create
a dictionary containing information about each duplicate.

Last update: 2023-09-08 Matthew Oppenheim.
'''

import argparse
from collections import namedtuple
import logging
from missing_shots_dropbox import MissingShots
import os
from pathlib import Path
from range_strings import find_duplicates, find_missing, get_ranges
import sys

# logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logging.getLogger().setLevel('DEBUG')

# the directory to look for duplicates in
DROPBOX = r'/nfs/dropbox02/dropobp-nfh/'

# directory with zero size files for testing
DROPBOX = r'/home/amuobpproc05/Documents/matt/testing/duplicate_shots_testing'

FILE_SUFFIX = r'.segd'

RENAMED_SUFFIX = r'.bak'

# tuple to describe duplicate files: (filename, modification time)
Duplicate = namedtuple("Duplicate", "name mtime")

# reminder for vim key mapping - ignore this
# nnoremap <leader>r :update<cr>:! %:p

def create_duplicate_dict(directory, duplicates):
    ''' Create duplicate_dict {shot, [duplicate_tuples]}. '''
    duplicate_dict = {}
    for filename in os.listdir(directory):
        if filename.endswith(FILE_SUFFIX) and any(filename.startswith(str(shot).zfill(5)) for shot in duplicates):
            filepath = os.path.join(directory, filename)
            update_duplicate_dict(duplicate_dict, filepath)
    return duplicate_dict


def filename_shot(filename):
    ''' Get the shot from the filename. '''
    return str(filename[:5])


def rename_all_duplicates(duplicate_dict, directory):
    ''' Rename the oldest duplicates for each shot in duplicate_dict. '''
    for shot in duplicate_dict.keys():
        oldest_dups = oldest_duplicates(duplicate_dict[shot])
        rename_shot_duplicates(oldest_dups, directory)


def rename_shot_duplicates(oldest_dups, directory):
    ''' Rename the filenames in oldest_dups. '''
    for duplicate in oldest_dups:
        filepath = os.path.join(directory, duplicate.name)
        renamed_filepath = '{}{}'.format(filepath, RENAMED_SUFFIX)
        logging.info('\ncommand: mv {} {}\n'.format(filepath, renamed_filepath))


def oldest_duplicates(duplicate_tuple_list):
    ''' Get the oldest duplicates for a single shot. '''
    # sort the tuples into age order
    duplicate_tuple_list.sort(key=lambda x:x[1], reverse=True)
    logging.debug('sorted tuples: {}'.format(duplicate_tuple_list))
    oldest_duplicates = duplicate_tuple_list[1:]
    logging.debug('tuples to rename: {}'.format(oldest_duplicates))
    return oldest_duplicates


def update_duplicate_dict(duplicate_dict, filepath):
    ''' Add Duplicate named tuple to the duplicate_dict for the shot_id in filepath. '''
    filename = os.path.basename(filepath)
    shot_id = filename_shot(filename)
    mtime = os.path.getmtime(filepath)
    duplicate_tuple = Duplicate(filename, mtime)
    if shot_id in duplicate_dict:
        duplicate_dict[shot_id].append(duplicate_tuple)
    else:
        duplicate_dict[shot_id] = [duplicate_tuple]
    return duplicate_dict


def main(directory, args):
    missing_shots = MissingShots(directory, args)
    shot_list = missing_shots.shots
    logging.debug('\nshots: {}'.format(shot_list))
    duplicate_shots = find_duplicates(shot_list)
    shot_directory = missing_shots.get_directory_path()
    duplicate_dict = create_duplicate_dict(shot_directory, duplicate_shots)
    rename_all_duplicates(duplicate_dict, directory)
    logging.debug('duplicate_dict: {}'.format(duplicate_dict))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('sequence', type=str, help='sequence(s) to find missing shots, can be a range')
    # comment out the following line for testing
    args = parser.parse_args()
    # uncomment the line below for testing
    # args = argparse.Namespace(sequence=SEQ)
    main(DROPBOX, args)
