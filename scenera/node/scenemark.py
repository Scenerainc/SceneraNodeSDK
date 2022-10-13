# pylint: disable=logging-fstring-interpolation
# pylint: disable=too-many-arguments
"""
This file contains the main SceneMark class and its methods for the Scenera Node SDK.
"""

__author__ = 'Dirk Meulenbelt'
__date__ = '10.05.22'

import datetime
import json
import logging
import random
import requests
import urllib3
from .jwt_decode import validate_jwt_token
from .logger import configure_logger
from .nodesequencer_header_schema import nodesequencer_header_schema
from .scenemark_schema import scenemark_schema
from .spec import (
    EventType,
    NICEItemType,
    ProcessingStatus,
    DataType,
    MediaFormat
)
from .utils import (
    get_my_version_number,
    extract_node_datatype_mode,
    get_regions_of_interest,
    get_latest_scenedata_version_number
    )
from .validators import (
    ValidationError,
    request_json_validator
    )

logger = logging.getLogger(__name__)
logger = configure_logger(logger, debug=True)

# Disable warning for local development
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SceneMark:
    # pylint: disable=too-many-public-methods
    # pylint: disable=too-many-instance-attributes
    """
    This class loads a SceneMark and contains various methods to update the
    SceneMark in the course of Node Processing. It provides various methods
    for retrieving information from, and adding information to, the SceneMark
    data structure.

    :param request: Incoming request including a SceneMark and a NodeSequencerAddress
    :param node_id: Environment variable assigned to the Node through the Developer Portal.
        The Node ID is the unique identifier of the Node.
    :type node_id: string
    :param disable_token_verification: Allows you to turn off the token validation.
    :type disable_token_verification: bool
    """
    def __init__ (
        self,
        request,
        node_id : str,
        disable_token_verification: bool = False,
        ):

        # --- Validation

        # Verify that we get an address to return the SceneMark z
        self.nodesequencer_header = request.json['NodeSequencerHeader']
        if not disable_token_verification:
            validate_jwt_token(self.nodesequencer_header['NodeToken'])
        request_json_validator(
            self.nodesequencer_header,
            nodesequencer_header_schema,
            "NodeSequencer Header"
            )

        # Verify SceneMark input to match the Spec
        self.scenemark = request.json['SceneMark']
        request_json_validator(
            self.scenemark,
            scenemark_schema,
            "SceneMark"
            )

        logger.info(f"Processing SceneMark: {self.scenemark['SceneMarkID']}")

        # --- Set Node Parameters
        self.node_id = node_id
        self.device_id = self.scenemark['SceneMarkID'][41:45]

        # --- Version Control

        # Get the number of the current node in the NodeSequence
        self.my_version_number = get_my_version_number(self.scenemark)

        # Update the version control with the NodeID & TimeStamp
        self.my_timestamp = self.get_current_utc_timestamp()

        # Automatically add a Version Control item to the Node
        self.add_version_control_item()

        # --- Node Objectives

        # Get the DataType the Node works on
        self.node_datatype_mode = extract_node_datatype_mode(self.nodesequencer_header)

        # Get the polygon if there is one.
        self.regions_of_interest = get_regions_of_interest(self.nodesequencer_header)

        # Find the latest scenedata additions
        self.latest_sd_version = get_latest_scenedata_version_number(self.scenemark)

        # Get the targets to work on
        self.targets = self.get_scenedata_uri_list()

        logger.info(f"Working on these items: {self.targets}")

    def save_request(self, request_type : str, name : str):
        """
        Used for development purposes to manually check the request.
        Saves the request as a json to file

        :param request_type: 'SM' for SceneMark, 'NSH' for the NodeSequencerHeader
        :type request_type: string
        :param name: The name you want to save the json as. Defaults to "scenemark" or
            "nodesequencer_header" based on request_type setting
        :type name: string
        """
        assert request_type in ("SM", "NSH")
        if request_type == "SM":
            logger.info(f"Saving SceneMark as '{name}.json'")
            if not name:
                name = "scenemark"
            with open(f"{name}.json", 'w', encoding="utf-8") as json_file:
                json.dump(self.scenemark, json_file)
        elif request_type == "NSH":
            logger.info(f"Saving NodeSequener Header as '{name}.json'")
            if not name:
                name = "nodesequencer_header"
            with open(f"{name}.json", 'w', encoding="utf-8") as json_file:
                json.dump(self.nodesequencer_header, json_file)

    def get_scenedata_uri_list(self):
        """
        Creates a list that contains all the URIs
        like so:

        :Example:

        [\n
            https://scenedatauri.example.com/1234_still.jpg,\n
            https://scenedatauri.example.com/1234_still2.jpg\n
        ]

        :return: List of target SceneData URIs
        :rtype: list
        """
        return [scenedata_item['SceneDataURI'] \
            for scenedata_item in self.scenemark['SceneDataList'] \
                if (scenedata_item['DataType'] == self.node_datatype_mode) and \
                    (scenedata_item['VersionNumber'] == self.latest_sd_version)]

    def get_scenedata_id_uri_dict(self, targets_only = True):
        """
        Creates a dictionary that has the SceneDataID as key, and the SceneDataURI as the value.
        like so:

        :Example:

        {\n
            'SDT_4f2b308f-851a-43ae-819a-0a255dc194a0_dd37_73ac01':\n
                'https://scenedatauri.example.com/1234_thumb.jpg',\n
            'SDT_4f2b308f-851a-43ae-819a-0a255dc194a0_dd37_73ac02':\n
                'https://scenedatauri.example.com/1234_still.jpg',\n
            'SDT_4f2b308f-851a-43ae-819a-0a255dc194a0_dd37_73ac03':\n
                https://scenedatauri.example.com/1234_vid.mp4',\n
        }

        :return: dictionary of {scenedata_id -> scenedata_uri}
        :rtype: dict
        """
        if targets_only:
            return {scenedata_item['SceneDataID']:scenedata_item['SceneDataURI'] \
                for scenedata_item in self.scenemark['SceneDataList'] \
                    if (scenedata_item['DataType'] == self.node_datatype_mode) and \
                        (scenedata_item['VersionNumber'] == self.latest_sd_version)}
        return {scenedata_item['SceneDataID']:scenedata_item['SceneDataURI'] \
            for scenedata_item in self.scenemark['SceneDataList']}

    def get_uri_scenedata_id_dict(self, targets_only = True):
        """
        Creates a dictionary that has the SceneDataURI as the key, and the SceneDataID as the value.
        like so:

        {\n
            'https://scenedatauri.example.com/1234_thumb.jpg':\n
                'SDT_4f2b308f-851a-43ae-819a-0a255dc194a0_dd37_73ac01',\n
            'https://scenedatauri.example.com/1234_still.jpg':\n
                'SDT_4f2b308f-851a-43ae-819a-0a255dc194a0_dd37_73ac02',\n
            'https://scenedatauri.example.com/1234_vid.mp4':\n
                'SDT_4f2b308f-851a-43ae-819a-0a255dc194a0_dd37_73ac03',\n
        }

        :return: dictionary of {scenedata_uri -> scenedata_id}
        :rtype: dict
        """
        if targets_only:
            return {scenedata_item['SceneDataURI']:scenedata_item['SceneDataID'] \
                for scenedata_item in self.scenemark['SceneDataList'] \
                    if (scenedata_item['DataType'] == self.node_datatype_mode) and \
                        (scenedata_item['VersionNumber'] == self.latest_sd_version)}
        return {scenedata_item['SceneDataURI']:scenedata_item['SceneDataID'] \
            for scenedata_item in self.scenemark['SceneDataList']}

    def get_id_from_uri(self, uri : str):
        """
        Gets the SceneDataID of the SceneData piece relating to the URI you put in.

        :param scenedata_uri: Uri to access SceneData
        :type scenedata_uri: string

        :return: SceneDataID corresponding to the URI
        :rtype: string
        """
        for scenedata in self.scenemark['SceneDataList']:
            if scenedata['SceneDataURI'] == uri:
                return scenedata['SceneDataID']
        logger.warning("No SceneData associated with the SceneMark")
        return "No SceneDataID found!"

    def get_uri_from_id(self, scenedata_id : str):
        """
        Gets the SceneDataURI of the SceneDataID you put in.

        :param scenedata_id: SceneDataID
        :type scenedata_id: string

        :return: SceneDataURI corresponding to the ID
        :rtype: string
        :raises ValidationError: "No match" if there isn't a match
        """
        for scenedata in self.scenemark['SceneDataList']:
            if scenedata['SceneDataID'] == scenedata_id:
                return scenedata['SceneDataURI']
        error = "No match found"
        logger.exception(error)
        raise ValidationError(error)

    def get_detected_objects_from_sd_id(self, scenedata_id):
        """
        Creates a list of DetectedObjects that have thge pased
        SceneDataID listed as RelatedSceneData.

        [\n
            {\n
                {\n
                  "NICEItemType": "Human",\n
                  "CustomItemType": "",\n
                  "ItemID": "",\n
                  "ItemTypeCount": 1,\n
                  "Probability": 0.95,\n
                  "Attributes": [\n
                  ],\n
                  "BoundingBox": {\n
                      "XCoordinate": 0.0244,\n
                      "YCoordinate": 0.4522,\n
                      "Height": 0.873,\n
                      "Width": 0.566,\n
                  },\n
                  "RelatedSceneData": "SDT_3c84184e-7a50-449e-af06-dcdf415bebce_c88e_360302"\n
              }\n
            }\n
        ]

        :return: list of DetectedObjects
        :rtype: list
        """
        det_objects = []
        for analysis_list_item in self.scenemark['AnalysisList']:
            for det_object_item in analysis_list_item['DetectedObjects']:
                if det_object_item['RelatedSceneData'] == scenedata_id:
                    det_objects.append(det_object_item)
        return det_objects

    def get_detected_objects_from_sd_uri(self, scenedata_uri):
        """
        Creates a list of DetectedObjects that have the pased
        SceneDataURI's associated ID listed as RelatedSceneData.

        :return: list of DetectedObjects
        :rtype: list
        """
        id = self.get_id_from_uri(scenedata_uri)
        return self.get_detected_objects_from_sd_id(id)

    def generate_scenedata_id(self):
        """
        Generates a SceneDataID using the Node ID

        :Example:

        SDT_9cdff73f-5db1-4e64-9656-ef83bdfeeb90_0001_e4041246

        :return: SceneDataID (see example)
        :rtype: string
        """
        return f"SDT_{self.node_id}_{self.device_id}_{self.generate_random_id(6)}"

    @staticmethod
    def generate_bounding_box(
        x_c : float,
        y_c : float,
        height : float,
        width: float,
        ):
        """
        Generates a Bounding Box using coordinates (from e.g. YOLO)
        Can take both pixels and relative coordinates. The latter is preferred.

        :Example:

        {\n
            "XCoordinate": 0.12,\n
            "YCoordinate": 0.3,\n
            "Height": 0.53,\n
            "Width": 0.39\n
        }

        :param x_c: Top-left x coordinate
        :type x_c: int
        :param y_c: Top-left y coordinate
        :type y_c: int
        :param height: Height of the bounding box
        :type height: int
        :param width: Width of the bounding box
        :type width: int

        :return: A dictionary bounding box object, see example
        :rtype: dict
        """
        assert (isinstance(x_c, float) \
            and isinstance(y_c, float) \
            and isinstance(height, float) \
            and isinstance(width, float)), \
            logger.exception("Arguments need to be integers")

        bounding_box_item = {}
        bounding_box_item['XCoordinate'] = x_c
        bounding_box_item['YCoordinate'] = y_c
        bounding_box_item['Height'] = height
        bounding_box_item['Width'] = width

        return bounding_box_item

    def generate_attribute_item(
        self,
        attribute : str,
        value : str,
        probability_of_attribute : float = 1.0,
        ):
        """
        Generates an Attribute list item, to Specify Attributes found
        associated with the Detected Object.

        :Example:

        {\n
            "VersionNumber": 1.0,\n
            "Attribute": "Mood",\n
            "Value": "Anger",\n
            "ProbabilityOfAttribute": 0.8\n
        }

        :param attribute: Name of the attribute
        :type attribute: string
        :param value: Value of the attribute
        :type value: string
        :param probability_of_attribute: Confidence of the attribute found,
            optional, defaulted to 1.0 == 100%
        :type probability_of_attribute: float

        :return: attribute item
        :rtype: dict

        """
        attribute_item = {}
        attribute_item['VersionNumber'] = self.my_version_number
        attribute_item['Attribute'] = attribute
        attribute_item['Value'] = value
        attribute_item['ProbabilityOfAttribute'] = probability_of_attribute

        logger.info(f"Attribute item of {attribute}:{value} created")
        return attribute_item

    @staticmethod
    def generate_detected_object_item(
        nice_item_type : str,
        related_scenedata_id : str,
        custom_item_type : str = "",
        item_id : str = "",
        item_type_count : int = 1,
        probability : float = 1.0,
        attributes : list = [],
        bounding_box : dict = None,
        ):
        # pylint: disable=dangerous-default-value
        """
        Generates a detected object item

        :Example:

        {\n
            "NICEItemType": "Human",\n
            "CustomItemType": "",\n
            "ItemID": "Chris",\n
            "ItemTypeCount": 1,\n
            "Probability": 0.93,\n
            "Attributes": [\n
                {\n
                    "VersionNumber": 1.0,\n
                    "Attribute": "Mood",\n
                    "Value": "Anger",\n
                    "ProbabilityOfAttribute": 0.8\n
                }\n
            ],\n
            "BoundingBox": {\n
                "XCoordinate": 10,\n
                "YCoordinate": 30,\n
                "Height": 10,\n
                "Width": 10\n
            },\n
            "RelatedSceneData": "SDT_9cdff73f-5db1-4e64-9656-ef83bdfeeb90_0001_e4041246"\n
        }

        :param nice_item_type: Indicating the NICEITemType found
        :type nice_item_type: string
        :param related_scenedata_id: Indication of what item the algorithm ran on
        :type related_scenedata_id: string
        :param custom_item_type: Allows specifying of the custom NICEItemType,
            defaults to "". Optional.
        :type custom_item_type: string
        :param item_id: Indicating an ID on the object.
            E.g. Name of the person Defaults to "". Optional.
        :type item_id: string
        :param item_type_count: Counting the amount of the stated NICEItemType,
            optional, defaults to 1,
        :type item_type_count: int
        :param probability: Indicating the confidence on the item. Optional, defaults to 1.0.
        :type probability: float
        :param attributes: Contains attribute items, defaults to []
        :type attributes: list
        :param bounding_box: Contains the bounding box, defaults to None
        :type bounding_box: dictionary
        :return: dictionary containing a DetectedObject item, see example.
        :rtype: dict
        """

        assert nice_item_type in NICEItemType, \
            logger.exception("This Item Type is not part of the Spec.")

        detected_object = {}
        detected_object['NICEItemType'] = nice_item_type
        detected_object['RelatedSceneData'] = related_scenedata_id
        detected_object['CustomItemType'] = custom_item_type
        detected_object['ItemID'] = item_id
        detected_object['ItemTypeCount'] = item_type_count
        detected_object['Probability'] = probability
        detected_object['Attributes'] = attributes
        detected_object['BoundingBox'] = bounding_box

        logger.info(f"DetectedObjects item of NICEItemType '{nice_item_type}' generated")
        return detected_object

    def add_analysis_list_item(
        self,
        processing_status : str,
        event_type : str,
        custom_event_type : str = "",
        analysis_description : str = "",
        analysis_id : str = "",
        total_item_count : int = 0,
        error_message : str = "",
        detected_objects : list = [],
        ):
        # pylint: disable=dangerous-default-value
        """
        Updates the SceneMark state with the unique analysis list item that is added by an AI Node.
        This could be considered the main event of the Node SDKs. Updates the SceneMark in place.

        :Example:

        {\n
            "VersionNumber": 1.0,\n
            "AnalysisID": "9cdff73f-5db1-4e64-9656-ef83bdfeeb90",\n
            "AnalysisDescription": "Loitering detection",\n
            "EventType": "Loitering",\n
            "CustomEventType": "",\n
            "ProcessingStatus": "Detected",\n
            "ErrorMessage": "",\n
            "TotalItemCount": 4,\n
            "DetectedObjects": [ .. ]\n
        }

        :param processing_status: One the following values: 'CustomAnalysis', 'Motion', 'Detected',
            'Recognized', 'Characterized', 'Undetected', 'Failed', 'Error'
        :type processing_status: string
        :param event_type: Environment variable assigned to the Node through the Developer Portal.
            The main thing this Node is 'interested in'. Can take the following range of values from
            the Specification: 'Custom', 'ItemPresence', Loitering, Intrusion, Falldown, Violence,
            Fire, Abandonment, SpeedGate, Xray, Facility
        :type event_type: string
        :param custom_event_type: Set when EventType is set to 'Custom', defaults to "". Optional
        :type custom_event_type: string
        :param analysis_description: string, default "", env variable assigned to the Node
            through the Developer Portal. Used to describe what the analysis is about,
            what it is 'doing'. By default set to an empty string. Optional.
        :type analysis_description: string
        :param analysis_id: Environment variable assigned to the Node through the Developer Portal.
            Should be a unique identifier refering to the particular algorithm
            used within the node. Defaults to "". Optional.
        :type analysis_id: string
        :param total_item_count: Total amount of items detected in the scene, defaults to 0
        :type total_item_count: int
        :param error_message: Used to propagate errors, optional, defaults to ""
        :type error_message: string
        :param detected_objects: Holds detected objects, defaults to an empty list
        :type detected_objects: list

        :raises AssertionError: When the ProcessingStatus is not recognized as part of the Spec.
        :raises AssertionError: When the EventType is not recognized as part of the Spec.
        """

        assert event_type in EventType, logger.exception("EventType given not in Spec")

        analysis_list_item = {}
        analysis_list_item['VersionNumber'] = self.my_version_number

        assert processing_status in ProcessingStatus, \
            logger.exception("This Processing Status is not part of the Spec.")
        analysis_list_item['ProcessingStatus'] = processing_status

        analysis_list_item['EventType'] = event_type
        analysis_list_item['CustomEventType'] = custom_event_type
        analysis_list_item['AnalysisID'] = analysis_id
        analysis_list_item['AnalysisDescription'] = analysis_description
        analysis_list_item['ErrorMessage'] = str(error_message)
        analysis_list_item['TotalItemCount'] = total_item_count
        analysis_list_item['DetectedObjects'] = detected_objects

        self.scenemark['AnalysisList'].append(analysis_list_item)
        logger.info(f"AnalysisList item of EventType '{event_type}' added")

    def add_thumbnail_list_item(self, scenedata_id : str):
        """
        Adds a new thumbnail list item to the thumbnail list in the SceneMark
        Use this method when you want to instruct the app to use a different
        image as the thumbnail to be displayed. Changes the SceneMark in place.

        :Example:

        {\n
            "VersionNumber": 1.0,\n
            "SceneDataID": "SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_8a7d01"\n
        }

        :param scenedata_id: SceneDataID of the thumbnail
        :type scenedata_id: string

        :Note:

        Use the Thumbnail id of any existing SceneData, such as a SceneData item
        that you have added yourself.
        """
        thumbnail_list_item = {}
        thumbnail_list_item['VersionNumber'] = self.my_version_number
        thumbnail_list_item['SceneDataID'] = scenedata_id

        self.scenemark['ThumbnailList'].append(thumbnail_list_item)
        logger.info(f"Thumbnail set to: {scenedata_id}")

    def add_scenedata_item(
        self,
        scenedata_uri : str,
        datatype : str,
        source_node_description : str = "",
        timestamp : str = "",
        duration : str  = "",
        media_format : str = "",
        encryption : dict = {},
        embedded_scenedata : str = "",
        ):
        # pylint: disable=dangerous-default-value
        """
        Adds a SceneData item to the SceneMark in place.

        :Example:

        {\n
            "VersionNumber": 2.0,\n
            "SceneDataID": "SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_123456",\n
            "TimeStamp": "2021-10-29T21:12:17.245Z",\n
            "SourceNodeID": "83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7",\n
            "SourceNodeDescription": "Scenera Bridge",\n
            "Duration": "30",\n
            "DataType": "RGBVideo",\n
            "Status": "Upload in Progress",\n
            "MediaFormat": "H.264",\n
            "SceneDataURI": "https://sduri.example.com/vid.mp4",\n
            "Resolution": {\n
                "Height": 100,\n
                "Width": 100\n
            },\n
            "EmbeddedSceneData": None,\n
            "Encryption": False\n
        }

        :param scenedata_uri: The URI where we find the image
        :type scenedata_uri: string
        :param datatype:
        :type datatype: string
        :param source_node_description: str = ""
        :type source_node_description: string
        :param timestamp: Timestamp of event, defaults to ""
        :type timestamp: str = "",
        :param duration: Duration of a videoclip, defaults to ""
        :type duration: string
        :param media_format: Format, e.g. H.264
        :type media_format: string
        :param encryption: Encryption on or off, defaults to False
        :type encryption: bool
        :param embedded_scenedata: Embedded scenedata, no idea what this is for to be honest
        :type embedded_scenedata: string
        :raises AssertionError: "No SceneData URI is present."
        :raises AssertionError: "This DataType is not part of the Spec."
        :raises AssertionError: "This Media Format is not part of the Spec."
        """

        scenedata_list_item = {}

        #First, we generate a new id for this new entry
        scenedata_list_item['VersionNumber'] = self.my_version_number
        scenedata_list_item['SceneDataID'] = self.generate_scenedata_id()

        # We update the new item with the URI that you have to provide
        assert scenedata_uri, \
            logger.exception("No SceneData URI is present.")
        scenedata_list_item['SceneDataURI'] = scenedata_uri
        scenedata_list_item['Status'] = "Available at Provided URI"

        # Update the DataType
        assert datatype in DataType, \
            logger.exception("This DataType is not part of the Spec.")
        scenedata_list_item['DataType'] = datatype

        # If the DataType is a thumbnail, we update the ThumbnailList
        if datatype == 'Thumbnail':
            self.add_thumbnail_list_item(scenedata_list_item['SceneDataID'])

        # You are allowed to set your own timestamp but will otherwise take the default
        scenedata_list_item['TimeStamp'] = timestamp if timestamp else self.my_timestamp

        assert media_format in MediaFormat, \
            logger.exception("This Media Format is not part of the Spec.")
        scenedata_list_item['MediaFormat'] = media_format if media_format else 'UNSPECIFIED'

        # This equals the Node ID that is assigned to your node
        scenedata_list_item['SourceNodeID'] = self.node_id
        scenedata_list_item['Encryption'] = encryption

        # The following parameters are all left out unless you specify them.
        scenedata_list_item['SourceNodeDescription'] = source_node_description
        scenedata_list_item['Duration'] = duration
        scenedata_list_item['EmbeddedSceneData'] = embedded_scenedata

        self.scenemark['SceneDataList'].append(scenedata_list_item)
        logger.info(f"SceneData item '{scenedata_list_item['SceneDataID']}' added")

    def update_scenedata_item(self, scenedata_id, key, value):
        """
        Updates existing SceneData pieces, to for example update its VersionNumber

        :param scenedata_id: SceneDataID of the item you want to change
        :param key: the key that needs changing
        :param value: the value that this key should take
        """
        try:
            for sd_item in self.scenemark['SceneDataList']:
                if sd_item['SceneDataID'] == scenedata_id:
                    if sd_item[key]:
                        sd_item_for_change = sd_item
                        break

            sd_item_for_change[key] = value
            logger.info(f"SceneData item '{scenedata_id}' updated: '{key}' set to '{value}'")
        except KeyError as _e:
            error = "Can't update the SceneData item"
            logger.exception(error)
            raise KeyError(error) from _e

    def add_version_control_item(self):
        """
        Adds a Version Control item to the SceneMark. Uses already existing
        data and is called automatically by the __init__ method

        :Example:

        {\n
            "VersionNumber": 2.0,\n
            "DateTimeStamp": "2021-07-19T16:25:21.647Z",\n
            "NodeID": "NodeID"\n
        }
        """
        version_list_item = {}
        version_list_item['VersionNumber'] = self.my_version_number
        version_list_item['DateTimeStamp'] = self.my_timestamp
        version_list_item['NodeID'] = self.node_id

        self.scenemark['VersionControl']['VersionList'].append(version_list_item)

    def add_custom_notification_message(self, message : str):
        """
        Adds a custom notification message to the SceneMark to display in the notification

        :param message: Text for the body of the push notification, capped at 200 characters
        :type message: string
        """
        assert len(str(message)) <= 200, logger.exception("Custom message exceeds 200 chars")
        self.scenemark['NotificationMessage'] = str(message)
        logger.info("Custom push notififation message added")

    def return_scenemark_to_ns(self, test = False, load_test = False):
        # pylint: disable=inconsistent-return-statements
        """
        Returns the SceneMark to the NodeSequencer with an HTTP call using the received address

        :param test: If set to True this returns the scenemark
            straight to the caller so you can test the node from Postman or
            some other app, defaults to False
        :type test: bool
        """

        # Update our original request with the updated SceneMark
        request_json_validator(self.scenemark, scenemark_schema, "SceneMark schema")

        scenemark = json.dumps(self.scenemark)
        if test:
            logger.info("Sending the SceneMark back directly")
            return scenemark

        if load_test:
            logger.info("Load Test: Doing nothing with the resulting SceneMark")
            return {}, 200

        # We add the token to the HTTP header.
        ns_header = {'Authorization': 'Bearer ' + self.nodesequencer_header['Token'],
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'}

        verify = True if self.nodesequencer_header['Ingress'].startswith("https") else False

        # Call NodeSequencer with an updated SceneMark
        answer = requests.post(
            self.nodesequencer_header['Ingress'],
            data=scenemark,
            headers=ns_header,
            verify=verify,
            stream=False)
        logger.info(f"Returned SceneMark to NodeSequencer: {answer}")

    # Helper Functions
    @staticmethod
    def get_current_utc_timestamp():
        """
        Helper function to create a UTC timestamp in the required format.

        :Example:
        '2022-03-14T15:43:04.010Z'

        """
        time = str(datetime.datetime.utcnow())
        time = time[:-3]
        time = time.replace(" ","T")
        time = time + "Z"
        return time

    @staticmethod
    def generate_random_id(length):
        """
        Helper function to create a random ID
        """
        return ''.join([random.choice('0123456789abcdefghijklmnopqrstuvwxyz') \
            for _ in range(length)])
