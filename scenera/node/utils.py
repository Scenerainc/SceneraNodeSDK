"""
Helper functions
"""

# pylint: disable=logging-fstring-interpolation
import logging
from .logger import configure_logger
from .validators import ValidationError
from .spec import DataTypeEnumDict

logger = logging.getLogger(__name__)
logger = configure_logger(logger, debug=True)

def get_my_version_number(scenemark):
    """
    Used internally to infer the Node's VersionNumer in the node
    sequence. Which is a +1 from the last object in the list.

    :param scenemark: the SceneMark
    :scenemark type: dictionary
    :return: The Version Number of the Node.
    :rtype: float
    :raises ValidationError: VersionControl is missing or malformed
    """
    try:
        return max([vc_item['VersionNumber']  \
            for vc_item in scenemark['VersionControl']['VersionList']]) + 1.0
    except ValidationError as _e:
        error = "The VersionControl item is missing or malformed"
        logger.exception(error)
        raise ValidationError(error) from _e

def extract_node_datatype_mode(nodesequencer_header):
    """
    Used internally to extract the DataType the Node should work on.

    :param nodesequencer_header: NodeSequencer header structure
    :type nodesequencer_header: dictionary
    :return: DataType, defaults to RGBStill
    :rtype: string
    """
    try:
        datatype_index = nodesequencer_header['NodeInput']['DataTypeMode']
    # We default to using the RGBStill image in case it is not defined
    except Exception as _e:
        logger.warning(f"NodeInput and/or DataTypeMode missing, setting default to RGBStill. ({_e})")
        datatype_index = 1
    datatype_mode = DataTypeEnumDict[datatype_index]
    logger.info(f"DataTypeMode: {datatype_mode}")
    return datatype_mode

def get_regions_of_interest(nodesequencer_header):
    """
    Extracts the polygon from the node input object in a list of lists as follows:

    :Example:

    [ [ (1, 2), (3, 4), (5, 6) ], [ (7, 8), (9, 10), (11, 12), (13, 14), (15, 16) ] ]

    :param nodesequencer_header: NodeSequencer header structure
    :type nodesequencer_header: dictionary
    :return: regions of interest coordinates
    :rtype: a list of lists, containing tuples
    """
    try:
        regions = []
        for polygon in nodesequencer_header['NodeInput']['RegionsOfInterest']:
            region = [(coord['X'],coord['Y']) for coord in polygon['Polygon']]
            if len(region) >= 3:
                regions.append(region)
            else:
                logger.warning(
                    "There is a Region of Interest with fewer than 3 coordinates. Discarding.")
        logger.info(f"Region(s) of Interest: {regions}")
        return regions
    except Exception as _e:
        logger.info(f"Region of Interest missing. Setting to an empty list. ({_e})")
        return []

def get_latest_scenedata_version_number(scenemark):
    """
    Get latest SceneData VersionNumber. This is what the Node should run on.

    :param scenemark: SceneMark structure
    :type scenemark: dictionary
    :return: VersionNumber
    :rtype: float
    """
    try:
        return max([sd_item['VersionNumber'] for sd_item in scenemark['SceneDataList']])
    except ValueError:
        logger.exception("There is no SceneData attached to this SceneMark.")
        return 0.0
