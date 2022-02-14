class BinaryTree():
    def __init__(self, name = None):
        self.left_child = None
        self.right_child = None
        self.name = name
    def addLeftChild(self, newchild):
        self.left_child = newchild
    def addRightChild(self, newchild):
        self.right_child = newchild
    def getLeaves(self, list):
        if self.left_child != None:
            self.left_child.getLeaves(list)
            self.right_child.getLeaves(list)
        else:
            list.append(self)
    def getLeavesNames(self, list):
        if self.left_child != None:
            self.left_child.getLeavesNames(list)
            self.right_child.getLeavesNames(list)
        else:
            list.append(self.name)

import os, re

'''
Alternative search for domains found in step 3 where the search is based on a binary tree. Necessary domains can be specified, 
and proteins are classified into bins of the possible combinations of these wanted domains. 
'''

# Location of the Files to search. (path to /InterProScan directory specified in step 3)
location_of_files = "<path_to_/InterProScan>"

# Which domains / features must be found to keep the protein? InterPro acc nuber (Examples given)
must_haves_ac = ['IPR005024','IPR036388']

# Which domains / features must be found to keep the protein? human friendly, same order (Examples given)
must_haves_names = ['Snf7 family','Winged helix-like DNA-binding domain superfamily']

# Get all the names of the files to investigate
# only take the .xml files (one of the InterProScan output formats)
all_files = os.listdir(location_of_files)
files_to_investigate = []
for file in all_files:
    if file[-4:] == '.xml':
        files_to_investigate.append(file)

# the search is based on a binary tree
tree = BinaryTree('')
for must_have_name in must_haves_names:
    current_leaves = []
    tree.getLeaves(current_leaves)
    for leave in current_leaves:
        leave.addLeftChild(BinaryTree(leave.name + must_have_name + " MISSING\t"))
        leave.addRightChild(BinaryTree(leave.name + must_have_name + " FOUND\t"))
leaves = []
tree.getLeavesNames(leaves)
encryption = {}
i = 0
while i < 2**len(must_haves_names):
    encryption[i] = leaves[i]
    i += 1

# All Proteins
results = {}

# Filling dict
for file in files_to_investigate:
    name = re.split('name="|"/>',open(location_of_files + '/' + file).read())[1]
    found_domains_acs = [part.split('"')[0] for part in open(location_of_files + '/' + file).read().split('entry ac="')[1:]]
    number = 0
    i = 0
    for must_have in must_haves_ac[::-1]:
        n = 2**i
        if must_have in found_domains_acs:
            number = number + n
        i = i + 1
    results[name] = number

# print bins (for example: bin1: ['IPR005024','IPR036388'], bin2: ['IPR005024'], bin3: ['IPR036388'], bin4: []
for possibility in encryption.items():
    print('\n\n' + possibility[1] + '\n')
    for result in results.items():
        if result[1] == possibility[0]:
            print(result[0])




