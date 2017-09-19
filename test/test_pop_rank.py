from unittest import TestCase

from heterogeneousgraph import HeGraph
import networkx as nx

from poprank import heterogeneous_neighbour_matrix


class TestPopRank(TestCase):
    def _setup(self):
        G = HeGraph()
        sub_graph_1 = nx.fast_gnp_random_graph(4, 4)
        sub_graph_2 = nx.fast_gnp_random_graph(4, 5)
        G.add_graph(sub_graph_1)
        G.add_graph(sub_graph_2)
        G.add_heterogeneous_edge(0, 0, 1, 1)
        G.add_heterogeneous_edge(0, 1, 1, 2)
        G.add_heterogeneous_edge(0, 2, 1, 3)
        return G

    def test_pop_rank(self):
        pass

    def test_heterogeneous_neighbour_matrix(self):
        G = self._setup()
        matrix = heterogeneous_neighbour_matrix(G)
        print(matrix)
