import heapq
import queue
from typing import Tuple, Callable, Iterable, List, Dict, Set

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
    edge_clusters = edge_cluster_coefficients(G)
    has_in_community = set()
    communities = []
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
                # todo: test all function
                neighbours = get_neighbour_edge_of_edge_community(G, community)
                for neighbour in neighbours:
                    if neighbour not in community and neighbour not in has_in_community:
                        value = edge_fitness(G, neighbour, community, edge_clusters)
                        if value > 0:
                            canadians.put((value, neighbour[0], neighbour[1]))
                if canadians.empty():
                    communities.append(community)
                    break

                while not canadians.empty():
                    edge = tuple(canadians.get()[1:])
                    community.add(edge)
                    has_in_community.add(edge)
                    canadians = resort_canadians(G, canadians, community, edge_clusters)
    return communities


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


def get_neighbour_edge_of_edge_community(G: nx.Graph, edge_community: Set):
    result = set()
    community_nodes = get_node_from_edge_community(edge_community)
    for node in community_nodes:
        for neighbour in G.neighbors(node):
            if neighbour not in community_nodes:
                result.add((node, neighbour) if node < neighbour else (neighbour, node))
    return result


def community_fitness(G: nx.Graph, edge_community: List, alpha=0.5,
                      edge_weight_func: Callable = lambda x, y: (x + y) / 2.):
    def get_m_in(edge_community):
        """
        Computer the sum of node's value
        :param nodes:
        :return:
        """
        result = 0.
        for edge in edge_community:
            result += edge_weight_func(*edge)
        return result

    def get_m_out(edge_community):
        result = 0.
        neighbour_edges = get_neighbour_edge_of_edge_community(G, edge_community)
        for edge in neighbour_edges:
            result += edge_weight_func(*edge)
        return result

    return get_m_in(edge_community) / ((get_m_in(edge_community) + get_m_out(edge_community)) ** alpha)


def edge_fitness(G, edge, community, clusters):
    u = edge[0]
    v = edge[1]
    mock_community = community.copy()
    edge_cluster = clusters[(u, v)]
    if (u, v) in community:
        community_fitness_with_edge = community_fitness(G, mock_community)
        mock_community.remove((u, v))
        community_fitness_without_edge = community_fitness(G, mock_community)
        return (edge_cluster + 2) * (community_fitness_with_edge - community_fitness_without_edge)
    else:
        community_fitness_without_edge = community_fitness(G, mock_community)
        mock_community.append((u, v))
        community_fitness_with_edge = community_fitness(G, mock_community)
        return (edge_cluster + 2) * (community_fitness_with_edge - community_fitness_without_edge)


def resort_canadians(G, canadians, community, clusters):
    result = MaxHeap()
    while not canadians.empty():
        edge = tuple(canadians.get()[1:])
        value = edge_fitness(G, edge, community, clusters)
        if value > 0:
            result.put((-value, *edge))
    return result
