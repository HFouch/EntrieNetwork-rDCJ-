import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class GraphTheory:

    def __init__(self, network):
        self.network = network


    def plot_network(self, start_node):
        hier_pos = GraphTheory.hierarchy_pos(self, self.network, start_node)
        nx.draw(self.network, pos=hier_pos, with_labels=False)
        plt.savefig('hierarchical_network_plot.png')
        plt.close()

    def metrics_on_degree_sequence(self):
        # number of nodes
        n = len(self.network.nodes())

        # isolate the sequence of degrees
        degree_sequence = list(self.network.degree())

        # comput number of edges and the metrics on the degree sequence
        nb_nodes = n
        nb_arr = len(self.network.edges())

        avg_degree = np.mean(np.array(degree_sequence)[:, 1])
        med_degree = np.median(np.array(degree_sequence)[:, 1])

        max_degree = max(np.array(degree_sequence)[:, 1])
        min_degree = np.min(np.array(degree_sequence)[:, 1])

        print("Number of nodes : " + str(nb_nodes))
        print("Number of edges : " + str(nb_arr))
        print("Maximum degree : " + str(max_degree))
        print("Minimum degree : " + str(min_degree))
        print("Average degree : " + str(avg_degree))
        print("Median degree : " + str(med_degree))

        print()
        print('This is a weakly connected network: ', nx.is_weakly_connected(self.network))
        print('This is a strongly connected network: ', nx.is_strongly_connected(self.network))
        print()


    def centrality_algorithms(self):
        # PageRank
        pagerank = nx.pagerank(self.network, alpha=0.9)
        pagerank = list(pagerank.values())

        # Degree centrality --> measure incoming and outgoining relationshipnetwork = Network.build_network(self)
        c_degree = nx.degree_centrality(self.network)
        c_degree = list(c_degree.values())

        # Closeness centrality --> node that can spread info efficiently through graph
        c_closeness = nx.closeness_centrality(self.network)
        c_closeness = list(c_closeness.values())

        # Betweenness Centrality --> amount of influence a node has over the flow of info
        # --> can be used to find nodes that serve as a bridge from one part of a graph to another
        c_betweenness = nx.betweenness_centrality(self.network)
        c_betweenness = list(c_betweenness.values())

        return pagerank, c_degree, c_closeness, c_betweenness

    def plot_centrality_measures(self, start_node, pagerank, c_degree, c_closeness, c_betweenness):



        plt.figure(figsize=(18, 12))
        hier_pos = GraphTheory.hierarchy_pos(self, self.network, start_node)



        #PageRank
        f, axarr = plt.subplots(2, 2, num=1)
        plt.sca(axarr[0, 0])
        nx.draw(self.network, cmap=plt.get_cmap('inferno'), node_color=pagerank, node_size=300, pos=hier_pos, with_labels=False)
        axarr[0, 0].set_title('PageRank', size=16)

        # Degree Centrality
        plt.sca(axarr[1, 0])
        nx.draw(self.network, cmap=plt.get_cmap('inferno'), node_color=c_degree, node_size=300, pos=hier_pos, with_labels=False)
        axarr[1, 0].set_title('Degree Centrality', size=16)

        # Proximity Centrality
        plt.sca(axarr[1, 1])
        nx.draw(self.network, cmap=plt.get_cmap('inferno'), node_color=c_closeness, node_size=300, pos=hier_pos, with_labels=False)
        axarr[1, 1].set_title('Proximity Centrality', size=16)

        # Betweenness Centrality
        plt.sca(axarr[0, 1])
        nx.draw(self.network, cmap=plt.get_cmap('inferno'), node_color=c_betweenness, node_size=300, pos=hier_pos, with_labels=False)
        axarr[0, 1].set_title('Betweenness Centrality', size=16)

        plt.savefig('centrality_measures_plot.png')
        plt.close()

    def hierarchy_pos(self, network, root, levels=None, width=1., height=1.):
        # https://stackoverflow.com/questions/29586520/can-one-get-hierarchical-graphs-from-networkx-with-python-3/29597209
        '''If there is a cycle that is reachable from root, then this will see infinite recursion.
           G: the graph
           root: the root node
           levels: a dictionary
                   key: level number (starting from 0)
                   value: number of nodes in this level
           width: horizontal space allocated for drawing
           height: vertical space allocated for drawing'''
        TOTAL = "total"
        CURRENT = "current"

        def make_levels(levels, node=root, currentLevel=0, parent=None):
            """Compute the number of nodes for each level
            """
            if not currentLevel in levels:
                levels[currentLevel] = {TOTAL: 0, CURRENT: 0}
            levels[currentLevel][TOTAL] += 1

            neighbors = network.neighbors(node)
            for neighbor in neighbors:
                if not neighbor == parent:
                    levels = make_levels(levels, neighbor, currentLevel + 1, node)
            return levels

        def make_pos(pos, node=root, currentLevel=0, parent=None, vert_loc=0):
            dx = 1 / levels[currentLevel][TOTAL]
            left = dx / 2
            pos[node] = ((left + dx * levels[currentLevel][CURRENT]) * width, vert_loc)
            levels[currentLevel][CURRENT] += 1

            neighbors = network.neighbors(node)
            for neighbor in neighbors:
                if not neighbor == parent:
                    pos = make_pos(pos, neighbor, currentLevel + 1, node, vert_loc - vert_gap)
                    ##print('pos, currentlevel, vert_loc, vert_gap')
                    ##print(pos, '    ',currentLevel, '      ', vert_loc, '     ', vert_gap )
                    ##print()
            return pos

        if levels is None:
            levels = make_levels({})
        else:
            levels = {l: {TOTAL: levels[l], CURRENT: 0} for l in levels}
        vert_gap = height / (max([l for l in levels]) + 1)
        return make_pos({})
