Checks for missing plots in the Supervision final plots directories for a given sequence.
To run:
python3 check_final_plots.py <seq>
e.g.
python3 check_final_plots.py 50

The script looks for a list of expected file suffices in:

plot_names.md

The missing plots are displayed.

Unexpected extra plot suffices are displayed.
