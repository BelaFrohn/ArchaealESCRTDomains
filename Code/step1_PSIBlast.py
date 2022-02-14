import os, time

'''
This script uses PsiBlast to search for homologs of a wanted protein. 
It was used with different input sequences to search for homologs of Cdv proteins in archaea.
We also used the Browser version of PsiBlast
'''

# E-mail address to allow contact
email = "bfrohn@biochem.mpg.de"

# The query sequence file path (fasta)
query_sequence = "<path_to_fasta_file>"

# The database to run search against
# https://www.ebi.ac.uk/seqdb/confluence/display/JDSAT/PSI-BLAST+protein+databases
database = "uniprotkb_archaea"

# Comparison matrix to be used
matrix = "BLOSUM45"

# Gap penalty values. Default: gap_open = 15, gap_extension = 2
gap_open = 15
gap_extension = 2

# The directory where the outputfiles should be stored.
outdir = "<path_to_directory>"

# Check if outpitdirectory exists
if not os.path.isdir(outdir):
    print("Output directory does not exist!\nExit. ")
    exit()

# The number of PSIBlast Results wanted
num_results = 5000

# Store initial workingdirectory to be able to go there again.
firstdir = os.getcwd()

# Change to outputdirectory to save temporary PSIBlast files there.
os.chdir(outdir)

# Give information to user about what is happening
print("STARTING PSIBLAST SEARCH")
print("Parameters:")
print("\tE-mail:",email)
print("\tdatabase:",database)
print("\tnew gap penalty:",gap_open)
print("\textending gap penalty:",gap_extension)
print("\tmaximum number of results:",num_results)

# Run PSIBlast
start_time = time.time()
os.system("python3 /media/zebrafish/Speicher/BF/Documents/Uni/MPI/Software/PSIBlast-client.py --matrix " + matrix +
          " --gapopen " + str(gap_open) +
          " --gapext " + str(gap_extension) +
          " --scores "+ str(num_results) +
          " --alignment "+ str(num_results) +
          " --email " + email +
          " --database " + database +
          " --filter no --outformat preselected_seq,ids,out --outfile FtsZ3_Search_tmp " + query_sequence)
duration = time.time() - start_time

# result information
print("\nPSIBlast took" , str(int(round(duration/60,0)))+ "m", str(int(round(duration%60,0))) +"s to run.")

# Change to initial workingdirectory.
os.chdir(firstdir)