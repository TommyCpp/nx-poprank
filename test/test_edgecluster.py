import edgecluster as ec
from .GraphTestCase import GraphTestCase


class EdgeClusterTest(GraphTestCase):
    def _setup(self, sub_graph_count=1, node_per_graph=3, **kwargs):
        return super()._setup(sub_graph_count, node_per_graph, 1)

    def test_edge_cluster_coefficient_in_3_dimension(self):
        G = self._setup()
        print(ec.edge_cluster_coefficient_in_3_dimension(G.sub_graphs[0], 0, 1))
