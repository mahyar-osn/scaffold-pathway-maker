import os
import sys
import json
import argparse

from pathmaker.scaffold_terms import load
from pathmaker.centreline import load as load_centreline
from pathmaker.connectivity_graph import connectivity_graph
from pathmaker.path_scaffold import Path

from mapknowledge import KnowledgeStore


__store__ = KnowledgeStore(None)


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

        """ Get ApiNATOMY model data from SCKAN
        """
        entity = __store__.entity_knowledge(model)

        """ Get terms from each scaffold
        """
        scaffold_regions = {}
        for name, filename in whole_body_organ_scaffold_list[-1].items():
            f = os.path.join(root, filename)
            region, terms = load(f, name)

        load_centreline(centreline_scaffold_file)

        # body_marker_data = _read_scaffold(args.input_body_scaffold)
        neuron_paths = get_paths(entity)

        graphs = {}

        for path in neuron_paths:
            if path == 'ilxtr:neuron-type-aacar-11':
                graphs[path] = connectivity_graph(path, __store__)

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
