"""
Util function
"""
import networkx as nx

from exception import HeterogeneousLinkBelongsToSameGraphException


def adjlist_of_heterogeneous_graph(graph_1: nx.Graph, graph_2: nx.Graph, heterogeneous_links_bwtween_1_2: list) -> dict:
    """
    adjlist of two heterogeneous graph

    :param graph_1:
    :param graph_2:
    :param heterogeneous_links:
    :return: adjlist between graph_1 and graph_2,
        key: node_index in graph_1
        value: dict, every key refers to a node_index in graph_2 and its value can store attribute of edge
    """
    result = dict()
    for (n1, n2) in heterogeneous_links_bwtween_1_2:  # type:(int,int,int,int)
        if n1 in graph_1.nodes():
            if n2 in graph_2.nodes():
                if n1 in result.keys():
                    result[n1][n2] = {}
                else:
                    result[n1] = {n2: {}}
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
    result = []
    for (g1, n1, g2, n2) in heterogeneous_links:
        if g1 == graph_1_index and g2 == graph_2_index:
            result.append((n1, n2))
        if g1 == graph_2_index and g2 == graph_1_index:
            result.append((n2, n1))
    return result


def sort_heterogeneous_link(graph_1_index: int, node_1_index: int, graph_2_index: int, node_2_index: int) -> tuple:
    if graph_2_index == graph_1_index:
        raise HeterogeneousLinkBelongsToSameGraphException()
    if graph_1_index < graph_2_index:
        return graph_1_index, node_1_index, graph_2_index, node_2_index
    else:
        return graph_2_index, node_2_index, graph_1_index, node_1_index
