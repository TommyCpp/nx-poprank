from unittest import TestCase

from heterogeneousgraph import HeGraph
import networkx as nx


class GraphTestCase(TestCase):
    def _setup(self, sub_graph_count=1, node_per_graph=3, probability_of_edge_creation=0.8):
        G = HeGraph()
        for i in range(sub_graph_count):
            sub_graph = nx.fast_gnp_random_graph(node_per_graph, probability_of_edge_creation)
            G.add_graph(sub_graph)
        return G
