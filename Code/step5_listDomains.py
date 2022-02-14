import os

'''
create a list of proteins finally selected in the following format: 
#<protein1_acc_number> 
<protein1_domain1_name>,<domain_starting_position>,<domain_end_position>
<protein1_domain2_name>,<domain_starting_position>,<domain_end_position>
...
#<protein2_acc_number> 
...

for example: 
#Q9HJ01
AAA ATPase; AAA+ lid domain,303,350
P-loop containing nucleoside triphosphate hydrolase,107,372
AAA+ ATPase domain,145,283
...
#S0ATL8
ATPase; AAA-type; conserved site,240,258
...

This output was used to subsequently generate Suppl. Table 1 

'''

# path to a file whicih maps protein ID to Organism in txt format with \t between Protein ID and Organism ID, entries separated by \n.
# Can be generated with table 2.
path_to_map = "<path_to/Map_ID_to_Organism.txt>"

# read in the results of InterProScan (may be reduced by step 3) (.tsv)
# stored in a dict: {UniProtID : list of results}
filepath_all = "<path_to/InterProScan/"
filenames = os.listdir(filepath_all)
tsv_filenames = []
for filename in filenames:
    if ".tsv" in filename:
        tsv_filenames.append(filename)
results = {}
for filename in tsv_filenames:
    file = open(filepath_all + filename).read().strip()
    if file == "":
        continue
    protein_name = file.split("|")[1]
    result = [line.replace(',',';').split("\t")[4:] for line in file.split("\n")]
    nice_result = []
    for domain in result:
        counters = [0,2,3]
        if domain[0] == "Coil":
            counters = [0,2,3]
        elif domain[-2][:3] == "IPR":
            counters = [-1,2,3]
        elif domain[1] == "consensus disorder prediction":
            counters = [1,2,3]
        nice_result.append([domain[i] for i in counters])
    results[protein_name] = nice_result

# print results in .csv format
#output = ""
#for protein_name, result in results.items():
#    output += protein_name
#    for domain in result:
#        output += "\n" + ",".join(domain)
#    output += "\n"
#print(output)

# print result in format indicated in description above
output = ""
protein_to_organism = [line.split("\t") for line in open(path_to_map).read().strip().split("\n")]
for protein in protein_to_organism:
    for protein_name, result in results.items():
        if protein_name != protein[0]:
            continue
        output += '#' + protein_name
        for domain in result:
            output += "\n" + ",".join(domain)
        output += "\n"
print(output)