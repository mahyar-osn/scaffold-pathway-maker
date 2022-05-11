from opencmiss.zinc.element import Element, Elementbasis
from opencmiss.zinc.field import Field
from opencmiss.zinc.node import Node
from opencmiss.zinc.context import Context
from opencmiss.utils.zinc.field import findOrCreateFieldCoordinates, find_or_create_field_group, findOrCreateFieldGroup
from opencmiss.utils.zinc.general import ChangeManager


class Path(object):

    def __init__(self, options: dict):
        self.__context = Context(options["id"])
        self.__region = self.__context.getDefaultRegion()
        self.__options = options

    def get_context(self):
        return self.__context

    def get_region(self):
        return self.__region

    def get_options(self):
        return self.__options

    def generate(self):
        coordinate_dimensions = 3
        elements_count = self.__options['number of elements']
        node_coordinates = self.__options['node coordinates']

        field_module = self.__region.getFieldmodule()

        with ChangeManager(field_module):
            field_module.beginChange()
            coordinates = findOrCreateFieldCoordinates(field_module, components_count=coordinate_dimensions)
            cache = field_module.createFieldcache()

            # Create nodes

            nodes = field_module.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)
            node_template = nodes.createNodetemplate()
            node_template.defineField(coordinates)
            node_template.setValueNumberOfVersions(coordinates, -1, Node.VALUE_LABEL_VALUE, 1)
            node_template.setValueNumberOfVersions(coordinates, -1, Node.VALUE_LABEL_D_DS1, 1)

            node_identifier = 1

            for n in range(len(node_coordinates)):
                node = nodes.createNode(node_identifier, node_template)
                cache.setNode(node)
                x = node_coordinates[n]
                # d = node_derivatives[n]

                coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_VALUE, 1, x)
                # coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS1, 1, d)
                node_identifier = node_identifier + 1

            # Create elements

            mesh = field_module.findMeshByDimension(1)
            cubic_hermite_basis = field_module.createElementbasis(1, Elementbasis.FUNCTION_TYPE_CUBIC_HERMITE)
            eft = mesh.createElementfieldtemplate(cubic_hermite_basis)
            element_template = mesh.createElementtemplate()
            element_template.setElementShapeType(Element.SHAPE_TYPE_LINE)
            result = element_template.defineField(coordinates, -1, eft)

            element_identifier = 1
            for e in range(elements_count):
                element = mesh.createElement(element_identifier, element_template)
                element.setNodesByIdentifier(eft, [e + 1, e + 2])
                element_identifier = element_identifier + 1

    def write(self, filename: str):
        self.__region.writeFile(filename)


def generate_path_scaffold(centreline_marker_names, edge_list):
    """
    Find match points between centreline and edges list and if the element is valid store the nodes and elements lists.
    :param centreline_marker_names: list of marker names in the centreline.
    :param edge_list: list of edges in the path.
    :return: list of nodes and valid elements of the scaffold.
    """

    def find_term_level():
        level = -1
        for c in node_term.split():
            if c.lower() in edge[nid].lower():
                # find level it is found. \n separates the levels. The term with minimum level is what we want.
                for i, t in enumerate(edge[nid].lower().split('\n')):
                    if c.lower() in t:
                        level = i
            else:
                level = -1
                break
        return level

    def find_inner_term():
        level_min = 100
        for t in terms:
            if t[1] < level_min:
                inner_term = t[0]

        return inner_term

    terms = []
    path_elements = []
    for edge in edge_list:
        node_names = [None, None]
        for nid in range(2):
            heart = 'heart' in edge[nid].lower()
            found_whole_term = False
            for node_term in centreline_marker_names:
                lvl = find_term_level()
                if lvl != -1:
                    found_whole_term = True
                    terms.append([node_term, lvl])

            if found_whole_term:
                node_term_t = find_inner_term()
                node_names[nid] = node_term_t
            # if the term is heart use fibrous pericardium coordinates.
            elif heart:
                node_names[nid] = 'fibrous pericardium'
        # Ignore the element if its nodes are the same.
        if node_names[0] != node_names[1]:
            if node_names[0] and node_names[1]:
                path_elements.append(node_names)

    path_nodes = set()
    for c in path_elements:
        path_nodes.add(c[0])
        path_nodes.add(c[1])
    path_nodes = list(sorted(path_nodes))

    return path_nodes, path_elements


def write_file(path_edges, path_nodes, markers_data, filename):
    """
    Write path scaffold into a zinc file.
    :param path_edges: list of edges in the scaffold.
    :param path_nodes: list of scaffold nodes terms.
    :param markers_data: a list of {marker name: coordinates}
    :param filename: output file name
    """
    elements_count = len(path_edges)
    nd = {}
    for i, c in enumerate(path_nodes):
        nd[c] = i + 1
    context = Context('neuron path')
    region = context.getDefaultRegion()

    coordinate_dimensions = 3
    field_module = region.getFieldmodule()

    with ChangeManager(field_module):
        coordinates = findOrCreateFieldCoordinates(field_module, components_count=coordinate_dimensions)
        cache = field_module.createFieldcache()

        # Create nodes
        nodes = field_module.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)
        node_template = nodes.createNodetemplate()
        node_template.defineField(coordinates)
        node_template.setValueNumberOfVersions(coordinates, -1, Node.VALUE_LABEL_VALUE, 1)
        node_template.setValueNumberOfVersions(coordinates, -1, Node.VALUE_LABEL_D_DS1, 1)

        node_identifier = 1

        for n in path_nodes:
            node = nodes.createNode(node_identifier, node_template)
            cache.setNode(node)
            x = markers_data[n]
            # d = node_derivatives[n]

            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_VALUE, 1, x)
            # coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS1, 1, d)
            node_identifier = node_identifier + 1

        # Create elements

        mesh = field_module.findMeshByDimension(1)
        cubic_hermite_basis = field_module.createElementbasis(1, Elementbasis.FUNCTION_TYPE_CUBIC_HERMITE)
        eft = mesh.createElementfieldtemplate(cubic_hermite_basis)
        element_template = mesh.createElementtemplate()
        element_template.setElementShapeType(Element.SHAPE_TYPE_LINE)
        result = element_template.defineField(coordinates, -1, eft)

        element_identifier = 1
        for e in range(elements_count):
            element = mesh.createElement(element_identifier, element_template)
            element.setNodesByIdentifier(eft, [nd[path_edges[e][0]], nd[path_edges[e][1]]])
            element_identifier = element_identifier + 1

    region.writeFile(filename)
