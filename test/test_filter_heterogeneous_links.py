import networkx as nx

from HeGraph import filter_heterogeneous_links

if __name__ == "__main__":

    """
    Setup
    
    """
    heterogeneous_links = [(0, 0,1, 0), (1, 1, 0, 1), (1, 2, 4, 5)]

    """
    Test
    
    """
    result = filter_heterogeneous_links(0, 1, heterogeneous_links)
    print(result)
    assert 2 == len(result)
