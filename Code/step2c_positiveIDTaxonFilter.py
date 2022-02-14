import re

'''
Alternative filtering where only proteins from organisms with specific ID are allowed. 
'''

# path to Suppl. Table 2 in .csv format
path_data = "<path>"

# a list of the wanted taxon IDs
wanted_taxIDs = [line.split(',')[2] for line in open(path_data).read().strip().split('\n')[1:]]
for i in range(len(wanted_taxIDs)-1,-1,-1):
    if wanted_taxIDs[i] == '':
        wanted_taxIDs.pop(i)

# a list of all the FtsZs we alreardy have
existing_FtsZ_IDs = [line.split(',')[3:5] for line in open('/media/zebrafish/Speicher/BF/Documents/Uni/MPI/Pretty/Data_ordered.csv').read().strip().split('\n')[1:]]
for i in range(len(existing_FtsZ_IDs)-1,-1,-1):
    if existing_FtsZ_IDs[i][0] == '' or not (existing_FtsZ_IDs[i][0] == 'FtsZ' or existing_FtsZ_IDs[i][0] == 'CetZ'):
        existing_FtsZ_IDs.pop(i)
existing_FtsZ_IDs = [entry[1] for entry in existing_FtsZ_IDs]

# The directory where the input file is and the output should be stored.
curdir = "/media/zebrafish/Speicher/BF/Documents/Uni/MPI/Data/OutputFiles/FtsZ3"

# Put all sequences found by PSIBlast in a list
all = open(curdir+"/FtsZ3_Search_tmp.preselected_seq.txt").read().strip().split(">")[1:]

# Create a list to store the good entries only
filtered = []

# Give information to user what is happening
print("STARTING TAXON-FILTERING")
print("Searching for following taxon IDs:")
for taxID in wanted_taxIDs:
    print("\t'"+taxID+"'")

# Filter the sequences
print("RUNNING")
for entry in all:
    cur_taxID = re.split("OX=| GN=",entry)[1]
    cur_protID = re.split('TR:|tr[|]| |SP\:|_]',entry.split('\n')[0])[1].split('|')[0]
    if (re.search("|".join(wanted_taxIDs),cur_taxID)) and not cur_protID in existing_FtsZ_IDs:
        filtered.append(entry)
print("FINISHED")

# Give information to user what was done and save result
print("Initial file had", len(all), "entries, filtered file has",len(filtered))
print("Creating new file: FtsZ3_Search_tmp_filtered.fasta")
out = open(curdir+"/FtsZ3_Search_tmp_filtered_new.fasta","w")
for entry in filtered:
    out.write(">"+entry)
out.close()

