#!/usr/bin/python3

'''
Rename reports for Job 7021 e.g. from:
    seq-3601_NFH.pdf
to:
    3601_2023HWT21111PAS3601_NFH_FINAL.pdf
    
Line names are taken from the substitutions.csv file.

The substitutions.csv file is copied from the X drive to the logs folder.
This copied file is accessed to get line names.
Madey asked me to access the substitutions file from a copy, not the original.

Last update: 2023_09_09 Matthew Oppenheim
'''

import argparse
import logging
import os
from pathlib import Path
import shutil
import sys

ORIGINAL_LOG_DIRECTORY = r'S:\Seismic\Processing\00_Jobs_Temp\7021\AcquisitionReports'
RENAMED_LOG_DIRECTORY = r'S:\Seismic\Processing\00_Jobs_Temp\7021\AcquisitionReports_Source_NOAR_PDF_FINAL'
SUBS_FILE = r'X:\D01\Reveal_Projects\7021_Eni_Hewett_Src\substitutions.csv'

RENAMED_SUFFIX = r'_NFH_FINAL.pdf'
UNNAMED_PREFIX = r'seq-'
UNNAMED_SUFFIX = r'_NFH.pdf'

logging.basicConfig(level=logging.INFO, format='%(message)s')


def check_path(path):
    ''' Check path exists. '''
    if not os.path.exists(path):
        exit_code('*** cannot find path: {}'.format(path))
    else:
        logging.info('found path: {}'.format(path))


def copy_subs(subs_filepath, destination):
    ''' Copy subs file. '''
    dest_subs_path = os.path.join(destination, 'substitutions.csv')
    shutil.copyfile(subs_filepath, dest_subs_path)
    logging.debug('copied subs file at: {}'.format(dest_subs_path))


def create_new_filename(sequence, linename):
    ''' Create the new filename. '''
    new_filename = '{}_{}{}'.format(sequence, linename, RENAMED_SUFFIX)
    logging.debug('new_filename: {}'.format(new_filename))
    return new_filename


def exit_code(message):
    ''' Exits. '''
    logging.info(message)
    logging.info('exiting')
    raise SystemExit


def find_original_logs(ORIGINAL_LOG_DIRECTORY):
    ''' Create a list of filenames to rename in <ORIGINAL_LOG_DIRECTORY>. '''
    files_to_change = []
    for filename in os.listdir(ORIGINAL_LOG_DIRECTORY):
        if identify_original(filename):
            files_to_change.append(filename)
    return files_to_change


def get_sequence(old_filename):
    ''' Extract the sequence from <old_filename>. '''
    sequence = old_filename.split('-')[1]
    sequence = sequence.split('_')[0]
    return sequence


def identify_original(filename):
    ''' Identify if <filename> has not been renamed. '''
    if filename.startswith(UNNAMED_PREFIX) and filename.endswith(UNNAMED_SUFFIX):
        return True
    logging.debug('file not to rename: {}'.format(filename))
    return False


def new_filename(old_filename):
    ''' Create new filename for <old_filename>. '''
    seq_to_look_for = get_sequence(old_filename)
    with open(substitution_path(), 'r') as subs:
        for line in subs:
            line = line.split(',')
            sequence = line[0]
            if sequence == seq_to_look_for:
                linename = line[1]
                new_filename = create_new_filename(sequence, linename)
                return new_filename
    return None


def rename_logs(log_list, original_log_directory, renamed_log_directory):
    ''' Rename logs in <log_list>. '''
    for old_log in log_list:
        logging.debug('renaming: {}'.format(old_log))
        new_name = new_filename(old_log)
        try:
            new_path = os.path.join(renamed_log_directory, new_name)
        except TypeError as e:
            continue
        old_path = os.path.join(original_log_directory, old_log)
        logging.info('copying: {} to {}\n'.format(old_log, new_name))
        shutil.copy2(old_path, new_path)


def substitution_path():
    ''' Return the filepath of the copied substitution.csv file. '''
    subs_path = os.path.join(ORIGINAL_LOG_DIRECTORY, 'substitutions.csv')
    return subs_path


def main():
    check_path(ORIGINAL_LOG_DIRECTORY)
    check_path(RENAMED_LOG_DIRECTORY)
    check_path(SUBS_FILE)
    copy_subs(SUBS_FILE, ORIGINAL_LOG_DIRECTORY)
    check_path(substitution_path())
    logs_to_rename = find_original_logs(ORIGINAL_LOG_DIRECTORY)
    logging.debug('logs_to_rename: {}'.format(logs_to_rename))
    rename_logs(logs_to_rename, ORIGINAL_LOG_DIRECTORY, RENAMED_LOG_DIRECTORY)
    exit_code('ended normally')


if __name__ == '__main__':
    main()
