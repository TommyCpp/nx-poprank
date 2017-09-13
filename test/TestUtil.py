import unittest

import networkx as nx

from heterogeneousgraph.util import *


class TestUtil(unittest.TestCase):
    def test_filter_heterogeneous_links(self):
        heterogeneous_links = [(0, 0, 1, 0), (1, 1, 0, 1), (1, 2, 4, 5)]
        result = filter_heterogeneous_links(0, 1, heterogeneous_links)
        print(result)
        self.assertEqual(2, len(result))

    def test_adjlist_of_heterogeneous_graph(self):
        graph_1 = nx.fast_gnp_random_graph(3, 3)
        graph_2 = nx.fast_gnp_random_graph(3, 3)
        heterogeneous_links = [(0, 0, 1, 0), (0, 1, 1, 1), (0, 2, 1, 0)]
        result = adjlist_of_heterogeneous_graph(graph_1, graph_2, heterogeneous_links)
        print(result)

    def test_sort_heterogeneous_link(self):
        heterogeneous_link = (1, 1, 0, 0)
        self.assertEqual((0, 0, 1, 1), sort_heterogeneous_link(*heterogeneous_link))
# todo: assert exception