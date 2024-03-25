This repository contains example files from my thesis.<br><br>
<b>GeneralDeletionAnalyzer.ipynb:</b>
<p>
	This tool is used to analyze the deletions in any number of datasets.
	The highest frequency deletions, highest frequency deletion lengths using three
	metrics, and highest frequency frameshift deletions are found. Histograms for the
	deletion lengths using the three frequency metrics are generated. This is the Jupyter Notebook version.</p><br>

 <b>SubunitAnalyzer.ipynb:</b>
 <p>See the description of general_subunit_analyzer.py for the newer version. The ipynb file was used during the thesis work.</p><br>

 <b>general_deletion_analyzer.py</b>
 <p>	This tool is used to analyze the deletions in any number of datasets.
	The highest frequency deletions, highest frequency deletion lengths using three
	metrics, and highest frequency frameshift deletions are found. Histograms for the
	deletion lengths using the three frequency metrics are generated. This is the Python file version.</p><br>
 
 <b>general_subunit_analyzer.py:</b>
<p> This tool can be used for any number of datasets and a set of user defined S-gene subunits/regions.
    General summaries denoting the percentages for subtitutions and/or deletions in the entire S-gene and
	the average numbers of each mutation type are produced for both datasets.
	General mutation frequency plots are then generated.
	Plots showing which positions in each subunit have mutated or have a high frequency are produced for the following subunits:<br>
	        NTD<br>
		RBD<br>
		S1<br>
		S2<br>
		FP<br>
		S2'<br>
		Cleavage Site at 815 to 816<br>
		IFP<br>
		HR1<br>
		HR2<br>
		TM<br>
		CT<br>
	Lists of positions that have not had at least one substitution and/or deletion are listed where applicable.
	The high frequency mutation positions and general summaries for each subunit are also printed.
	It also lists the high frequency (>= 0.1) mutation positions in each dataset.</p><br>
