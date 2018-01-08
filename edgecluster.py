import heapq
import queue
from typing import Tuple, Callable, Iterable, List, Dict

from heterogeneousgraph import HeGraph
import networkx as nx


class MaxHeap:
    data = []

    def put(self, input):
        heapq.heappush(self.data, (-input[0], input[1], input[2]))

    def get(self):
        result = heapq.heappop(self.data)
        return -result[0], result[1], result[2]

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return str(self.data)

    def empty(self):
        return len(self.data) == 0


def find_community_by_edge_cluster(G: nx.Graph, nodeValueCaculateFunc: Callable):
    node_values = nx.get_node_attributes(G, "value")
    edges = G.edges()
    max_heap = get_edge_priority_queue_by_coefficient_of_edge_clustering(node_values, edges)
    has_in_community = set()
    while not max_heap.empty():
        edge_with_attr = max_heap.get()
        seed_edge = (edge_with_attr[1], edge_with_attr[2])
        if seed_edge in has_in_community:
            continue
        else:
            # find local community
            community = {seed_edge}
            has_in_community.add(seed_edge)
            while 1:
                canadians = MaxHeap()
                # todo: continue implement


def sort_node_of_edge(edges: Iterable[Tuple[int, int]]):
    return [(edge[0], edge[1]) if edge[0] < edge[1] else (edge[1], edge[0]) for edge in edges]


def get_node_from_edge_community(edge_community: Iterable[Tuple[int, int]]):
    node_set = set()
    for edge in edge_community:
        node_set.add(edge[0])
        node_set.add(edge[1])
    return node_set


def convert_edge_communities_to_node_communities(edge_communities: Iterable[Iterable[Tuple[int, int]]]) -> Iterable[
    Iterable[int]]:
    return [get_node_from_edge_community(edge_community) for edge_community in edge_communities]


def edge_cluster_coefficients(G: nx.Graph) -> dict:
    result = {}
    for (u, v) in G.edges():
        edge_cluster_coefficient = edge_cluster_coefficient_in_3_dimension(G, u, v)
        if u < v:
            result[(u, v)] = edge_cluster_coefficient
        else:
            result[(v, u)] = edge_cluster_coefficient
    return result


def edge_cluster_coefficient_in_3_dimension(G: nx.Graph, u: int, v: int) -> float:
    """

    :param G: graph
    :param u: one node of edge
    :param v: another node of edge
    :return: coefficient of edge clustering(边聚类系数)
    """
    u_neighbour = G.neighbors(u)
    v_neighbour = G.neighbors(v)
    z3 = [node for node in u_neighbour if node in v_neighbour]
    min_k = min(G.degree(u) - 1, G.degree(v) - 1)
    return (len(z3) + 1.) / min_k if min_k != 0 else 0


def get_edge_priority_queue_by_coefficient_of_edge_clustering(nodeValue: Dict, edges: List,
                                                              edgeWeightfunc: Callable = lambda x, y: (x + y) / 2.):
    """

    :param nodeValue:
    :param edges:
    :param edgeWeightfunc:
    :return: heap, use heapq.heappop to get value
    """
    result = MaxHeap()

    for (u, v) in edges:
        result.put((edgeWeightfunc(nodeValue[u], nodeValue[v]), u, v))
    return result


def get_neighbour_edge_of_edge_community(G: nx.Graph, edge_community: List):
    result = set()
    community_nodes = get_node_from_edge_community(edge_community)
    for node in community_nodes:
        for neighbour in G.neighbors(node):
            if neighbour not in community_nodes:
                result.add((node, neighbour) if node < neighbour else (neighbour, node))
    return list(result)


def community_fitness(node_value: Dict, edge_community: List, edge_weight_func: Callable = lambda x, y: (x + y) / 2.):
    def get_m_in():
        """
        Computer the sum of node's value
        :param nodes:
        :return:
        """
        result = 0.
        for edge in edge_community:
            result += edge_weight_func(*edge)
        return result

    def get_m_out(nodes):
        result = 0.
        # todo:implement
    community_nodes = get_node_from_edge_community(edge_community)
    return
