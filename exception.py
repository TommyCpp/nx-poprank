import networkx as nx


class HeterogeneousLinkBelongsToSameGraphException(nx.NetworkXException):
    def __init__(self):
        pass

    def __str__(self):
        return "Try to add a heterogeneous link whose nodes belongs to same graph. Use nx.Graph.add_edge " \
               "instead "


class PopRankAlgorithmParamException(nx.NetworkXException):
    params = {
        "epsilon": "epsilon should be in 0-1",
        "alpha": "alpha should be in 0-1",
        "max_iter": "max_iter should bigger than 0",
        "propagation_factor": "propagation_factor should be an numpy array"
    }

    def __init__(self, param):
        self.param = param

    def __str__(self):
        return self.params[self.param]


class SubGraphNotExist(nx.NetworkXException):
    def __init__(self):
        pass

    def __str__(self):
        return "sub graph not exist"

