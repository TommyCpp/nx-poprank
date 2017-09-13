import networkx as nx


class HeterogeneousLinkBelongsToSameGraphException(nx.NetworkXException):
    def __init__(self):
        pass

    def __str__(self):
        return "Try to add a heterogeneous link whose nodes belongs to same graph. Use nx.Graph.add_edge " \
                       "instead "
