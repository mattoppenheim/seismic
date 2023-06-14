# copy_weekly_plots path:
/nfs/awa-data01/Reveal_Projects/3163_CGG_NVG_3D_2023/Scripts/copy_weekly_plots/copy_weekly_plots.py

copies and renames files from a weekly plot folder and saves them in:

V:\Reveal_Projects\3163_CGG_NVG_3D_2023\SuperVision\Weekly\plots_for_weekly

The renamed plots are linked to the PowerPoint presentations here:

S:\Seismic\Jobs\3163-AWA-CGG-NVG-2023\103_FieldGeo\04_Weekly_Outputs\testing_templates

The template PowerPoints are: CGG23001_Areal_Maps_Seqaaa-bbb_ddmm2023.pptx
CGG23001_Coff_Cube_Seqaaa-bbb_ddmm2023.pptx
CGG23001_Fold_Coverage_Seq-nnn_ddmm2023.pptx

## usage

./copy_weekly_plots <sequence>

e.g.

./copy_weekly_plots 36

This copies all of the plots from the weekly plot folder in SuperVision for seq
36 to the plots_for_weekly folder. The plots are all renamed - the sequence
number is replaced with 'xxx'. This allows the plot names to be linked in the
PowerPoint.

The existing plots in the plots_for_weekly folder are deleted. You need to
explicitly say 'y' to do this. There may be a scenario when you don't want to
delete the previous week's plots from the target folder. I figure it's safer to
have a check before deleting data. No data is deleted from anywhere else.
Probably.

There are three sets of data to copy, one for each of the three PowerPoints we
produce.

The files containing the list of plots names for each of the PowerPoints are:

attribute_plots_list.md coff_plots_list.md fold_plots_list.md

The example plot names have a sequence number in them. This sequence number does
not matter - it is replaced with xxx in the plots_for_weekly folder. The
sequence number can be any three numbers, the rest of the text is what is
searched for in the source directories.

Close and open the relevant template PowerPoint and the latest plots appear.

**Save the template PowerPoint with a new name.**

At some point, you'll forget to do this and overwrite a template. Backups of the
templates are at:

S:\Seismic\Processing\Personal\Matt\testing_templates

Break the links to the plots in the SuperVision folder, or when these change, so
will the plots in the PowerPoint. Plus, if you send the PowerPoint off the ship,
none of the plots will display as the PowerPoint will be looking for the plots
on the ship.

To break the links: Go to the 'Files' tab.  On the left hand menu bar, select
the 4th option down 'Info'.  On the right hand side of the screen, almost at the
bottom, there is a tiny option called 'Edit Links to Files', just above the red
text 'Show All Properties'. Click on this.

For each of the links in the window, click on 'break link'. Now save the file.

Update sequence numbers and dates. Check through as any of the previous week's
annotations may or may not still be visible. Need to test to find out.
