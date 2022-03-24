from opencmiss.zinc.context import Context
from opencmiss.zinc.field import Field
from opencmiss.zinc.result import RESULT_OK

from opencmiss.utils.zinc.finiteelement import get_element_node_identifiers


def load(input_centreline_file_name):
    context = Context("Centreline Scaffold")
    region = context.getDefaultRegion()
    result = region.readFile(input_centreline_file_name)
    assert result == RESULT_OK, "Failed to load centreline model file" + str(input_centreline_file_name)

    return _get_centreline_connectivity(region)


def _get_centreline_connectivity(region):
    field_module = region.getFieldmodule()
    field_cache = field_module.createFieldcache()
    coordinate_field = field_module.findFieldByName("coordinates")
    marker_name_field = field_module.findFieldByName("marker_name")
    marker_group = field_module.findFieldByName("ilx11")

    mesh = field_module.findMeshByDimension(1)

    nodes = field_module.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)

    element_iter = mesh.createElementiterator()
    element = element_iter.next()
    if marker_group.isValid():
        marker_group = marker_group.castGroup()
        marker_node_group = marker_group.getFieldNodeGroup(nodes)
        if marker_node_group.isValid():

            while element.isValid():
                eft = element.getElementfieldtemplate(coordinate_field, -1)
                node_identifiers = get_element_node_identifiers(element, eft)

                node_names = []
                for node_id in node_identifiers:
                    node = nodes.findNodeByIdentifier(node_id)
                    field_cache.setNode(node)
                    name = marker_name_field.evaluateString(field_cache)
                    node_names.append(name)

                print('Element ', element.getIdentifier())
                print('\t Nodes: ', node_names)
                element = element_iter.next()
