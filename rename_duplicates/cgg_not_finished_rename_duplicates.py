#!/usr/bin/python3
''' Rename duplicate files.
June 2023 Matt Oppenheim
NOT TESTED - DO NOT USE
'''

import logging
import os
from pathlib import Path

logging.basicConfig(level=logging.DEBUG, format='%(message)s')


DROP2 = r'/nfs/awa-data02/dropbox2/dropobp'
MISSING_SHOTS_FILE_DIR = r'/nfs/awa-data01/Reveal_Projects/3163_CGG_NVG_3D_2023/tables/P1_SegdQC/SPs_CHANs_NFHs_check/'
MISSING_SHOTS_FILE_SUFFIX = r'-missing-dup-NFH.csv'
SEQ = '38'
SHOTS_TO_COPY_SUFFIX = '_missing.txt'
SOURCE_DIR_SUFFIX = '_not_used'
SOURCE_DIR_SUFFIX = '_testing'


def create_move_command(shot_filename, source_directory, target_directory):
    ''' Create the Linux command to move the shot file. '''
    source_filepath = os.path.join(source_directory, shot_filename)
    target_filepath = os.path.join(target_directory, shot_filename)
    command_string = 'mv {} {}'.format(source_filepath, target_filepath)
    return command_string


def exit_code(message):
    ''' Exits. '''
    logging.info(message)
    logging.info('exiting')
    raise SystemExit


def find_missing_shot(missing_shot, source_directory):
    ''' Find shot in source_directory. '''
    logging.info('looking for missing shot {} in {}'.format(missing_shot, source_directory))
    missing_shot = missing_shot.strip().zfill(5)
    for shotfilename in os.listdir(source_directory):
        shot_number = shotfilename[:5].__str__()
        logging.info('shot_number: {} missing_shot: {}'.format(shot_number, missing_shot))
        if shot_number.endswith(missing_shot.__str__()):
            logging.info('found source shot: {}'.format(shotfilename))
            return shotfilename


def find_source_directory(basepath, sequence):
    ''' Return path to source directory. '''
    for directory in os.listdir(basepath):
        if directory.startswith(sequence):
            if directory.endswith(SOURCE_DIR_SUFFIX):
                source_directory = os.path.join(basepath, directory)
                return(source_directory)


def find_target_directory(basepath, sequence):
    ''' Return path to source directory. '''
    for directory in os.listdir(basepath):
        if directory.startswith(sequence):
            target_directory = os.path.join(basepath, directory)
            return(target_directory)


def move_shots(missing_shots_filepath, source_directory, target_directory):
    ''' Move missing shots to target directory. '''
    with open(missing_shots_filepath, 'r') as missingshots_file:
        next(missing_shots_file)
        for shot in missing_shots_file:
            shot = shot.split(',')[:1]
            logging.info('shot: {}'.format(shot))
            shot_filename = find_missing_shot(shot, source_directory)
            move_command = create_move_command(shot_filename, source_directory, target_directory)
            logging.info('move command: {}'.format(move_command))
            # os.system(move_command)


def missing_shotlist_filepath(basepath, sequence):
    ''' Return path to file containing missing shots. '''
    missing_shotlist_dir = os.path.join(basepath, sequence.zfill(3))
    for filename in os.listdir(missing_shotlist_dir):
        if filename.startswith(sequence.zfill(3)) and filename.endswith(MISSING_SHOTS_FILE_SUFFIX):
            missing_shots_filepath = os.path.join(basepath, filename)
            return(missing_shots_filepath)
    exit_code('No file ending {} found for seq {} in {}'.format(MISSING_SHOTS_FILE_SUFFIX, sequence, missing_shotlist_dir))


def main(sequence=SEQ):
    source_directory = find_source_directory(DROP2, sequence)
    target_directory = find_target_directory(DROP2, sequence)
    '''
    if source_directory is None:
         exit_code('cannot find source directory for {}'.format(sequence))
    if target_directory is None:
         exit_code('cannot find target directory for {}'.format(sequence))
    '''
    logging.info('found source directory for {}: {}'.format(sequence, source_directory))
    logging.info('found target directory for {}: {}'.format(sequence, target_directory))
    missing_shots_filepath = missing_shotlist_filepath(MISSING_SHOTS_FILE_DIR, sequence)
    if missing_shots_filepath is None:
        exit_code('cannot find missing shots file for {}'.format(sequence))
    logging.info('found missing shots file for {}: {}'.format(sequence, missing_shots_filepath))
    # move_shots(missing_shots_filepath, source_directory, target_directory)


if __name__ == '__main__':
    main()


