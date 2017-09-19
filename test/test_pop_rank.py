from unittest import TestCase

from heterogeneousgraph import HeGraph
import networkx as nx


class TestPopRank(TestCase):
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

