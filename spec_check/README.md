check_bad_shot_range.py

Tests edits files or a list of bad shots to check if they are in spec.
Checks against specs that are defined in tuples.

# check edits files

check_bad_shot_ranges <sequence(s)>

e.g.

check_bad_shot_ranges 3667

or

check_bad_shot_ranges 3667-3669

If no sequence(s) are supplied, the script iterates through
everything that is in the substitutions.csv file.

# supply a list of shots

Check that a line is still in spec when there are bad shots.
Supply the bad shots as a list called:

    BAD_SHOT_LIST

e.g.

[1 ,2 ,3, 500]

ranges can be supplied, e.g.

 [33, '50-60', '72-80']

Note that the ranges are supplied as strings, e.g.

'50-60'

# define specs

The specs are supplied as tuples in the form:

 (max number edits, number of shots to check over)

e.g. (9, 80) means 9 shots bad in an 80 shot range is illegal.

# tests

tests are in tests_check_bad_shot_range

Use pytest to run these

Last update: 2023_09_05 Matthew Oppenheim


