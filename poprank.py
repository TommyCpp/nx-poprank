"""
PopRank Algorithm

"""
import numpy as np

from exception import PopRankAlgorithmParamException
from heterogeneousgraph import HeGraph
import networkx as nx


# todo: test
def pop_rank(g: HeGraph, epsilon=0.5, propagation_factor=None, alpha=0.85, max_iter=100):
    """

    :param max_iter:
    :param g:
    :param epsilon:
    :param propagation_factor:
    :param alpha:
    :return:
    """
    # setup propagation_factor
    sub_graph_count = len(g.sub_graphs.items())
    if propagation_factor is None:
        factor = 1. / (sub_graph_count - 1)
        propagation_factor = np.array([[factor] * sub_graph_count] * sub_graph_count)

    # check param
    if max_iter < 0:
        raise PopRankAlgorithmParamException("max_iter")
    if alpha > 1 or alpha < 0:
        raise PopRankAlgorithmParamException("alpha")
    if epsilon > 1 or alpha < 0:
        raise PopRankAlgorithmParamException("epsilon")
    if propagation_factor is not None and not isinstance(propagation_factor, np.ndarray):
        raise PopRankAlgorithmParamException("propagation_factor")

    page_rank = {graph_index: nx.pagerank(g.sub_graphs[graph_index], alpha=alpha) for graph_index in
                 g.sub_graphs.keys()}  # pagerank value of every sub graph

    poprank = {}
    iterator_pop_rank = {}

    for sub_graph_index in g.sub_graphs.keys():
        poprank[sub_graph_index] = np.array([page_rank[sub_graph_index].values()])
        iterator_pop_rank[sub_graph_index] = np.zeros((1, len(np.array([page_rank[sub_graph_index].values()]))))

    m_xy = heterogeneous_neighbour_matrix(g)

    for i in range(max_iter):
        iterator_pop_rank = {}
        for x in range(len(poprank)):
            y_sum = np.zeros((1, len(g.sub_graphs[x].nodes())))
            for y in range(sub_graph_count):
                if y != x:  # if not the same sub graph
                    y_sum += propagation_factor[y][x] * m_xy[y][x].T.dot(poprank[y].T).T

            iterator_pop_rank[x] = epsilon * poprank[x] + (1 - epsilon) * y_sum
        poprank = iterator_pop_rank
    return poprank


def heterogeneous_neighbour_matrix(G: HeGraph):
    result = {}
    adj_dict = G.heterogeneous_graph_adj_dict()
    for x, x_graph in G.sub_graphs.items():
        result[x] = {}
        for y, y_graph in G.sub_graphs.items():
            if x != y:
                result[x][y] = np.zeros(
                    (len(x_graph.nodes()), len(y_graph.nodes()))
                )
                for x_node in adj_dict[x][y].keys():
                    for y_node in adj_dict[x][y][x_node]:
                        result[x][y][x_node][y_node] = 1. / G.heterogeneous_degree_to(y, y_node, x)

    return result
