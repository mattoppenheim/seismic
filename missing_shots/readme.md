# missing_shots_dropbox.py
June 2023 Matthew Oppenheim

This script looks for missing shots in dropbox1 and dropbox2. The shot numbers
contained in the filenames are used to find missing shots. The script imports the file called range_strings.py
which contains functions used to calculate and present the ranges of missing
shots.

For example, to run on sequence 41, cd to the directory where the script is saved and type:

./missing_shots_dropbox.py 41

Output:

seq 41
directory: /nfs/awa-data01/dropbox1/dropobp/41
first shot: 14530
last shot: 3312
missing shots: 14475-11721,9526-9480,8723-8412
first missing shot: 14475
last missing shot: 8412
number missing shots: 3114
number expected files: 11221
no duplicates found

seq 41
directory: /nfs/awa-data02/dropbox2/dropobp/41
first shot: 8723
last shot: 2750
missing shots: 8411-3310
first missing shot: 8411
last missing shot: 3310
number missing shots: 5102
number expected files: 5974
no duplicates found

The paths to the directory locations are contained in the script.

