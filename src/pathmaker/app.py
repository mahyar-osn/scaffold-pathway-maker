import os
import sys
import json
import argparse

from centreline import load as load_centreline
from connectivity_graph import connectivity_graph
from path_scaffold import write_file, generate_path_scaffold
from scaffold_terms import load

from mapknowledge import KnowledgeStore

import networkx as nx

store_dir = r"C:\Users\egha355\Desktop\work_related\automatenerveTest\codes\scaffold-pathway-maker\tests\ardell\rat"
__store__ = KnowledgeStore(store_dir)


class ProgramArguments(object):
    def __init__(self):
        self.input_manifest = None
        # self.input_model = None
        # self.input_centreline_scaffold = None
        # self.output_ex = None


def write_ex(output_file, path):
    path.generate()
    path.write(output_file)


def _read_scaffold(input_scaffold):
    return load(input_scaffold)


def load_manifest(file_path):
    with open(file_path, "r") as f:
        manifest_data = json.load(f)

    return manifest_data

# def _get_path(markers, connectivity):
#     paths = {}
#     for path in connectivity["paths"]:
#         path_description = {"node coordinates": [], "id": path["id"], "type": path["type"]}
#         for edge in path["edges"]:
#             if edge in markers.keys():
#                 path_description["node coordinates"].append(markers[edge])
#         number_of_element = len(path_description["node coordinates"]) - 1
#         path_description["number of elements"] = number_of_element
#         neuron_path = Path(path_description)
#         paths[path["id"]] = neuron_path
#
#     return paths


def get_paths(entity):
    paths = []
    for path in entity['paths']:
        paths.append(path['id'])
    return paths


def print_paths_edges(paths: list):
    graphs = {}
    for path in paths:
        # skip the one that gives error
        if path != 'ilxtr:neuron-type-aacar-13':
            graphs[path] = connectivity_graph(path, __store__)

            print()
            print(path)
            edge_list = []
            for edge in graphs[path].edges:
                edge_list.append(edge)
                print(edge)


def get_edges_list(path):
    graph = connectivity_graph(path, __store__)
    edge_list = []
    for edge in graph.edges:
        edge_list.append(edge)

    return edge_list


def get_markers(marker_names, x_list):
    markers = {}
    for i, c in enumerate(marker_names):
        markers[c] = x_list[i]
    return markers


def get_model_paths(model: str):
    """ Get ApiNATOMY model data from SCKAN
    """
    entity = __store__.entity_knowledge(model)
    paths = get_paths(entity)

    return paths


def main():
    args = parse_args()
    if os.path.exists(args.input_manifest):

        # if args.output_ex is None:
        #     output_ex = args.input_body_scaffold + '_with_paths.ex'
        # else:
        #     output_ex = args.output_ex

        """ Load data from manifest
        """
        root = os.path.dirname(args.input_manifest)
        manifest = load_manifest(args.input_manifest)
        model = manifest['model']
        centreline_scaffold_file = manifest['centreline']
        whole_body_organ_scaffold_list = manifest['scaffolds']

        """ Get terms from each scaffold
        """
        scaffold_regions = {}
        for name, filename in whole_body_organ_scaffold_list[-1].items():
            f = os.path.join(root, filename)
            region, terms = load(f, name)

        fi = os.path.join(root, centreline_scaffold_file)
        centreline_edges, centreline_marker_names, x_list = load_centreline(fi)
        centreline_markers = get_markers(centreline_marker_names, x_list)

        # body_marker_data = _read_scaffold(args.input_body_scaffold)

        neuron_id = 'ilxtr:neuron-type-aacar-11'
        # neuron_paths = get_model_paths(model)
        # print_paths_edges(neuron_paths)
        # print_paths_edges([neuron_id])

        edge_list = get_edges_list(neuron_id)
        path_nodes, path_elements = generate_path_scaffold(centreline_marker_names, edge_list)

        write_file(path_elements, path_nodes, centreline_markers, os.path.join(root, 'output_neuron_scaffold.exf'))

        # connectivity = _read_connectivity(args.input_connectivity)

        # if body_marker_data is None or entity is None:
        #     sys.exit(-2)
        # else:
        #     pass

            # graph = connectivity_graph(connectivity)
            #
            # paths = _get_path(body_marker_data, connectivity)
            # for index, path in paths.items():
            #     write_ex(output_ex, path)
    else:
        sys.exit(-1)


def parse_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("input_manifest", help="")
    # parser.add_argument("input_model", help="")
    # parser.add_argument("input_centreline_scaffold", help="")
    # parser.add_argument("--output-ex", help="Location of the output ex file. "
    #                                         "[defaults to the location of the input scaffold file if not set.]")

    program_arguments = ProgramArguments()
    parser.parse_args(namespace=program_arguments)

    return program_arguments


if __name__ == "__main__":
    main()
