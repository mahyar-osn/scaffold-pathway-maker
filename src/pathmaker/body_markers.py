from opencmiss.zinc.context import Context
from opencmiss.zinc.field import Field
from opencmiss.zinc.result import RESULT_OK
from opencmiss.utils.zinc.general import ChangeManager


def load(input_body_file_name):
    context = Context("Body Scaffold")
    region = context.getDefaultRegion()
    result = region.readFile(input_body_file_name)
    assert result == RESULT_OK, "Failed to load body model file" + str(input_body_file_name)

    return _get_marker_coordinates(region)


def _get_marker_coordinates(region):
    field_module = region.getFieldmodule()
    field_cache = field_module.createFieldcache()
    coordinate_field = field_module.findFieldByName("coordinates")
    element_xi_field = field_module.findFieldByName("body_marker_location")
    body_marker_name_field = field_module.findFieldByName("body_marker_name")
    marker_group = field_module.findFieldByName("body_marker")

    nodes = field_module.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)

    if marker_group.isValid():
        marker_group = marker_group.castGroup()
        marker_node_group = marker_group.getFieldNodeGroup(nodes)
        if marker_node_group.isValid():
            marker_nodes = marker_node_group.getNodesetGroup()

            if element_xi_field.isValid() and body_marker_name_field.isValid():
                with ChangeManager(field_module):
                    body_marker_coordinate_field = field_module.createFieldEmbedded(coordinate_field, element_xi_field)
                    node_iter = marker_nodes.createNodeiterator()
                    node = node_iter.next()
                    marker_data = {}
                    while node.isValid():
                        field_cache.setNode(node)
                        name = body_marker_name_field.evaluateString(field_cache)
                        result, values = body_marker_coordinate_field.evaluateReal(field_cache, 3)
                        assert result == RESULT_OK, "Failed to get marker coordinates for" + str(name)
                        marker_data[name] = values
                        node = node_iter.next()
                return marker_data

    return None
