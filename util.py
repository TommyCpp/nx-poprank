"""
Util function
"""
import networkx as nx

from exception import HeterogeneousLinkBelongsToSameGraphException


def adjlist_of_heterogeneous_graph(G, graph_1_index: int, graph_2_index: int,
                                   heterogeneous_links: list) -> dict:
    """
    adjlist of two heterogeneous graph

    :param G:
    :param graph_1_index:
    :param graph_2_index:
    :param heterogeneous_links:
    :return:
    """
    result = dict()
    graph_1 = G.sub_graphs[graph_1_index]
    graph_2 = G.sub_graphs[graph_2_index]
    for link in heterogeneous_links:  # type:(int,int,int,int)
        if link[0] == graph_1_index:
            pair_1 = (link[0], link[1])
            pair_2 = (link[2], link[3])
        else:
            pair_1 = (link[2], link[3])
            pair_2 = (link[0], link[1])

        if pair_1[1] in graph_1.nodes():
            if pair_2[1] in graph_2.nodes():
                if pair_1[1] in result.keys():
                    result[pair_1[1]][pair_2[1]] = 1
                else:
                    result[pair_1[1]] = {pair_2[1]}
            else:
                raise nx.NetworkXError("node not in graph_2")
        else:
            raise nx.NetworkXError("node not in graph_1")
    return result


def filter_heterogeneous_links(graph_1_index, graph_2_index, heterogeneous_links: list):
    """Filter the heterogeneous_links
    return links that connect graph_1 and graph_2

    :param graph_1_index:
    :param graph_2_index:
    :param heterogeneous_links:
    :return:
    """
    return list(filter(
        lambda x: (x[0] == graph_1_index and x[2] == graph_2_index) or (
            x[0] == graph_2_index and x[2] == graph_1_index),
        iter(heterogeneous_links)))


def sort_heterogeneous_link(graph_1_index: int, node_1_index: int, graph_2_index: int, node_2_index: int) -> tuple:
    if graph_2_index == graph_1_index:
        raise HeterogeneousLinkBelongsToSameGraphException()
    if graph_1_index < graph_2_index:
        return graph_1_index, node_1_index, graph_2_index, node_2_index
    else:
        return graph_2_index, node_2_index, graph_1_index, node_1_index
