import networkx as nx
import numpy as np
import scipy as sp

node_dict_factory = dict
graph_dict_factory = dict
adjlist_dict_factory = dict


class HeGraph(object):
    def __init__(self):
        self.node_dict_factory = ndf = self.node_dict_factory
        self.adjlist_dict_factory = self.adjlist_dict_factory
        self.graph_dict_factory = gdf = self.graph_dict_factory

        self.adj = ndf()  # empty adjacency dict
        self.sub_graphs = gdf()  # type:dict{int:str}
        self.heterogeneous_links = []  # type:list{(int,int,int,int)}
        self.heterogeneous_adj = adjlist_dict_factory()

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
        try:
            graph = self.sub_graphs[sub_graph_index]  # type:nx.Graph
        except IndexError:
            raise nx.NetworkXError("the graph %s is not in heterogeneous graph dict" % sub_graph_index)
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

    def remove_node(self, sub_graph_index: int, n):
        """Remove node n.

        Removes the node n and all adjacent edges.
        Attempting to remove a non-existent node will raise an exception.

        Parameters
        ----------
        sub_graph_index: int
            index of the graph
        n : node
           A node in the graph

        Raises
        -------
        NetworkXError
           If n is not in the graph.

       :param n:
       :param sub_graph_index:
        """
        graph = self.sub_graphs[sub_graph_index]  # type:nx.Graph
        graph.remove_node(n)

    def add_heterogeneous_edge(self, graph_index_1, node_index_1, graph_index_2, node_index_2):
        """Add an heterogeneous edge

        Parameters
        ----------
        graph_index_1: int
            index of the first graph

        node_index_1: int
            index of node in first graph

        graph_index_2: int
            index of the second graph

        node_index_2: int
            index of node in second graph


        Raise
        -----
        NetworkXError
            If the node is not in graph.
            If the graph is not in sub graph.

        :param graph_index_1:
        :param node_index_1:
        :param graph_index_2:
        :param node_index_2:
        :return:
        """
        if graph_index_1 in self.sub_graphs.keys() and graph_index_2 in self.sub_graphs.keys():
            if node_index_1 in self.sub_graphs[graph_index_1].nodes() and node_index_2 in self.sub_graphs[
                graph_index_2].nodes():
                self.heterogeneous_links.append((graph_index_1, node_index_1, graph_index_2, node_index_2))
            else:
                raise nx.NetworkXError("the node is not in graph")
        else:
            raise nx.NetworkXError("the graph is not in sub graphs")
