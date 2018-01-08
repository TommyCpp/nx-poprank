import heapq

import edgecluster as ec
from .GraphTestCase import GraphTestCase


class EdgeClusterTest(GraphTestCase):
    def _setup(self, sub_graph_count=1, node_per_graph=3, **kwargs):
        return super()._setup(sub_graph_count, node_per_graph, 1)

    def test_edge_cluster_coefficient_in_3_dimension(self):
        G = self._setup()
        print(ec.edge_cluster_coefficient_in_3_dimension(G.sub_graphs[0], 0, 1))

    def test_get_edge_priority_queue_by_coefficient_of_edge_clustering(self):
        nodeValue = {0: 0.219386, 1: 0.213213, 3: 0.55, 4: 0.3249}
        edges = [(0, 1), (1, 3), (3, 4), (1, 4), (0, 4)]
        result = ec.get_edge_priority_queue_by_coefficient_of_edge_clustering(nodeValue, edges)

        priority_queue = []
        length = len(result)
        for i in range(length):
            priority_queue.append(result.get())

        print(priority_queue)

        for i in range(len(priority_queue) - 1):
            self.assertTrue(priority_queue[i][0] > priority_queue[i + 1][0])
