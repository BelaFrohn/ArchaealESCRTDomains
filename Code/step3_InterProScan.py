import os, time

'''
Running the filtered list of homologs against the InterPro database. 
InterProScan needs to be installed on the machine. 
Scans against NCBI CDD were executed via the browser application. 
'''

# path to interproscan on the machine
path_to_interproscan = "<path_to_interproscan.sh>"

# path to result of step 2
input_path = "<path>"

# The directory where the outputfiles should be stored.
outdir = "<path_to_directory>"

# Put all sequences to investigate in a list
sequences_to_investigate = [">"+entry.strip() for entry in open(input_path).read().strip().split(">")[1:] ]

# Make directory for InterProScan files
os.mkdir(outdir + "/InterProScan")
outdir = outdir + "/InterProScan"

# Run InterProScan for every sequence
total_scans = len(sequences_to_investigate)
print("STARTING InterProScan FOR ALL", total_scans, "FILES.")
tmp_name = outdir+"/CdvInterProScanInput_tmp.fasta"
silent = outdir+"/silent.txt"
open(silent,"w").write("output of InterProScan\n")
i=1
for sequence in sequences_to_investigate:
    print("Scanning file", i, "/", total_scans)
    start_time = time.time()
    tmp_file = open(tmp_name,"w").write(sequence)
    os.system(path_to_interproscan +
              " -d " + outdir +
              " -i " + tmp_name + " > " + silent)
    duration = time.time() - start_time
    print("Scan took" , str(int(round(duration/60,0)))+ "m", str(int(round(duration%60,0))) +"s to run.")
    i+=1
os.remove(outdir+"/CdvInterProScanInput_tmp.fasta")
os.remove(silent)
print("FINISHED")