'''
Script drawing Suppl. Figure 2
'''

## CLASSES ##

# An organism's genome
class Genome:
    def __init__(self, organism=None, length = 0):
        # name of organism the genome belongs to
        self.organism = organism
        # total length of genome
        self.length = length
        # list of genes on genome
        self.genes = []

# A gene encoding one of the Cdv proteins.
class Gene:
    def __init__(self, name=None, start=None, end=None, direction=True):
        # name of the gene such as CdvB, CdvB1, CdvC, CdvBt...
        self.name = name
        # position of first nucleotide (REAL position, not python!)
        self.start = start
        # position of last nucleotide (REAL position, not python!)
        self.end = end
        # direction of gene: True = forward, False = reverse complement
        self.direction = direction

## FUNCTIONS ##

# returning a list of genes ordered by their start position
def order_genes_by_start(genes):
    ordered = []
    for gene in genes:
        i = 0
        if ordered != []:
            for ordered_gene in ordered:
                if ordered_gene.start < gene.start:
                    i = i+1
                    continue
        ordered.insert(i,gene)
    return ordered

## USER SPECIFICATIONS ##

# Tell me which organisms to show. Expected format: \n separated list, empty entry gives distance
organisms_to_show_path = 'S:/BF/Documents/Uni/MPI/Pretty/Nucl_Seqs/organisms_to_show.txt'

# colors to specify gene
color_legend = {
    'CdvA':'#c12200',
    'CdvB':'#007b0a',
    'CdvB1':'#8bff4d',
    'CdvB2':'#30d892',
    'CdvB12': '#8bff4d',
    'CdvB3':'#28d243',
    'CdvBt':'#caaa42',
    'CdvBa1':'#ff4949', # change
    'CdvBa2':'#ff4949', # change
    'CdvBe':'blue', # change
    'CdvC':'darkviolet',
}

excluded_protein_names = ['FtsZ', 'CetZ', 'FtsZalt']

# Tell me where the table with all the infos is - Suppl. Table 2
data_path = '<path_to/Suppl_table_2>'

# specifications of drawing
leading_line_length = 20
last_line_length = 80
cutoff_line_length = 80

## READING DATA ##

# Read in data
data = [line.split(",") for line in open(data_path).read().strip().split('\n')]

# Make genomes to show
organisms_to_show = open(organisms_to_show_path).read().strip().split('\n')
cur_organism = ''
# {organism name: [Genome1 ID, Genome2 ID, ...]}
organisms = {}
# {genome ID: Genome}
genomes = {}
for line in data:
    # first line
    if line[0] == 'Organism':
        continue
    # a new organism is found and created
    elif line[0] != '':
        cur_organism = line[0]
        if cur_organism in organisms_to_show:
            organisms[cur_organism] = []
        else:
            print('Not showing', cur_organism)
    # fill the organism
    else:
        if cur_organism in organisms_to_show and not line[3] in excluded_protein_names and not 'not included' in line[3]:
            genome_ID = line[18]
            # if genome doesn't yet exist create new
            if not genome_ID in genomes.keys():
                genomes[genome_ID] = Genome(organism = cur_organism, length=int(line[22]))
                organisms[cur_organism].append(genome_ID)
            # add current gene
            print(line[3])
            genomes[genome_ID].genes.append(Gene(name=line[3], start=int(line[19]), end=int(line[20]), direction=('normal'==line[19])))

## DRAWING ##

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Create figure and axes
fig,ax = plt.subplots(1)

# get total length to define pic size (some organisms have multiple genomes)
total_length = 0
for organism in organisms.values():
    for genome in organism:
        total_length += 1

# Define size of figure
fig.set_size_inches(15,(total_length+1)*0.4)

# define x-axis length
ax.set_xlim(0,1200)
ax.set_ylim(0,2500)

# Label y-axis with organisms
y_labels = open(organisms_to_show_path).read().strip().split('\n')[::-1]
yticks_range = [0]
for label in y_labels:
    if label == "":
        yticks_range.append(yticks_range[-1] + 25)
    else:
        yticks_range.append(yticks_range[-1] + (len(organisms[label])) * 50)
yticks_range.pop(0)
plt.yticks(yticks_range, y_labels)

# Remove frame, ticks and x-axis
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.get_xaxis().set_ticks([])
ax.tick_params(width=0)

plt.tight_layout()

# Draw Genes
i=0
for organism in y_labels:

    if organism == "":
        i = i + 0.5
        continue
    else:

        for genome in organisms[organism]:

            i = i + 1

            # draw leading line
            line = patches.Rectangle((50, i * 50), leading_line_length, 0, linewidth=1, edgecolor='black')
            ax.add_patch(line)

            genes_to_draw = genomes[genome].genes

            # order genes
            ordered_genes_to_draw = order_genes_by_start(genes_to_draw)

            # distances between genes
            distances = []

            for n in range(len(ordered_genes_to_draw)-1):
                distances.append((ordered_genes_to_draw[n+1].start - ordered_genes_to_draw[n].end)/10)

            # add last line
            distances.append(last_line_length)

            x_position = 50 + leading_line_length
            n=0
            for cur_gene in ordered_genes_to_draw:
                color = color_legend[cur_gene.name]


                arrow_length = (cur_gene.end - cur_gene.start)/10
                if not cur_gene.direction:
                    x_position = x_position + arrow_length
                    arrow_length = arrow_length * -1
                    arrow = patches.FancyArrow(x_position, i*50, arrow_length, 0, 20, True, head_width=20, head_length=20, color=color)
                    ax.add_patch(arrow)
                    x_position = x_position + arrow_length
                else:
                    arrow = patches.FancyArrow(x_position, i*50, arrow_length, 0, 20, True, head_width=20, head_length=20, color=color)
                    ax.add_patch(arrow)

                if not distances[n] < 500:
                    line = patches.Rectangle((x_position + (cur_gene.end - cur_gene.start) / 10, i * 50), cutoff_line_length, 0,
                                             linewidth=1, edgecolor='black')
                    ax.add_patch(line)
                    x_position = x_position + cutoff_line_length + (cur_gene.end - cur_gene.start) / 10

                    interrupt1 = patches.FancyArrow(x_position - (cutoff_line_length/2 +15), i * 50 - 10, 20, 20, True, head_width=0, linewidth=1,
                                                    edgecolor='black')
                    interrupt2 = patches.FancyArrow(x_position - (cutoff_line_length/2 +10), i * 50 - 10, 20, 20, True, head_width=0, linewidth=4,
                                                    edgecolor='white')
                    interrupt3 = patches.FancyArrow(x_position - (cutoff_line_length/2 +5), i * 50 - 10, 20, 20, True, head_width=0, linewidth=1,
                                                    edgecolor='black')
                    ax.text(x_position - (cutoff_line_length/2 -10),i * 50 + 20, str(round(distances[n]/100,0))[:-2] + "kb", ha="center", va="center", color="black")
                    ax.add_patch(interrupt2)
                    ax.add_patch(interrupt1)
                    ax.add_patch(interrupt3)

                else:
                    line = patches.Rectangle((x_position + (cur_gene.end - cur_gene.start) / 10, i * 50), distances[n], 0,
                                             linewidth=1, edgecolor='black')
                    ax.add_patch(line)
                    x_position = x_position + distances[n] + (cur_gene.end - cur_gene.start)/10

                n = n+1

            # add information about hof much is left of the genome
            interrupt1 = patches.FancyArrow(x_position - (last_line_length/2 + 15), i * 50 - 10, 20, 20, True, head_width=0, linewidth=1,
                                            edgecolor='black')
            interrupt2 = patches.FancyArrow(x_position - (last_line_length/2 + 10), i * 50 - 10, 20, 20, True, head_width=0, linewidth=4,
                                            edgecolor='white')
            interrupt3 = patches.FancyArrow(x_position - (last_line_length/2 + 5), i * 50 - 10, 20, 20, True, head_width=0, linewidth=1,
                                            edgecolor='black')
            ax.text(x_position - (last_line_length/2 - 10), i * 50 + 20, str(round((genomes[genome].length / 10 - (sum(distances) - last_line_length )) / 100, 0))[:-2] + "kb", ha="center", va="center",
                    color="black")
            ax.add_patch(interrupt2)
            ax.add_patch(interrupt1)
            ax.add_patch(interrupt3)

# make scale bar
bar = patches.Rectangle((50, 15), 100, 0, linewidth=2, edgecolor='black')
ax.add_patch(bar)
ax.text(100, -2, "1kb", ha="center", va="center", color="black")

# show
plt.show()










