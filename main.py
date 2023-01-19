# This is a sample Python script.

# Press Shift+F10 pipto execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import networkx as nx
import matplotlib.pyplot as plt
import math
import warnings
import util
import urllib.request
import os
import tarfile

warnings.filterwarnings('ignore')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # First graph example
    G1 = nx.Graph()

    G1.add_edge(1, 2, weight=1)
    G1.add_edge(2, 3, weight=1)
    G1.add_edge(3, 4, weight=1)
    G1.add_edge(4, 1, weight=1)
    G1.add_edge(1, 3, weight=-1)

    util.check_balance(G1)
    ##########################################################################
    # Second graph example
    G = nx.Graph()
    G.add_edge(0, 1, weight=-1)
    G.add_edge(0, 2, weight=1)
    G.add_edge(1, 2, weight=-1)
    util.check_balance(G)
    ##########################################################################
    # Third graph example from eclass
    G = nx.Graph()
    G.add_edge(0, 1, weight=1)
    G.add_edge(0, 2, weight=1)
    G.add_edge(1, 2, weight=1)
    G.add_edge(1, 4, weight=1)
    G.add_edge(1, 3, weight=-1)
    G.add_edge(2, 5, weight=-1)
    G.add_edge(3, 7, weight=-1)
    G.add_edge(3, 8, weight=-1)

    G.add_edge(4, 5, weight=-1)

    G.add_edge(5, 6, weight=1)
    G.add_edge(5, 10, weight=-1)

    G.add_edge(6, 10, weight=-1)

    G.add_edge(7, 11, weight=1)

    G.add_edge(8, 11, weight=1)

    G.add_edge(9, 11, weight=1)
    G.add_edge(9, 10, weight=-1)

    G.add_edge(10, 12, weight=-1)
    G.add_edge(10, 13, weight=-1)

    G.add_edge(11, 12, weight=1)

    G.add_edge(12, 14, weight=-1)

    G.add_edge(13, 14, weight=-1)

    util.check_balance(G)
    ###################################################################################

    # Tribes Graph
    filename = 'ucidata-gama.tar.bz2'
    url = "http://konect.cc/files/download.tsv.{}".format(filename)
    if not os.path.exists(filename):
        urllib.request.urlretrieve(url, filename)

    tar = tarfile.open(filename, "r:bz2")
    tar.extractall()
    tar.close()
    # Load the graph using NetworkX's `read_edgelist` function
    G = nx.read_edgelist('ucidata-gama/out.ucidata-gama', comments='%', nodetype=int, data=[('sign', int)])

    # You can then access the nodes and edges of the graph using the `nodes` and `edges` methods
    nodes = G.nodes()
    edges = G.edges()

    # You can also access the sign of each edge using the `get_edge_attributes` method
    signs = nx.get_edge_attributes(G, 'sign')
    nx.set_edge_attributes(G, signs, 'weight')

    util.check_balance(G)
    util.walk_balance(G)

    ####################################################################################
    # Wiki conflict Graph
    filename = 'wikiconflict.tar.bz2'
    url = "http://konect.cc/files/download.tsv.{}".format(filename)
    if not os.path.exists(filename):
        urllib.request.urlretrieve(url, filename)

    tar = tarfile.open(filename, "r:bz2")
    tar.extractall()
    tar.close()
    # Load the graph using NetworkX's `read_edgelist` function
    G = nx.read_edgelist('wikiconflict/out.wikiconflict', comments='%', nodetype=int, data=[('sign', float), ('unknown', int)])

    # You can then access the nodes and edges of the graph using the `nodes` and `edges` methods
    nodes = G.nodes()
    edges = G.edges()

    # You can also access the sign of each edge using the `get_edge_attributes` method
    signs = nx.get_edge_attributes(G, 'sign')
    nx.set_edge_attributes(G, signs, 'weight')

    util.check_balance(G, draw = False)
    ########################################################################################
    G = nx.Graph()

    G.add_edge(1, 2, weight=1)
    G.add_edge(1, 3, weight=-1)
    G.add_edge(1, 5, weight=1)
    G.add_edge(2, 3, weight=-1)
    G.add_edge(3, 4, weight=1)
    G.add_edge(4, 5, weight=1)

    util.walk_balance(G)
    #######################################################################################
    G = nx.Graph()

    G.add_edge(1, 2, weight=1)
    G.add_edge(1, 3, weight=1)
    G.add_edge(1, 5, weight=1)
    G.add_edge(2, 3, weight=-1)
    G.add_edge(3, 4, weight=-1)
    G.add_edge(4, 5, weight=1)

    util.walk_balance(G)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
