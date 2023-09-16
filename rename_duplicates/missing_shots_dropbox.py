#!/usr/bin/python3
''' List missing shots in dropbox1 and dropbox2 for a sequence.
Expects a sequence number to be supplied.
To run on e.g. sequence 38 type:
./missing_shots.py 38
Dependancy:
    range_strings.py needs to be in the same directory as this script
pip3 install termcolor for coloured output text.
Last update: 2023-06-09 Matthew Oppenheim.
'''

import argparse
import logging
import os
from pathlib import Path
from range_strings import find_duplicates, find_missing, get_ranges
import sys
# Stu added termcolor to highlight missing shots
# install with 'pip3 install termcolor -U'
try:
    from termcolor import colored
except ModuleNotFoundError as e:
    pass

logging.basicConfig(level=logging.INFO, format='%(message)s')

# default sequence value used if one is not supplied
SEQ = '17'

# base directory for folders containing shots
DROPBOX1_SHOTS = r'/nfs/dropbox01/dropobp/'

# base directory for folders containing re-exported shots
DROPBOX2_SHOTS = r'/nfs/dropbox02/dropobp/'

# base directory for folders containing nfh
DROPBOX1_NFH = r'/nfs/dropbox01/dropobp-nfh/'

# base directory for folders containing re-exported nfh
DROPBOX2_NFH = r'/nfs/dropbox02/dropobp-nfh/'


class MissingShots():


    def __init__(self, directory_path,  *args):
        self.main(directory_path, *args)


    def correct_shot_name(self, file_name):
        ''' Check that file_name is a valid segd file. '''
        if file_name.endswith('.segd') and file_name[:5].isdigit():
            return True
        return False


    def display_duplicates(self, duplicates):
        ''' Display information about duplicated shots. '''
        if len(duplicates) == 0:
            logging.info('+++ no duplicates found')
        else:
            logging.info('+++ duplicates: {}'.format(get_ranges(duplicates)))
        return duplicates


    def display_missing(self, missing):
        ''' Display missing shot information. '''
        if len(missing) == 0:
            logging.info('+++ no missing shots +++')
            return
        logging.info('')
        # if termcolor is installed, highlight missing shots
        try:
            logging.info((colored('!! !! !! ' 'missing shots !! -----> : {}'.format(get_ranges(missing)),'red')))
        except NameError as e:
            logging.info('+++ missing shots range +++\n\t{}'.format(get_ranges(missing)))
        logging.info('')
        logging.info('first missing shot: {}'.format(missing[0]))
        logging.info('last missing shot: {}'.format(missing[-1]))
        logging.info('number missing shots: {}'.format(len(missing)))


    def display_shot_info(self, shots):
        ''' Display information about the shots. '''
        logging.info('\nfirst shot: {}'.format(shots[0]))
        logging.info('last shot: {}'.format(shots[-1]))
        missing = find_missing(shots)
        self.display_missing(missing)
        number_expected = abs(shots[-1] - shots[0]) + 1
        logging.info('number expected files: {}'.format(number_expected))
        duplicates = find_duplicates(shots)
        self.display_duplicates(duplicates)


    def drop_dir_path(self, sequence, dropbox_dir):
        drop_dir_path = os.path.join(dropbox_dir, sequence)
        if not os.path.exists(drop_dir_path):
            logging.info('cannot find directory: {}'.format(drop_dir_path))
        return os.path.join(dropbox_dir, sequence)


    def exit_code(self, message):
        ''' Exits. '''
        logging.info(message)
        logging.info('exiting')
        raise SystemExit


    def get_directory_path(self):
        return self.directory_path


    def get_filenames(self, input_dir):
        ''' Create a list of filenames in input_dir sorted in time order. '''
        basepath = Path(input_dir)
        try:
            os.chdir(basepath)
        except FileNotFoundError as e:
            logging.info('directory path is not found: {}'.format(basepath))
            return None
        filenames = list(filter(os.path.isfile, os.listdir(basepath)))
        filenames.sort(key=lambda x: os.path.getmtime(x))
        return filenames


    def is_inc(self, shot_list):
        ''' Detect if shot_list is incrementing or decrementing. '''
        if shot_list[0] > shot_list[-1]:
            return False
        return True


    def parse_arguments(self, *args):
        ''' Parse command line arguments. '''
        try:
            args = ''.join(*args)
        except TypeError:
            logging.info('no arguments passed, using defaults:')


    def shot_list(self, filename_list):
        ''' Extract shots from the filenames. '''
        shot_list = []
        for filename in filename_list:
            # check that the file is a valid segd file
            if not self.correct_shot_name(filename):
                continue
            shot_list.append(int(filename[:5]))
        return shot_list


    def sort_shots(self, shot_list):
        ''' Sort the shots. '''
        # sometimes the shots are saved out of time order
        inc = self.is_inc(shot_list)
        if inc:
            shot_list.sort()
        else:
            shot_list.sort(reverse=True)
        return shot_list


    def main(self, directory_path, args):
        sequence = args.sequence.__str__()
        logging.info('\nseq {}'.format(sequence))
        self.directory_path = self.drop_dir_path(sequence, directory_path)
        if not self.directory_path:
            return
        logging.info('directory: {}'.format(self.directory_path))
        files = self.get_filenames(self.directory_path)
        if not files:
           return
        self.shots = self.shot_list(files)
        self.incrementing = self.is_inc(self.shots)
        self.sorted_shots = self.sort_shots(self.shots)
        self.display_shot_info(self.sorted_shots)


def sort_list(shot_list, is_incrementing):
    ''' Sort shot lists. '''
    if is_incrementing:
        shot_list.sort()
    else:
        shot_list.sort(reverse=True)
    return shot_list

def main(dropbox1, dropbox2, args):
    logging.info('\nlooking in: {} {}'.format(dropbox1, dropbox2))
    dropped1 = MissingShots(dropbox1, args)
    dropped2 = MissingShots(dropbox2, args)
    try:
        drop1_incrementing = dropped1.incrementing
    except AttributeError:
        return
    try:
        drop2_incrementing = dropped2.incrementing
    except AttributeError:
        return
    drop1_shots = dropped1.shots
    drop2_shots = dropped2.shots
    # I don't know why the class variables drop1_shots and drop2_shots are
    # always returned sorted in ascending order, not in the order they
    # exist in the class, so I added a sort_list function
    drop1_shots = sort_list(drop1_shots, drop1_incrementing)
    drop2_shots = sort_list(drop2_shots, drop2_incrementing)
    all_shots = [*drop1_shots, *drop2_shots]
    sorted_all_shots = dropped1.sort_shots(all_shots)
    logging.info('\nCombined shots for dropbox1 and dropbox2')
    dropped1.display_shot_info(sorted_all_shots)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('sequence', type=str, nargs='?', default=SEQ, help='sequence to find missing shots')
    # comment out the following line for testing
    args = parser.parse_args()
    # uncomment the line below for testing
    # args = argparse.Namespace(sequence=SEQ)
    main(DROPBOX1_SHOTS, DROPBOX2_SHOTS, args)
    main(DROPBOX1_NFH, DROPBOX2_NFH, args)
