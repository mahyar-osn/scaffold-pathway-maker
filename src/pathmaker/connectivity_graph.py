import ipycytoscape
import networkx as nx


def label(term, kdb):
    if term is not None:
        label = kdb.label(term)
        return f'{term}: {label}' if label is not None else term
    return ''


def node_id(node, kdb):
    names = [label(node[0], kdb)]
    for term in node[1]:
        names.append(label(term, kdb))
    return '\n'.join(names)


def connectivity_graph(neuron_population_id, kdb):
    knowledge = kdb.entity_knowledge(neuron_population_id)
    G = nx.Graph()
    for n, pair in enumerate(knowledge.get('connectivity', [])):
        nodes = (node_id(pair[0], kdb),
                 node_id(pair[1], kdb))
        if nodes[0] != nodes[1]:
            G.add_edge(*nodes, directed=True, id=n)
            n += 1

    g = ipycytoscape.CytoscapeWidget()
    g.graph.add_graph_from_networkx(G, directed=True)

    return G
