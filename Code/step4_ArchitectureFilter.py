import os, re

'''
This script searches for domains found in step 3. Necessary domains can be specified, 
and proteins are classified into bins of the possible combinations of these wanted domains. 
'''

# Location of the Files to search.
location_of_files = "<path_to_directory>"

# Which domains / features must be found to keep the protein? InterPro ac
must_haves_ac = ['IPR005024','IPR036388']

# Which domains / features must be found to keep the protein? human friendly
must_haves_names = ['Snf7 family','Winged helix-like DNA-binding domain superfamily']

# Get all the names of the files to investigate
# only take the .xml files
all_files = os.listdir(location_of_files)
files_to_investigate = []
for file in all_files:
    if file[-4:] == '.xml':
        files_to_investigate.append(file)

# List of proteins including all must_haves
good_proteins = []

# List of proteins including none of the must_haves
bad_proteins = []

# Lists including some of the must_haves

# Filling list
for file in files_to_investigate:
    name = re.split('name="|"/>',open(location_of_files + '/' + file).read())[1]
    found_domains_acs = [part.split('"')[0] for part in open(location_of_files + '/' + file).read().split('entry ac="')[1:]]
    good = True
    for must_have_ac in must_haves_ac:
        if must_have_ac not in found_domains_acs:
            good = False
    if good:
        good_proteins.append(name)
    else:
        bad_proteins.append(name)

print("GOOD PROTEINS")
for good_protein in good_proteins:
    print(good_protein)
print("\nBAD PROTEINS")
for bad_protein in bad_proteins:
    print(bad_protein)