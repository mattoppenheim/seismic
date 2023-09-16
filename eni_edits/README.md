# eni_edits

Scripts for creating ENI format edits.

Input: Reveal format .csv edit file
Output: ENI format file

The file all_edits.py is used to create the edit files. The other files in the
directory are used by this script.

## to run

To run:

./all_eni_edits.py <sequences>

A single or a range of sequences needs to be supplied.

e.g.

./all_eni_edits.py 3-45

## edits file contents

example Reveal edit line:
shot_1, shot_2, str_chan_1, str_chan_2, str_1, str_2
12071,12071,699,701,3,3

eni format edit line (text, shots, channels):

    TDELETE   TRACE_NUM        12071         2297:2299

_Hard_shot_edits.csv files are different. They only have shot_1, shot_2 information.

## eni edits files

The output format conforms to the requirements in 05.5_Ref_02__AESI-P-MAN-02-Rev01.PDF.

eni_edits.py contains the EniEdits class. This class is used by
all_eni_edits.py script to create ENI format edits.

The script pads out the sequences to be 3 characters, e.g. 003.

## how to add a new eni edits file

In the scripts, change the input and output directories. Change the eni edit
file suffix and the Reveal edit file suffix.

## how to setup for a new project

Between jobs, in the eni_edits file, change the number of streamers and number
of channels in the variables:

MAX_STREAMER
CHANNELS_PER_STREAMER

Update the path to the subsitutions file:

SUBS_FILE

Information is extracted from the substitutions.csv file. The column information is stored in
the globals that start SUBS\_. These need to be updated if the format of the
substitutions.csv file changes.


