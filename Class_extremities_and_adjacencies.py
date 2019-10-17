class Extremities_and_adjacencies:

    def __init__(self):

        pass

    def gene_extremities(self, genome):
        genome_gene_ext = []
        for chromosome in genome:
            chromosome_gene_ext = []
            for marker in chromosome:
                if int(marker) >= 0:

                    chromosome_gene_ext.append(marker)
                    chromosome_gene_ext.append(marker + 0.5)
                else:
                    marker_str = str(abs(marker))
                    chromosome_gene_ext.append(abs(marker) + 0.5)
                    chromosome_gene_ext.append(abs(marker))
            genome_gene_ext.append(chromosome_gene_ext)

        return genome_gene_ext

    def create_adjacency_list(self, genome):
        adjacencies = []
        gene_extremities = Extremities_and_adjacencies.gene_extremities(self, genome)
        for chromosome in gene_extremities:
            i = 0
            while i < len(chromosome):
                if chromosome[i] == chromosome[0] or chromosome[i] == chromosome[-1]:
                    adjacencies.append((chromosome[i]))
                    i += 1
                else:
                    adjacencies.append((chromosome[i], chromosome[i + 1]))
                    i += 2
        return adjacencies

    def adjacencies_ordered_and_sorted(self, genome):
        adjacencies = Extremities_and_adjacencies.create_adjacency_list(self, genome)
        ordered = []
        for element in adjacencies:
            if type(element) is tuple:
                if int(element[0]) < int(element[1]):
                    ordered.append(element)
                else:
                    ordered.append((element[1], element[0]))
            else:
                ordered.append(element)
        sorted_adjacencies = []
        tuples = []
        not_tuples = []
        for element in ordered:
            if type(element) is tuple:
                tuples.append(element)
            else:
                not_tuples.append(element)
        for element in sorted(not_tuples):
            sorted_adjacencies.append(element)
        for element in sorted(tuples):
            sorted_adjacencies.append(element)

        return sorted_adjacencies