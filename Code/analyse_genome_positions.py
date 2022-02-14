import re

'''
Script searching for positions of wanted genes in a genome. 
'''

# a function to get the complement of a sequence
def make_complement(seq):
    return seq.replace("A", "t").replace("T", "a").replace("C", "g").replace("G", "c").upper()

# path to a csv file containing protien name, gene id and genome id (suppl. table 2)
table_path = "<path_to/suppl_table_2.csv"


# the data file that has protein name, gene id and genome id.
data = [line.strip().split(',') for line in open(table_path).read().strip().split('\n')]

# the result
output = ''

# a dict of genomes
# key: fasta head, value: sequence
path_genomes = "<path_to/genomes.fna>"
genomes_list = [">" + entry for entry in open(path_genomes).read().strip().split(">")[1:]]
genomes = {}
for genome in genomes_list:
    genome = genome.split("\n")
    genomes[genome[0]] = "".join(genome[1:])

# a dict of all genes
# key: fasta head, value: sequence
path_genes = "<path_to/CdvABC_allgenes.fna>"
genes_list = [entry.split("\n") for entry in open(path_genes).read().strip().split(">")[1:]]
genes = {}
for gene in genes_list:
    genes[">" + gene[0]] = "".join(gene[1:])

# if a gene and a genome is existent, analyse and store result
for line in data:
    gene_ID = line[4]
    genome_ID = line[18]

    # if a gene ID and a genome ID exist analyse
    if line[0] == '' and not '&' in genome_ID and gene_ID != '' and genome_ID != '':

        # tell me where we are for debug
        if gene_ID != '':
            print('Investigating gene', gene_ID)

        cur_gene = ''
        cur_genome = ''

        # search the current gene and get the sequence
        for head in genes.keys():
            if gene_ID in head:
                cur_gene = genes[head]
                print('Found gene seq.')
                break

        # search the current genome and get the sequence
        for head in genomes.keys():
            if genome_ID in head:
                cur_genome = genomes[head]
                break

        # check if both seqs were found.
        if cur_genome == '':
            print('Genome seq not found. SKIPPING.')
        elif cur_gene == '':
            print('Gene seq not found. SKIPPING.')
        # analyse position and orientation
        else:

            line[22] = str(len(cur_genome))
            line[15] = str(len(cur_gene))

            # normal, normal
            search1 = re.search(cur_gene, cur_genome)
            if search1:
                start = str(search1.start() + 1)
                end = str(search1.end())
                orientation = 'normal'

                # place information in current line
                line[19] = start
                line[20] = end
                line[21] = orientation

                # give feedback
                print('Found gene on genome in',orientation,'orientation at', start, 'to', end)

            # normal, complement
            search2 = re.search(make_complement(cur_gene), cur_genome)
            if search2:
                start = str(search2.start() + 1)
                end = str(search2.end())
                orientation = 'complement'

                # place information in current line
                line[19] = start
                line[20] = end
                line[21] = orientation

                # give feedback
                print('Found gene on genome in',orientation,'orientation at', start, 'to', end)

            # reverse, normal
            search3 = re.search(cur_gene[::-1], cur_genome)
            if search3:
                start = str(search3.start() + 1)
                end = str(search3.end())
                orientation = 'reverse'

                # place information in current line
                line[19] = start
                line[20] = end
                line[21] = orientation

                # give feedback
                print('Found gene on genome in',orientation,'orientation at', start, 'to', end)

            # reverse, complement
            search4 = re.search(make_complement(cur_gene)[::-1], cur_genome)
            if search4:
                start = str(search4.start() + 1)
                end = str(search4.end())
                orientation = 'reverse complement'

                # place information in current line
                line[19] = start
                line[20] = end
                line[21] = orientation

                # give feedback
                print('Found gene on genome in',orientation,'orientation at', start, 'to', end)

            if not (search1 or search2 or search3 or search4):
                print('Gene not found in genome')

    # append the line to the output after everything is done
    output += ",".join(line) + '\n'

# Save output
open(table_path,"w").write(output)
print('All done. ')