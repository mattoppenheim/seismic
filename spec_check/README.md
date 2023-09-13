spec_check.py

Tests edits files or a list of bad shots to check if they are in spec.
Checks against specs that are defined in tuples.
Get the specs from the job book for each project.

# check edits files

spec_check <sequence(s)>

e.g.

spec_check 3667

or

spec_check 3667-3669

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

There are often two further specs, the % of each line that can be bad and the %
of all shots for the entire survey.

Adjust the two global variables accordingly:

PERCENTAGE_PER_LINE

PERCENTAGE_SURVEY

# tests

tests are in tests_spec_check

Use pytest to run these

Last update: 2023_09_05 Matthew Oppenheim


