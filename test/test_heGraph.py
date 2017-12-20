import networkx as nx

from heterogeneousgraph import HeGraph
from test.GraphTestCase import GraphTestCase


class TestHeGraph(GraphTestCase):
    def _setup(self, sub_graph_count=1, **kwargs):
        return super()._setup(sub_graph_count=1, node_per_graph=3, probability_of_edge_creation=1)

    def test_add_graph(self):
        G = HeGraph()
        sub_graph = nx.Graph()
        G.add_graph(sub_graph)
        self.assertEqual(1, len(G.sub_graphs))

    def test_add_node_to_sub_graph(self):
        G = HeGraph()
        sub_graph = nx.fast_gnp_random_graph(3, 3)
        G.add_graph(sub_graph)
        G.add_node_to_sub_graph(0, 4)
        self.assertEqual(4, len(sub_graph.nodes()))

    def test_add_nodes_to_sub_graph(self):
        G = self._setup()
        G.add_nodes_to_sub_graph(0, [4, 5, 6])
        self.assertEqual(6, len(G.sub_graphs[0].nodes()))

    def test_remove_node_from_sub_graph(self):
        G = self._setup(3, )
        G.add_heterogeneous_edge(0, 0, 1, 0)
        G.add_heterogeneous_edge(2, 2, 1, 1)
        G.remove_node_from_sub_graph(0, 0)
        print(G.heterogeneous_links)
        self.assertEqual([(1, 1, 2, 2)], G.heterogeneous_links)

    def test_remove_nodes_from_sub_graph(self):
        G = self._setup(3, )
        G.add_heterogeneous_edge(0, 0, 1, 0)
        G.add_heterogeneous_edge(2, 2, 1, 1)
        G.add_heterogeneous_edge(2, 1, 1, 1)
        G.remove_nodes_from_sub_graph(2, [2, 1])
        print(G.heterogeneous_links)
        self.assertEqual([(0, 0, 1, 0)], G.heterogeneous_links)

    def test_nodes_iter(self):
        G = self._setup(3, )
        self.assertEqual(list(iter(G.sub_graphs[0].nodes())), list(G.nodes_iter(0)))

    def test_sub_graph_iter(self):
        G = self._setup(3, )
        self.assertEqual(list(G.sub_graph_iter()), list(iter(G.sub_graphs.values())))

    def test_add_heterogeneous_edge(self):
        G = self._setup(3, )
        G.add_heterogeneous_edge(0, 0, 1, 0)
        G.add_heterogeneous_edge(2, 2, 1, 1)
        print(G.heterogeneous_links)
        self.assertEqual([(0, 0, 1, 0), (1, 1, 2, 2)], G.heterogeneous_links)

    def test_heterogeneous_graph_adj_dict(self):
        G = self._setup(3, )
        G.add_heterogeneous_edge(0, 0, 1, 0)
        G.add_heterogeneous_edge(2, 2, 1, 1)
        print(G.heterogeneous_graph_adj_dict())
        except_result = {
            0: {
                1: {
                    0: {0}
                },
                2: {}
            },
            1: {
                0: {
                    0: {0}
                },
                2: {
                    1: {2}
                }
            },
            2: {
                0: {},
                1: {
                    1: {2}
                }
            }
        }
        self.assertEqual(except_result,
                         G.heterogeneous_graph_adj_dict())

    def test_has_heterogeneous_link(self):
        G = self._setup(3, )
        G.add_heterogeneous_edge(0, 0, 1, 0)
        G.add_heterogeneous_edge(2, 2, 1, 1)
        self.assertTrue(G.has_heterogeneous_link(0, 0, 1, 0))

    def test_heterogeneous_degree_to(self):
        G = self._setup(3, )
        G.add_heterogeneous_edge(0, 0, 1, 0)
        G.add_heterogeneous_edge(0, 0, 1, 1)
        G.add_heterogeneous_edge(0, 0, 2, 1)
        G.add_heterogeneous_edge(2, 2, 1, 1)
        self.assertEqual(2, G.heterogeneous_degree_to(0, 0, 1))
        self.assertEqual(3, G.heterogeneous_degree(0, 0))
