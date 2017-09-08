import networkx as nx
import numpy as np
import scipy as sp


class HeterogeneousGraph(object):
    def __init__(self):
        self.sub_graphs = {}  # type:dict{int:str}
        self.heterogeneous_links = []  # type:list{(int,int,int,int)}

    def add_graph(self, graph: nx.Graph, index: int = None) -> None:
        index = len(self.sub_graphs.keys())
        self.sub_graphs[index] = graph

    def add_node_to_sub_graph(self, sub_graph_index: int, n, attr_dict, **attr) -> None:
        """Add a single node n and update node attributes.

        Parameters
        ----------
        sub_graph_index: int
            int indicate the index of the target graph in sub_graphs
        n : node
            A node can be any hashable Python object except None.
        attr_dict : dictionary, optional (default= no attributes)
            Dictionary of node attributes.  Key/value pairs will
            update existing data associated with the node.
        attr : keyword arguments, optional
            Set or change attributes using key=value.


        :param sub_graph_index:
        :param n:
        :param attr_dict:
        :param attr:
        :return:
        """

        graph = self.sub_graphs[sub_graph_index]  # type:nx.Graph
        graph.add_node(n, attr_dict, **attr)

    def add_nodes_to_sub_graph(self, sub_graph_index: int, nodes, **attr) -> None:
        """Add multiple nodes to sub_graph.

        Parameters
        ----------
        sub_graph_index: int
            int indicate the index of the target graph in sub_graphs
        nodes : iterable container
            A container of nodes (list, dict, set, etc.).
            OR
            A container of (node, attribute dict) tuples.
            Node attributes are updated using the attribute dict.
        attr : keyword arguments, optional (default= no attributes)
            Update attributes for all nodes in nodes.
            Node attributes specified in nodes as a tuple
            take precedence over attributes specified generally.

        :param sub_graph_index:
        :param nodes:
        :param attr:
        :return:
        """
        graph = self.sub_graphs[sub_graph_index]  # type:nx.Graph
        graph.add_nodes_from(nodes, **attr)
