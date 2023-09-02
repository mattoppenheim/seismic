# Python scripts

Matthew Oppenheim
last update: 2023_08_11

## missing_shots_dropbox.py

### Summary

Checks dropbox1 and dropbox2 for missing or duplicated shots for a sequence.

Updated on the AMU to check both dropobp and dropobp-nfh

Outputs ranges of missing shots.  Presents information for each dropbox and for
an amalgamated data set containing all shots found.

Safe to use online.

Works by creating a list of the file numbers found in the dropbox1 and dropbox2
directories for the target sequence.

### Dependencies

Uses functions from the file 'range_strings.py'. This must be in the same directory as
missing_shots_dropbox.py.

I could copy the functions into missing_shots_dropbox.py, but then I'd be
maintaining two scripts and associated tests each time I edit the functions.

If you want coloured output text:

pip3 install termcolor -U

The script still runs if this is not installed.

### Arguments

<sequence number>

### Example

[amuobpproc05@amu-wkst04 missing_shots]$ python3 missing_shots_dropbox.py 22

looking in: /nfs/dropbox01/dropobp/ /nfs/dropbox02/dropobp/

seq 22
directory: /nfs/dropbox01/dropobp/22

first shot: 1779
last shot: 4931

+++ missing shots range +++
	3012-3014

first missing shot: 3012
last missing shot: 3014
number missing shots: 3
number expected files: 3153
no duplicates found

seq 22
directory: /nfs/dropbox02/dropobp/22

first shot: 3012
last shot: 3014
+++ no missing shots +++
number expected files: 3
no duplicates found

Combined shots for dropbox1 and dropbox2

first shot: 1779
last shot: 4931
+++ no missing shots +++
number expected files: 3153
no duplicates found

looking in: /nfs/dropbox01/dropobp-nfh/ /nfs/dropbox02/dropobp-nfh/

seq 22
cannot find directory: /nfs/dropbox01/dropobp-nfh/22
directory: /nfs/dropbox01/dropobp-nfh/22
directory path is not found: /nfs/dropbox01/dropobp-nfh/22

seq 22
directory: /nfs/dropbox02/dropobp-nfh/22

first shot: 1789
last shot: 4921
+++ no missing shots +++
number expected files: 3133
no duplicates found

### Tests

I wrote some tests for the range_strings.py functions. These are in the file:

test_find_ranges.py

Run using:
python -m pytest

The script was tested on various sequences that had missing shots and
duplicates.

