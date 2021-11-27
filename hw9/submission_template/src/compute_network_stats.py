import json
import os
import argparse
import networkx as nx
from networkx.algorithms.centrality import betweenness_centrality

def parse_args():

    parser = argparse.ArgumentParser(description='Compile pony word counts')
    parser.add_argument('-i', help='<interaction_network.json>', required=True)
    parser.add_argument('-o', help='<stats.json>', required=True)
    args = parser.parse_args()

    return args.i, args.o


def verify_directory(path):

    # Verify if save directory exists, make it if necessary
    save_dir = os.path.split(path)[0]
    if save_dir != '':
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)

def get_graph(json_data):
    
    graph = nx.Graph()

    for pony in json_data:
        for pony2 in json_data[pony]:
            graph.add_edge(pony, pony2, weight=json_data[pony][pony2])

    return graph


def analyze(graph):
    
    # Initialize output dictionary
    output_dict = {'most_connected_by_num': None, 'most_connected_by_weight': None, 'most_central_by_betweenness': None}

    # Get top three most connected characters by node degree
    most_edges = []
    node_degrees = list(graph.degree())
    node_degrees.sort(key=lambda x: -x[1])
    for i in range(3):
        most_edges.append(node_degrees[i][0])
    output_dict['most_connected_by_num'] = most_edges

    # Get the top three most connected characters by weighted node degree
    most_weight = []
    wnode_degree = list(graph.degree(weight='weight'))
    wnode_degree.sort(key=lambda x: -x[1])
    for i in range(3):
        most_weight.append(wnode_degree[i][0])
    output_dict['most_connected_by_weight'] = most_weight

    # Get the top three most central characters by betweenness
    most_central = []
    centrality = list(betweenness_centrality(graph).items())
    centrality.sort(key=lambda x: -x[1])
    for i in range(3):
        most_central.append(centrality[i][0])
    output_dict['most_central_by_betweenness'] = most_central 
    
    return output_dict


def main():
    
    input_fname, output_fname = parse_args()
    
    with open(input_fname, 'r') as f:
        json_data = json.load(f)
    
    graph = get_graph(json_data)
    
    output_dict = analyze(graph)

    verify_directory(output_fname)

    with open(output_fname, 'w') as f:
        json.dump(output_dict, f, indent=2)

if __name__=='__main__':
    main()
