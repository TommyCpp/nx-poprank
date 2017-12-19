from unittest import TestCase

import poprank
from heterogeneousgraph import HeGraph
import networkx as nx
import numpy as np


class TestPopRank(TestCase):
    def _setup(self, sub_graph_count=1):
        G = HeGraph()
        for i in range(sub_graph_count):
            sub_graph = nx.fast_gnp_random_graph(3, 3)
            G.add_graph(sub_graph)
        return G

    def test_pop_rank(self):
        G = HeGraph()
        sub_graph_1 = nx.Graph()
        sub_graph_2 = nx.Graph()
        sub_graph_1.add_edge(1, 3)
        sub_graph_1.add_edge(1, 2)
        sub_graph_2.add_edge(1, 2)
        sub_graph_2.add_edge(2, 3)
        sub_graph_2.add_edge(3, 4)
        G.add_graph(sub_graph_1)
        G.add_graph(sub_graph_2)

    def test_heterogeneous_neighbour_matrix(self):
        G = self._setup(3)
        G.add_heterogeneous_edge(0, 0, 1, 0)
        G.add_heterogeneous_edge(2, 2, 1, 1)
        result = poprank.heterogeneous_neighbour_matrix(G)
        print(result)
        expect = {0: {1: np.array([[1., 0., 0.],
                                   [0., 0., 0.],
                                   [0., 0., 0.]]),
                      2: np.array([[0., 0., 0.],
                                   [0., 0., 0.],
                                   [0., 0., 0.]])},
                  1: {0: np.array([[1., 0., 0.],
                                   [0., 0., 0.],
                                   [0., 0., 0.]]),
                      2: np.array([[0., 0., 0.],
                                   [0., 0., 1.],
                                   [0., 0., 0.]])},
                  2: {0: np.array([[0., 0., 0.],
                                   [0., 0., 0.],
                                   [0., 0., 0.]]),
                      1: np.array([[0., 0., 0.],
                                   [0., 0., 1.],
                                   [0., 0., 0.]])}}
        for i in result.keys():
            for j in result[i].keys():
                np.testing.assert_almost_equal(expect[i][j], result[i][j])
