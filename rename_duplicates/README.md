# rename_duplicates

Renames files with the same file number in a dropbox folder.  Renames the oldest
files to <filename>.bak.  Leaves the youngest duplicate file alone.

The use case is when there are corrupted files in the dropbox folder and new
files are copied over, which have the same file numbe as the corrupted files.

Renaming the corrupted files to <filename>.bak removes them from the data set
that will be seen by the processing software.

The script assumes that the corrupted files will be older than the uncorrupted
files. Duplicate files are found and the oldest ones have .bak appended to the
filename.
