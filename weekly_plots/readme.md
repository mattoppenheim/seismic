# copy_weekly_plots path:
/nfs/awa-data01/Reveal_Projects/3163_CGG_NVG_3D_2023/Scripts/copy_weekly_plots/copy_weekly_plots.py

Copies and renames .png files from:
/nfs/D01/Reveal_Projects/7021_Eni_Hewett_Stmr/SuperVision/Weekly/plots_for_powerpoint

To:

/nfs/D01/Reveal_Projects/7021_Eni_Hewett_Stmr/SuperVision/Weekly/plots_for_powerpoint

The renamed plots are linked to the PowerPoint presentations here:

S:\Seismic\Jobs\7021-AMU-VES-Eni Hewett UK CC Hybrid NOARD 3D\OBP\004_Weekly_Outputs\AMU_templates

The template PowerPoints are:
7021_ENI_Areal_Maps_Seqaaa-bbb_ddmm2023.pptx
7021_ENI_Coff_Cube_Seqaaa-bbb_ddmm2023.pptx
7021_ENI_Fold_Coverage_Seq-nnn_ddmm2023.pptx

## usage

./weekly_plots <sequence>

e.g.

./weekly_plots 37

For whatever reason, the weekly plots are created in folders with names e.g.

Up-to-SEQ037

The sequence supplied to the script must match one of these folders. The plots
are then taken from these folders and copied to the plots_for_powerpoint
folder.

Due to Windows permissions, these must then be copied to the S: directory on the PC.

script location:
/nfs/D01/Reveal_Projects/7021_Eni_Hewett_Stmr/scripts/weekly_plots/weekly_plots.py

renamed plots go to:
/nfs/D01/Reveal_Projects/7021_Eni_Hewett_Stmr/SuperVision/Weekly/plots_for_powerpoint

manually copy the entire directory plots_for_powerpoint to:
S:\Seismic\Jobs\7021-AMU-VES-Eni-Hewett UK CC Hybrid NOAR 3D\OBP\004_Weekly_Outputs

Open a template from the AMU_templates directory and the new plots should replace the old ones.
The S: drive folder must be a trusted folder for PowerPoint on your PC.

The plots are all renamed - the sequence number is replaced with 'xxx'. This
allows the plot names to be linked in the weekly report PowerPoints.

The existing plots in the plots_for_weekly folder are deleted. You need to
explicitly say 'y' to do this. There may be a scenario when you don't want to
delete the previous week's plots from the target folder. I figure it's safer to
have a check before deleting data.

There are three sets of data to copy, one for each of the three PowerPoints we
produce.

The files containing the list of plots names for each of the PowerPoints are:

attribute_plots.md coff_plots.md fold_plots.md

Close and open the relevant template PowerPoint and the latest plots appear.

**Save the template PowerPoint with a new name.**

At some point, you'll forget to do this and overwrite a template. Backups of the
templates are at:

S:\Seismic\Processing\Personal\matt_oppenheim\weekly_powerpoint_templates

## Breaking links to the plots

Break the links to the plots in the SuperVision folder, or when these change, so
will the plots in the PowerPoint. Plus, if you send the PowerPoint off the ship,
none of the plots will display as the PowerPoint will be looking for the plots
on the ship.

To break the links: Go to the 'Files' tab.  On the left hand menu bar, select
the 4th option down 'Info'.  On the right hand side of the screen, almost at the
bottom, there is a tiny option called 'Edit Links to Files', just above the red
text 'Show All Properties'. Click on this.

If you don't see the Edit Links to Files, you need to make the document a trusted document.

For each of the links in the window, click on 'break link'. Now save the file.

Update sequence numbers and dates. Check through as any of the previous week's
annotations may or may not still be visible. Need to test to find out.
