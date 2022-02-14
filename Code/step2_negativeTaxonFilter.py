import re

'''
This script filters the result of step 1 for taxa that should not be included, for example because they are fragmentary, 
originate from uncultured organisms etc. 
'''


# The directory where the input file is and the output should be stored.
curdir = "<path_to_file>"

# name to give to output file
outname = "<name>"

# Put all sequences found by PSIBlast in a list
all = open(curdir+"<path_to_PsiBlast_output.txt>").read().strip().split(">")[1:]

# Create a list to store the good entries only
filtered = []

# Define patterns that indicate an unknown (=bad=excluded) taxon. proteins whose organism names include these words will be excluded from the list. List filled with examples.
bad_taxa = ["unknown", " sp\.", "Archaea", "Archaeon", "archaeon", "metagenome", "cellular organisms", "unclassified", " group", "uncultured"]

# Give information to user what is happening
print("STARTING TAXON-FILTERING")
print("Criteria for exclusion:")
print("\tOne word only or including following regular expressions in taxon:")
for bad_taxon in bad_taxa:
    print("\t'"+bad_taxon+"'")

# Filter the sequences
print("RUNNING")
for entry in all:
    taxon = re.split("Tax=| TaxID=|OS=| OX=",entry)[1]
    if (not re.search("|".join(bad_taxa),taxon)) and (re.search(" ",taxon)): # criterion: bad pattern included or only one word
        filtered.append(entry)
print("FINISHED")

# Give information to user what was done and save result
print("Initial file had", len(all), "entries, filtered file has",len(filtered))
print("Creating new file: CdvSearch_tmp_filtered.fasta")
out = open(curdir+"/"+ outname +"_filtered.fasta","w")
for entry in filtered:
    out.write(">"+entry)
out.close()

