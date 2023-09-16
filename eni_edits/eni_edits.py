#!/usr/bin/python3

'''
Create ENI format edit files
Input: Reveal format .csv edit file
Output: ENI format file
example Reveal edit line:
shot_1, shot_2, str_chan_1, str_chan_2, str_1, str_2
12071,12071,699,701,3,3

eni format edit line (text, shots, channels):

    TDELETE   TRACE_NUM        12071         2297:2299

_Hard_shot_edits.csv files are different. They only have shot_1, shot_2 information.

Last update 2023_09_14 Matthew Oppenheim
'''

import logging
import os
from pathlib import Path
from range_strings import find_missing, get_ranges
import sys
from tools import exit_code, first_last_seq, verify_path

logging.basicConfig(level=logging.debug, format='%(message)s')
#logging.getLogger().setLevel('DEBUG')


class EniEdits:

    # default sequence value used if one is not supplied
    SEQ = '003'
    CHANNELS_PER_STREAMER = 799

    # field numbers for information in the edits file, starts at 0
    EDITS_SHOT_1 = 0
    EDITS_SHOT_2 = 1
    EDITS_TRACE_1 = 2
    EDITS_TRACE_2 = 3
    EDITS_STR_1 = 4
    EDITS_STR_2 = 5

    # default sequence value used if one is not supplied
    SEQ = '003'
    # Reveal edits directory
    REVEAL_EDITS_DIR = r'/nfs/D01/Reveal_Projects/7021_Eni_Hewett_Stmr/tables/edits/edits_QC'

    SUBS_FILE = r'/nfs/D01/Reveal_Projects/7021_Eni_Hewett_Stmr/substitutions.csv'
    # column numbers for information in the substitutions.csv file, starts at 0
    SUBS_LINENAME_COLUMN = 1
    SUBS_FSP_COLUMN = 7
    SUBS_LSP_COLUMN = 8
    SUBS_SEQ_COLUMN = 0

    # if a reveal channel number is '9999' this means all channels are bad
    ALL_FLAG = 9999
    # number streamers, for when shot edit files need information adding
    MAX_STREAMER = 6

    def __init__(self, reveal_suffix, eni_suffix, eni_output_dir):
        self.verify_paths()
        self.reveal_suffix = reveal_suffix
        self.eni_suffix = eni_suffix
        self.eni_output_dir = eni_output_dir


    def abs_chan_num(self, channel, streamer):
        ''' Calculate absolute channel number. '''
        return (int(streamer)-1)*self.CHANNELS_PER_STREAMER + int(channel)


    def add_chans_streamer(self, split_reveal_edit):
        ''' Add channel and streamer entry to a split reveal edits entry. '''
        logging.debug('split_reveal_edit: {}'.format(split_reveal_edit))
        chans_streamer = [1, self.CHANNELS_PER_STREAMER, 1, self.MAX_STREAMER]
        split_reveal_edit.extend(chans_streamer)
        logging.debug('split_reveal_edit: {}'.format(split_reveal_edit))
        return split_reveal_edit


    def add_edits(self, reveal_edits_filepath, eni_edits_filepath):
        ''' Parse reveal edits to eni format and write to eni_edits_filepath. '''
        with open(reveal_edits_filepath, 'r') as edits:
            # first line contains headers
            edits.readline()
            for line in edits:
                eni_shot_range, eni_chan_range =  self.parse_reveal_edit(line)
                eni_edit_line = self.format_eni_line(eni_shot_range, eni_chan_range)
                self.writeline(eni_edits_filepath, eni_edit_line)


    def all_flag(self,channel):
        ''' If channel is the ALL_FLAG for a bad shot, return the maximum channel in the streamer. '''
        if int(channel) == int(self.ALL_FLAG):
            logging.debug('\n*** all flag: {}'.format(channel))
            return self.CHANNELS_PER_STREAMER
        return channel


    def calc_eni_chan_range(self, reveal_chan_range, reveal_streamer):
        ''' Create channel string to go into eni edit. '''
        split_chan_range = self.reveal_chan_range.split('-')
        logging.debug('split_chan_range: {} streamer: {}'.format(split_chan_range, reveal_streamer))
        if len(split_chan_range) == 1:
            return self.abs_chan_num(reveal_chan_range, reveal_streamer)
        else:
            f_chan = self.abs_chan_num(split_chan_range[0], reveal_streamer)
            l_chan = self.abs_chan_num(split_chan_range[-1], reveal_streamer)
            return '{}:{}'.format(f_chan, l_chan)


    def channel_num(self,channel, streamer):
        ''' Return absolute channel number. '''
        return (streamer-1)*CHANNELS_PER_STREAMER + channel


    def comment_1(self, line_ident):
        ''' Prepare comment line 1. '''
        c1 = '{:<9s}{:<20s}'.format('LINE',line_ident)
        return c1


    def comment_2(self):
        return '$TRCDLRV'


    def comment_3(self):
        return ' *DELREVDEF'


    def comment_4(self):
        return '    DELREV = SHOTPOINT_NUM'


    def comment_6(self):
        return '{:3s}{:<10s}{:3s}{:<7s}{:6s}{:<6s}{:4s}{:<13s}{:2s}{:<11s}'.format(' ',r'<OPERATION',' ','LITERAL',
                ' ', 'GATHER', ' ', 'LITERAL_VALUE', ' ', 'DETECT_TYPE')


    def format_eni_line(self, shots, channels):
        ''' Create formatted eni edits line. '''
        eni_line = '{:<4s}{:<9s}{:<1s}{:<9s}{:<7s}{:<14s}{:<s}'.format('','TDELETE','','CHANNEL','', shots,channels)
        logging.debug(eni_line)
        return eni_line


    def initialise_file(self, filepath):
        ''' Create blank file. '''
        with open(filepath, 'w') as file:
            pass
        logging.debug('created empty file: {}'.format(filepath))


    def line_ident(self, seq, subs_filepath = SUBS_FILE):
        ''' Get the line identifier from the substitutions file. '''
        with open(subs_filepath, 'r') as subs:
            for line in subs:
                line = line.split(',')
                sequence = line[self.SUBS_SEQ_COLUMN]
                # lots of lines just containing ',' in the subs file
                if sequence == seq:
                    line_ident = line[self.SUBS_LINENAME_COLUMN]
                    logging.debug('seq: {} line_ident in subs file: {}'.format(seq, line_ident))
                    return line_ident
        exit_code('no line_ident found for seq {} in {}'.format(seq, subs_filepath))


    def output_filepath(self, seq, line_ident, dir):
        ''' Create filename for output file. '''
        eni_filename = '{}_{}{}'.format(seq, line_ident, self.eni_suffix)
        logging.debug('output filename: {}'.format(eni_filename))
        return os.path.join(dir, eni_filename)


    def parse_reveal_edit(self, reveal_edit):
        ''' Translate reveal edit line to eni format. '''
        # see comments at top for an example input and output
        reveal_edit = reveal_edit.strip()
        logging.debug('\nreveal_edit: {}'.format(reveal_edit))
        split_reveal_edit = reveal_edit.strip().split(',')
        logging.debug('split_reveal_edit: {}'.format(split_reveal_edit))
        shot_1 = split_reveal_edit[self.EDITS_SHOT_1]
        shot_2 = split_reveal_edit[self.EDITS_SHOT_2]
        if shot_1 == shot_2:
            eni_shot_range = '{}'.format(shot_1)
        else:
            eni_shot_range = '{}:{}'.format(shot_1, shot_2)
        # Hard_shot_edits only have shot information, need to fake the rest
        try:
            chan_1 = split_reveal_edit[self.EDITS_TRACE_1]
        except IndexError:
            logging.debug('faking channels and streamer entries')
            split_reveal_edit = self.add_chans_streamer(split_reveal_edit)
            chan_1 = split_reveal_edit[self.EDITS_TRACE_1]
        chan_2 = split_reveal_edit[self.EDITS_TRACE_2]
        chan_1 = self.all_flag(chan_1)
        chan_2 = self.all_flag(chan_2)
        str_1 = split_reveal_edit[self.EDITS_STR_1]
        str_2 = split_reveal_edit[self.EDITS_STR_2]
        abs_chan_1 = self.abs_chan_num(chan_1, str_1)
        abs_chan_2 = self.abs_chan_num(chan_2, str_2)
        if abs_chan_1 == abs_chan_2:
            eni_chan_range = '{}'.format(abs_chan_1)
        else:
            eni_chan_range = '{}:{}'.format(abs_chan_1, abs_chan_2)
        logging.debug('eni_shot: {} eni_chan_range: {}'.format(eni_shot_range, eni_chan_range))
        return eni_shot_range, eni_chan_range


    def process_all_sequences(self, sequences):
        ''' Process all the sequences. '''
        # get first and last sequence from input sequence string e.g. '10-20'
        first_seq, last_seq = first_last_seq(sys.argv[1:])
        logging.info('Looking for seq {} to {}'.format(first_seq, last_seq))
        for seq in range(first_seq, last_seq+1):
            self.process_single_seq(str(seq).zfill(3))
        logging.info('completed normally\n')


    def process_single_seq(self, seq):
        ''' Process a single sequence. '''
        seq_line_ident = self.line_ident(seq)
        reveal_edits_filepath = self.reveal_edits_path(seq, self.reveal_suffix)
        out_filepath = self.output_filepath(seq, seq_line_ident, self.eni_output_dir)
        self.initialise_file(out_filepath)
        self.write_header(seq_line_ident, out_filepath)
        self.add_edits(reveal_edits_filepath, out_filepath)
        logging.info('created edits file for seq: {} ending {}'.format(seq, self.eni_suffix))


    def reveal_edits_path(self, seq, reveal_file_suffix, edits_dir=REVEAL_EDITS_DIR):
        ''' Return filepath to the reveal edits file. '''
        reveal_edits_filename = '{}{}'.format(seq, reveal_file_suffix)
        for filename in os.listdir(edits_dir):
            if filename == reveal_edits_filename:
                logging.debug('reveal_edits filename: {}'.format(filename))
                return os.path.join(edits_dir, filename)
        logging.debug('seq: {} no reveal_edits file'.format(seq))


    def verify_paths(self):
        ''' Verify paths exist. '''
        verify_path(self.REVEAL_EDITS_DIR)
        verify_path(self.SUBS_FILE)


    def write_header(self, seq_line_ident, out_filepath):
        ''' Write the header lines to the output file. '''
        c1 = self.comment_1(seq_line_ident)
        c2 = self.comment_2()
        c3 = self.comment_3()
        c4 = self.comment_4()
        c5 = ''
        c6 = self.comment_6()
        for line in [c1, c2, c3, c4, c5, c6]:
            self.writeline(out_filepath, line)


    def writeline(self, outputfile, line):
        ''' Append a line to the output file. '''
        with open(outputfile, 'a') as file:
            file.writelines('{}{}'.format(line,'\n'))

