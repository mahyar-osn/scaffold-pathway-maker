from typing import Tuple

from opencmiss.zinc.context import Context
from opencmiss.zinc.region import Region
from opencmiss.zinc.field import Field
from opencmiss.zinc.field import FieldFiniteElement
from opencmiss.zinc.result import RESULT_OK

from opencmiss.utils.zinc.general import ChangeManager
from opencmiss.utils.zinc.field import get_group_list
from opencmiss.utils.zinc.field import find_or_create_field_group


def load(input_scaffold_file: str, name: str) -> Tuple[Region, dict]:
    context = Context(name)
    region = context.getDefaultRegion()
    result = region.readFile(input_scaffold_file)
    assert result == RESULT_OK, "Failed to load scaffold model file" + str(input_scaffold_file)
    groups = _get_scaffold_annotation_groups(region)
    # marker_coordinates = _get_marker_coordinates(region)

    return region, groups


def _discover_coordinate_fields(fm, coordinate_filed=None) -> Field:
    if coordinate_filed:
        field = fm.findFieldByName(coordinate_filed)
    else:
        mesh = get_highest_dimension_mesh()
        element = mesh.createElementiterator().next()
        if element.isValid():
            field_cache = fm.createFieldcache()
            field_cache.setElement(element)
            fielditer = fm.createFielditerator()
            field = fielditer.next()
            while field.isValid():
                if field.isTypeCoordinate() and (field.getNumberOfComponents() == 3) \
                        and (field.castFiniteElement().isValid()):
                    if field.isDefinedAtLocation(field_cache):
                        break
                field = fielditer.next()
            else:
                field = None
    if field:
        _set_model_coordinates_field(field)


def _set_model_coordinates_field(coordinate_filed: Field) -> FieldFiniteElement:
    finite_element_field = coordinate_filed.castFiniteElement()
    assert finite_element_field.isValid() and (finite_element_field.getNumberOfComponents() == 3)
    return finite_element_field


def _get_scaffold_annotation_groups(region: Region):
    field_module = region.getFieldmodule()
    coordinate_field = _discover_coordinate_fields(field_module, coordinate_filed='coordinates')
    return get_group_list(field_module)


def _get_scaffold_marker_groups(region: Region):

    return


def _get_marker_coordinates(region: Region) -> dict:
    field_module = region.getFieldmodule()
    field_cache = field_module.createFieldcache()
    coordinate_field = _discover_coordinate_fields(field_module, coordinate_filed='coordinates')
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
