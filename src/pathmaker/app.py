import os
import sys
import json
import argparse

from pathmaker.body_markers import load
from pathmaker.path_scaffold import Path


class ProgramArguments(object):
    def __init__(self):
        self.input_body_scaffold = None
        self.input_connectivity = None
        self.output_ex = None


def write_ex(output_file, path):
    path.generate()
    path.write(output_file)


def _get_path(markers, connectivity):
    paths = {}
    for path in connectivity["paths"]:
        path_description = {"node coordinates": [], "id": path["id"], "type": path["type"]}
        for edge in path["edges"]:
            if edge in markers.keys():
                path_description["node coordinates"].append(markers[edge])
        number_of_element = len(path_description["node coordinates"]) - 1
        path_description["number of elements"] = number_of_element
        neuron_path = Path(path_description)
        paths[path["id"]] = neuron_path

    return paths


def _read_connectivity(input_connectivity):
    with open(input_connectivity, "r") as path_data:
        connectivity = json.load(path_data)
    return connectivity


def _read_scaffold(input_scaffold):
    return load(input_scaffold)


def main():
    args = parse_args()
    if os.path.exists(args.input_body_scaffold) and os.path.exists(args.input_connectivity):
        if args.output_ex is None:
            output_ex = args.input_body_scaffold + '_with_paths.ex'
        else:
            output_ex = args.output_ex

        body_marker_data = _read_scaffold(args.input_body_scaffold)
        connectivity = _read_connectivity(args.input_connectivity)

        if body_marker_data is None or connectivity is None:
            sys.exit(-2)
        else:
            paths = _get_path(body_marker_data, connectivity)
            for index, path in paths.items():
                write_ex(output_ex, path)
    else:
        sys.exit(-1)


def parse_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("input_body_scaffold", help="")
    parser.add_argument("input_connectivity", help="")
    parser.add_argument("--output-ex", help="Location of the output ex file. "
                                            "[defaults to the location of the input scaffold file if not set.]")

    program_arguments = ProgramArguments()
    parser.parse_args(namespace=program_arguments)

    return program_arguments


if __name__ == "__main__":
    main()
