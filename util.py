import networkx as nx
import matplotlib.pyplot as plt
import math

def draw_graph(G):
    elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 0.5]
    esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= 0.5]

    # nodes
    pos = nx.spectral_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=700)

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=elarge, width=6)
    nx.draw_networkx_edges(
        G, pos, edgelist=esmall, width=6, alpha=0.5, edge_color="b", style="dashed"
    )

    # node labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
    # edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    plt.show()

def positive_connected_components(G):
    # Create a copy of the graph and remove all negative edges
    G_positive = G.copy()
    for u, v, w in list(G.edges(data=True)):
        if w['weight'] < 0:
            G_positive.remove_edge(u, v)

    # Find all connected components in the positive graph
    connected_components = list(nx.connected_components(G_positive))

    return connected_components

def find_negative_edge_circle(G, connected_components):
    for component in connected_components:
        subgraph = G.subgraph(component)
        for cycle in nx.cycle_basis(subgraph):
            for u, v in zip(cycle, cycle[1:]):
                if G[u][v]['weight'] < 0:
                    return cycle
    return None

def create_new_graph(G, connected_components):
    new_graph = nx.Graph()
    # Add a node for each connected component
    for component in connected_components:
        new_graph.add_node(frozenset(component))
    # Add edges for negative edges in the original graph
    for u, v, data in G.edges(data=True):
        if data['weight'] < 0:
            # Find the nodes in the new graph corresponding to the connected components
            # containing u and v in the original graph
            u_node = None
            v_node = None
            for component in connected_components:
                if u in component:
                    u_node = frozenset(component)
                if v in component:
                    v_node = frozenset(component)
            # Add the edge between the nodes in the new graph, if it doesn't already exist
            if u_node and v_node and not new_graph.has_edge(u_node, v_node):
                new_graph.add_edge(u_node, v_node, weight=data['weight'])
    return new_graph

def is_bipartite(G):
    # Create a queue for the BFS
    queue = []
    # Create a dictionary to store the colors of the nodes
    colors = {}
    # Add the first node to the queue and assign it the color "0"
    queue.append(list(G.nodes())[0])
    colors[list(G.nodes())[0]] = 0
    # Perform the BFS
    while queue:
        # Get the next node from the queue
        node = queue.pop(0)
        # Get the neighbors of the node
        neighbors = list(G.neighbors(node))
        # Assign the opposite color to the neighbors
        for neighbor in neighbors:
            if neighbor not in colors:
                colors[neighbor] = 1 - colors[node]
                queue.append(neighbor)
            # Return False if a neighbor has the same color as the node
            elif colors[neighbor] == colors[node]:
                return False, colors
    # Return True if the graph is bipartite
    return True, colors


def check_balance(G, draw = True):
    # Create a color map for the edges
    cmap = {1: 'g', -1: 'r'}

    if draw:
        # Draw the original graph
        print("The original graph:")
        nx.draw(G, edge_color=[cmap[data['weight']] for u, v, data in G.edges(data=True)], with_labels=True)
        plt.show()

    # Find the positive connected components of the graph
    components = positive_connected_components(G)
    print('The positve connected components are:', components)

    # Check if there is a negative edge cycle
    cycle = find_negative_edge_circle(G, components)
    if cycle:
        print('Found a circle with odd number of negative edges so there is no balance')
        print("The circle is:", cycle)
        return

    # Create a new graph from the positive connected components
    new_graph = create_new_graph(G, components)
    if draw:
        print("The new graph:")
        nx.draw(new_graph)
        plt.show()

    # Check if the new graph is bipartite
    if is_bipartite(new_graph)[0]:
        print("The new graph is bipartite so the original graph is balanced.")
    else:
        print("The new graph is not bipartite.")
        # Find the cycles in the new graph
        cycles = nx.cycle_basis(new_graph)
        for cycle in cycles:
            if len(cycle) % 2 != 0:
                print(cycle)
                lenght = len(cycle)
                break
        # Find the cycles in the original graph that are at least as long as the cycle found in the new graph
        cycles_orig = nx.cycle_basis(G)
        for cycle in cycles_orig:
            if len(cycle) >= lenght:
                print(cycle)


def walk_balance(G, draw = True):
    if draw:
        print('Original Graph')
        draw_graph(G)

    G_positive = G.copy()
    for u, v, w in list(G.edges(data=True)):
        if w['weight'] < 0:
            G_positive[u][v]['weight'] = 1
    if draw:
        print('The positive graph')
        draw_graph(G_positive)

    # eigenvaluse of original graph
    eig = nx.adjacency_spectrum(G, weight='weight')

    # eigenvalues of postive graph
    eig2 = nx.adjacency_spectrum(G_positive)

    # Number of nodes
    n = len(G.nodes)

    sum1 = 0
    sum2 = 0
    for j in range(n):
        sum1 = sum1 + math.exp(eig[j])
        sum2 = sum2 + math.exp(eig2[j])

    K = sum1 / sum2
    print(f"{K:.3f}")
