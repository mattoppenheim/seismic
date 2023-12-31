#!/usr/bin/python3
''' Copy latest weekly plots to a directory so that the weekly PowerPoint can access them.
Supply the sequence number to take the plots from to put into the weekly.
example:
    copy_weekly_plots 40

example plot to copy and rename:

    3.Up-to-SEQ044-Areal-SEQ.png

renamed to:

    3.Up-to-SEQxxx-Areal-SEQ.png

Copies and renames files from the source directories to the target directories.
Files are renamed to be the same as in the file xxxx_PLOTS_LIST.md files.

Matthew Oppenheim.
Updating for AMU
last update: 2023_08_16
'''


import argparse
import os
from pathlib import Path
import logging
import sys

logging.basicConfig(level=logging.DEBUG, format='%(message)s')
#logging.basicConfig(level=logging.INFO, format='%(message)s')

# directory paths of the where to save the plots
SOURCE_DIR = '/nfs/D01/Reveal_Projects/7021_Eni_Hewett_Stmr/SuperVision/Weekly/'
SOURCE_SUBDIR_PREFIX='Up-to-SEQ'
COFF_TARGET_DIR = '/nfs/D01/Reveal_Projects/7021_Eni_Hewett_Stmr/SuperVision/Weekly/Cubes'
FOLD_TARGET_DIR = '/nfs/D01/Reveal_Projects/7021_Eni_Hewett_Stmr/SuperVision/Weekly/Fold_Maps'
PLOTS_TARGET_DIR = '/nfs/D01/Reveal_Projects/7021_Eni_Hewett_Stmr/SuperVision/Weekly/plots_for_powerpoint'

# files containing the list of plots that we want to copy

COFF_SOURCE='Cubes'
FOLD_SOURCE='Fold_Maps'
AREAL_SOURCE='ArealMaps'

COFF_PLOTS = 'coff_plots_amu.md'
FOLD_PLOTS = 'fold_plots_amu.md'
AREAL_PLOTS = 'areal_plots_amu.md'

parser = argparse.ArgumentParser()
parser.add_argument('sequence', type=str, help='sequence to copy plots from for the weekly report')


def copy_plots(paths_dictionary):
    ''' Copy from <source> to <target> for <source>:<target> in paths_dictionary. '''
    for source in paths_dictionary.keys():
        copy_command = 'cp {} {}'.format(source, paths_dictionary[source])
        logging.debug('\n*** {}\n'.format(copy_command))
        # comment out the following command during testing
        os.system(copy_command)


def erase_old_png(directory_path):
    ''' Delete all .png files in directory_path. '''
    logging.info('deleting png files from the target directory before copying in new ones')
    logging.info('target directory: {}'.format(directory_path))
    permission_to_proceed('\n*** all right to delete old plots from the target weekly_plots directory?\n')
    if not os.path.exists(directory_path):
        exit_code('target directory does not exist: {}'.format(directory_path))
    for filename in os.listdir(directory_path):
        filepath = os.path.join(directory_path, filename)
        if filepath.endswith('.png'):
            logging.debug('found file to erase: {}'.format(filepath))
            os.system('rm {}'.format(filepath))
        else:
            logging.debug('leaving this file alone: {}'.format(filepath))


def exit_code(message):
    ''' Exits. '''
    logging.info(message)
    logging.info('exiting')
    raise SystemExit


def find_extra_plots(source_plot_dir_path, plotslist):
    ''' Create a list of files in the source directory that are not in the weekly plot list. '''
    extra_plots = []
    plot_files = os.listdir(source_plot_dir_path)
    for plot in plot_files :
        plot_sourcepath = os.path.join(source_plot_dir_path, plot)
        if os.path.isfile(plot_sourcepath):
            if plot not in plotslist:
                logging.info('extra plot file in source directory: {}'.format(plot))
                extra_plots.append(plot)
    return extra_plots


def oldest_directory(dir_path):
    ''' Find the oldest sub directory in <dir_path>. '''
    sub_directories = [dir for dir in os.listdir(dir_path) if os.path.isdir(dir)]
    return max(sub_directories, key=os.path.getmtime)


def paths_dictionary(plots_to_copy, source_directory, target_directory, sequence):
    ''' Create a dictionary <source_plot_path>, <target_plot_path>. '''
    plots_dict = {}
    for plotname in plots_to_copy:
        source_path = os.path.join(source_directory, plotname)
        target_name = plotname.replace('SEQ{}'.format(sequence.zfill(3)), 'SEQxxx')
        target_path = os.path.join(target_directory, target_name)
        plots_dict[source_path] = target_path
    return plots_dict


def permission_to_proceed(message):
    ''' Get user permission to proceed. '''
    permission = input('{}\n press y to proceed\n'.format(message))
    if permission in ['y', 'Y']:
        pass
    if permission in ['q', 'Q']:
        exit_code("Quit command received")


def plots_to_find(weekly_plots_list_filepath, sequence):
    ''' Create a list of plot files to look for by renaming plot names found in weekly_plots_list_filepath. '''
    plotlist = []
    if not os.path.isfile(weekly_plots_list_filepath):
        exit_code('weekly plots list not found: {}'.format(weekly_plots_list_filepath))
    # want plots from the newest subdirectory
    logging.info('\nlooking for plots to copy in: {}'.format(weekly_plots_list_filepath))
    with open(weekly_plots_list_filepath, 'r') as plot_names:
        next(plot_names)
        for plot in plot_names:
            plot = plot.strip()
            plot = rename_plot(plot, sequence)
            if plot is None:
                continue
            plotlist.append(plot)
    return plotlist


def rename_plot(plotname, sequence):
    ''' Rename the plot with the sequence number. '''
    new_seq_name = 'SEQ{}'.format(sequence.zfill(3))
    try:
        plotname = plotname.replace('SEQxxx', new_seq_name)
    except NameError as e:
        logging.info('\nunable to create plotfile for: {}'.format(plot))
        logging.debug(e)
        return None
    return plotname


def source_directory_path(sequence, plot_sub_directory):
    ''' Find the path to where we copy plots from. '''
    sequence = sequence.zfill(3)
    seq_subdir = '{}{}'.format(SOURCE_SUBDIR_PREFIX,sequence)
    source_path = os.path.join(SOURCE_DIR, plot_sub_directory, seq_subdir)
    if not os.path.exists(source_path):
        exit_code('plots directory: {} not found'.format(source_path))
    return source_path


def copy_weekly_plots(sequence, plots_sub_directory, plots_list):
    ''' Find and copy weekly plots in <plots_list> from the source sub_directory. '''
    # look for the source directory to copy plots from
    source_dir_path = source_directory_path(sequence, plots_sub_directory)
    logging.info('\nfound source_dir_path: {}'.format(source_dir_path))

    # create a list of plots to look for
    plotslist = plots_to_find(plots_list, sequence)

    # see if there are extra plots in the source directory that are not in
    # plots_list

    extra_plots = find_extra_plots(source_dir_path, plotslist)
    if len(extra_plots) == 0:
        logging.info('no extra plots in the source directory')

    # remove any extra plots from the list of plots to copy
    plots_to_copy = list(set(plotslist) - set(extra_plots))

    # make a dictionary of <source_path>:<target_path> for each plot
    directory_to_copy_to = os.path.join(PLOTS_TARGET_DIR, plots_sub_directory)
    paths_dict = paths_dictionary(plots_to_copy, source_dir_path, directory_to_copy_to, sequence)

    # erase any png files already in the target directory
    erase_old_png(directory_to_copy_to)

    # copy over plots from the source directory
    logging.info('\ncopying files to the target directory')
    copy_plots(paths_dict)


def main(args):
    sequence = args.sequence.__str__()
    logging.info('\nseq {}'.format(sequence))
    copy_weekly_plots(sequence, AREAL_SOURCE, AREAL_PLOTS)
    copy_weekly_plots(sequence, COFF_SOURCE, COFF_PLOTS)
    copy_weekly_plots(sequence, FOLD_SOURCE, FOLD_PLOTS)


if __name__ == '__main__':
    # comment out the following line for testing
    args = parser.parse_args()
    # uncomment the line below for testing
    # args = argparse.Namespace(sequence=37)
    main(args)
