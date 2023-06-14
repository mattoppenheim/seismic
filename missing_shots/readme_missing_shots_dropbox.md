# Python scripts

Matthew Oppenheim
last update: 2023_06_09

## missing_shots_dropbox.py

### Summary

Checks dropbox1 and dropbox2 for missing or duplicated shots for a sequence.

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

seq 47
directory: /nfs/awa-data01/dropbox1/dropobp/47

first shot: 2719
last shot: 14520

*** missing shots range ***
	3889-4749, 6857-8039, 12168-13085

first missing shot: 3889
last missing shot: 13085
number missing shots: 2962
number expected files: 11802
no duplicates found

seq 47
directory: /nfs/awa-data02/dropbox2/dropobp/47

first shot: 3889
last shot: 13085

+++ missing shots range +++
	4750-6856, 8040-12167

first missing shot: 4750
last missing shot: 12167
number missing shots: 6235
number expected files: 9197
no duplicates found

Combined shots for dropbox1 and dropbox2

first shot: 2719
last shot: 14520
+++ no missing shots +++
number expected files: 11802
no duplicates found

### Tests

I wrote some tests for the range_strings.py functions. These are in the file:

test_find_ranges.py

Run using:
python -m pytest

The script was tested on various sequences that had missing shots and
duplicates.

