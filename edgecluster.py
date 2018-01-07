import heapq
from typing import Tuple, Callable, Iterable, List

from heterogeneousgraph import HeGraph
import networkx as nx


def find_community_by_edge_cluster(G: nx.Graph(), nodeValueCaculateFunc: Callable):
    pass


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


def get_edge_priority_queue_by_coefficient_of_edge_clustering(G: nx.Graph,
                                                              edgeWeightfunc: Callable = lambda x, y: (x + y) / 2.):
    result = []
    for (u, v) in G.edges():
        uValue = G.node[u]["value"]
        vValue = G.node[v]["value"]
        heapq.heappush(result, (edgeWeightfunc(uValue, vValue), u, v))
    return result
