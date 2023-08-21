from .utils import pascal

def generate_meta_db_attribute_item(
    attribute: str,
    value: str,
    start_time_stamp: str,
    last_time_stamp: str,
    related_track: str,
    probability_of_attribute: float = 1.0,
    ):
    return pascal(locals())

def generate_meta_db_row(
    version: float,
    directional_movement_id: str,
    item_id: str,
    start_time_stamp : str,
    last_time_stamp : str,
    source_node_id: str,
    nice_item_type: str,
    source_node_description: str = "",
    custom_item_type: str = "",
    analysis_description: str = "",
    analysis_id: str = "",
    attributes: list = [],
    related_tracks: list = [],
    related_scene_data: list = [],
    meta: list = [],
    ):
    return pascal(locals())

def generate_event_db_row(
    version: float,
    start_time_stamp: str,
    last_time_stamp: str,
    event_type: str,
    event_category: str,
    processing_status: str = "",
    event_attributes: list = [],
    analysis_id: str = "",
    analysis_description: str = "",
    linked_detected_objects: list = [],
    related_scene_data: list = [],
    meta: list = [],
    ):
    return pascal(locals())

# Sample calls to the functions with parameters and print the results
# print(generate_meta_db_attribute_item("testAttribute", "testValue", "2023-08-01T12:00:00", "2023-08-01T13:00:00", "track123"))
# print(generate_meta_db_row(1.0, "movement123", "item456", "live", "node789", "niceType"))
# print(generate_event_db_row(1.0, "2023-08-01T12:00:00", "2023-08-01T13:00:00", "eventTypeTest", "eventCategoryTest"))
