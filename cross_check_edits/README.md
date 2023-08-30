cross_check_edits.py

To run e.g.

./cross_check_edits.py 3604

Accepts a range of sequences as well as single sequence e.g.

./cross_check_edits.py 3604-3610

Compares the _Hard_edits.csv and _Zero_depth.csv files for a given sequence.

Displays all the hard edits and zero edits.

Does not crash if a bogus sequence number is supplied. The script will display
that there are no edits or zero depths, which is correct, as there aren't any!
It's up to you to supply a valid sequence number.

Outputs the shot numbers that are in the _Zero_depths.csv file and not in the
_Hard_edits.csv file.

Outputs the shot numbers that are in the _Hard_edits.csv file and not in the
_Zero_depth.csv file.

Useful for checking that all _Zero_depth shots are in the _Hard_edits file.

Useful for checking up on edits that are not zero depth edits.

Matt Oppenheim, Amundsen, August 2023
