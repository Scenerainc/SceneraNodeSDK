"""
This filecontains the main SceneMark class and its methods for the Scenera Node SDK.
"""

__author__ = 'Dirk Meulenbelt'
__date__ = '09.11.21'

from .spec import *
import json
import jsonschema
import requests
import datetime
import random

class ValidationError(Exception):
    """
    Self-defined error to raise when the values do not match.
    """
    def __init__(self, msg):
        self.msg = msg

class SceneMark:
    """
    This class loads a SceneMark and contains various methods to update the
    SceneMark in the course of Node Processing. It provides various methods
    for retrieving information from, and adding information to, the SceneMark
    data structure.

    :param request: Incoming request including a SceneMark and a NodeSequencerAddress
    :param node_id: Environment variable assigned to the Node through the Developer Portal.
        The Node ID is the unique identifier of the Node.
    :type node_id: string
    :param event_type: Environment variable assigned to the Node through the Developer Portal.
        The main thing this Node is 'interested in'. Can take the following range of values from
        the specification: 'Custom', 'ItemPresence', Loitering, Intrusion, Falldown, Violence, Fire,
        Abandonment, SpeedGate, Xray, Facility
    :type event_type: string
    :param custom_event_type: Set when the EventType is set to 'Custom', defaults to "". Optional
    :type custom_event_type: string
    :param analysis_description: string, default "", env variable assigned to the Node
        through the Developer Portal. Used to describe what the analysis is about,
        what it is 'doing'. By default set to an empty string. Optional.
    :type analysis_description: string
    :param analysis_id: Environment variable assigned to the Node through the Developer Portal.
        Should be a unique identifier refering to the particular algorithm
        used within the node. Defaults to "". Optional.
    :type analysis_id: string
    """
    def __init__ (
        self,
        request,
        node_id : str,
        event_type : str,
        custom_event_type : str = "",
        analysis_description : str = "",
        analysis_id : str = "",
        ):
        """
        Constructor method
        """
        # Verify SceneMark input to match the spec
        self.scenemark = request.json['SceneMark']
        self.request_json_validator(self.scenemark, SceneMarkSchema)

        # Verify that we get an address to return the SceneMark z
        self.nodesequencer_address = request.json['NodeSequencerAddress']
        self.request_json_validator(self.nodesequencer_address, NodesequencerAddressSchema)

        # Set assigned node parameters
        self.node_id = node_id
        assert event_type in EventType, "EventType given not in spec"
        self.event_type = event_type
        self.custom_event_type = custom_event_type
        self.analysis_description = analysis_description
        self.analysis_id = analysis_id

        # Get the number of the current node in the NodeSequence
        self.my_version_number = self.get_my_version_number()

        # Update the version control with the NodeID & TimeStamp
        self.my_timestamp = self.get_current_utc_timestamp()
        self.add_version_control_item()

    def save_request(self, request_type : str, name : str):
        """
        Used for development purposes to manually check the request.
        Saves the request as a json to file

        :param request_type: 'SM' for SceneMark, 'NS' for the NodeSequencer Address
        :type request_type: string
        :param name: The name you want to save the json as. Defaults to "scenemark" or
            "nodesequencer_address" based on request_type setting
        :type name: string
        """
        assert request_type in ("SM", "NS")
        if request_type == "SM":
            if not name:
                name = "scenemark"
            with open(f"{name}.json", 'w') as json_file:
                json.dump(self.scenemark, json_file)
        elif request_type == "NS":
            if not name:
                name = "nodesequencer_address"
            with open(f"{name}.json", 'w') as json_file:
                json.dump(self.nodesequencer_address, json_file)

    def request_json_validator(self, request, schema):
        """
        Used internally to validate incoming and outgoing requests.

        :param request: the request json
        :type request: json
        :param schema: the schema found in the spec
        :type schema: json
        :raises ValidationError: Represents a JSON Schema validation error.
        """
        try:
            jsonschema.validate(instance = request, schema = schema)
        except jsonschema.exceptions.ValidationError as e:
            raise jsonschema.exceptions.ValidationError(e.message)
        return True

    def get_my_version_number(self):
        """
        Used internally to infer the Node's VersionNumer in the node
        sequence. Which is a +1 from the last object in the list.

        :return: The Version Number of the Node.
        :rtype: float
        :raises ValidationError: VersionControl is missing or malformed
        """
        try:
            return max([vc_item['VersionNumber'] for vc_item in self.scenemark['VersionControl']['VersionList']]) + 1.0
        except:
            raise ValidationError("The VersionControl item is missing or malformed")

    def get_scenedata_datatype_uri_dict(self):
        """
        Creates a dictionary that has the datatype as key, and the uri as value,
        like so:

        :Example:

        {\n
        'Thumbnail': https://scenedatauri.example.com/1234_thumb.jpg,\n
        'RGBStill': https://scenedatauri.example.com/1234_still.jpg,\n
        'RGBVideo': https://scenedatauri.example.com/1234_vid.mp4,\n
        }

        :return: dictionary of {datatype -> scenedata_uri}
        :rtype: dict
        """
        return {scenedata_item['DataType']:scenedata_item['SceneDataURI'] \
            for scenedata_item in self.scenemark['SceneDataList']}

    def get_scenedata_id_uri_dict(self):
        """
        Creates a dictionary that has the datatype as key, and the uri as value,
        like so:

        :Example:

        {\n
            'SDT_4f2b308f-851a-43ae-819a-0a255dc194a0_dd37_73ac01': https://scenedatauri.example.com/1234_thumb.jpg,\n
            'SDT_4f2b308f-851a-43ae-819a-0a255dc194a0_dd37_73ac02': https://scenedatauri.example.com/1234_still.jpg,\n
            'SDT_4f2b308f-851a-43ae-819a-0a255dc194a0_dd37_73ac03': https://scenedatauri.example.com/1234_vid.mp4,\n
        }

        :return: dictionary of {scenedata_id -> scenedata_uri}
        :rtype: dict
        """
        return {scenedata_item['SceneDataID']:scenedata_item['SceneDataURI'] \
            for scenedata_item in self.scenemark['SceneDataList']}

    def get_scenedata_uri_list(self, exclude_thumbnail = False):
        """
        Creates a list that contains all the URIs
        like so:

        :Example:

        [\n
            https://scenedatauri.example.com/1234_thumb.jpg,\n
            https://scenedatauri.example.com/1234_still.jpg,\n
            https://scenedatauri.example.com/1234_vid.mp4\n
        ]

        :param exclude_thumbnail: Excludes the 'Thumbnail' DataType from the list, defaults to False. Optional.
        :type exclude_thumbnail: bool

        :return: List of SceneData URIs
        :rtype: list
        """
        if exclude_thumbnail:
            return [scenedata_item['SceneDataURI'] \
                for scenedata_item in self.scenemark['SceneDataList'] \
                    if scenedata_item['DataType'] != 'Thumbnail']
        else:
            return [scenedata_item['SceneDataURI'] \
                for scenedata_item in self.scenemark['SceneDataList']]

    def get_id_from_uri(self, uri : str):
        """
        Gets the SceneDataID of the SceneData piece relating to the URI you put in.

        :param scenedata_uri: Uri to access SceneData
        :type scenedata_uri: string

        :return: SceneDataID corresponding to the URI
        :rtype: string
        :raises ValidationError: "No match" if there isn't a match
        """
        for scenedata in self.scenemark['SceneDataList']:
            if scenedata['SceneDataURI'] == uri:
                return scenedata['SceneDataID']
        raise ValidationError("No match found")

    def get_uri_from_id(self, id : str):
        """
        Gets the SceneDataURI of the SceneDataID you put in.

        :param scenedata_id: SceneDataID
        :type scenedata_id: string

        :return: SceneDataURI corresponding to the ID
        :rtype: string
        :raises ValidationError: "No match" if there isn't a match
        """
        for scenedata in self.scenemark['SceneDataList']:
            if scenedata['SceneDataID'] == id:
                return scenedata['SceneDataURI']
        raise ValidationError("No match found")

    def generate_scenedata_id(self):
        """
        Generates a SceneDataID using the Node ID

        :Example:

        SDT_9cdff73f-5db1-4e64-9656-ef83bdfeeb90_0001_e4041246

        :return: SceneDataID (see example)
        :rtype: string
        """
        return f"SDT_{self.node_id}_0001_{self.generate_random_id(6)}"

    def generate_bounding_box(
        self,
        xc : int,
        yc : int,
        height : int,
        width: int,
        ):
        """
        Generates a Bounding Box using coordinates (from e.g. YOLO)

        :Example:

        {\n
            "XCoordinate": 10,\n
            "YCoordinate": 30,\n
            "Height": 400,\n
            "Width": 400\n
        }

        :param xc: Top-left x coordinate
        :type xc: int
        :param yc: Top-left y coordinate
        :type yc: int
        :param height: Height of the bounding box
        :type height: int
        :param width: Width of the bounding box
        :type width: int

        :return: A dictionary bounding box object, see example
        :rtype: dict
        """
        assert (type(xc) == type(yc) == type(height) == type(width) == int), \
            "Arguments need to be integers"

        bounding_box_item = {}
        bounding_box_item['XCoordinate'] = xc
        bounding_box_item['YCoordinate'] = yc
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
        Generates an Attribute list item, to specify Attributes found
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
        :param probability_of_attribute: Confidence of the attribute found, optional, defaulted to 1.0 == 100%
        :type probability_of_attribute: float

        :return: attribute item
        :rtype: dict

        """
        attribute_item = {}
        attribute_item['VersionNumber'] = self.my_version_number
        attribute_item['Attribute'] = attribute
        attribute_item['Value'] = value
        attribute_item['ProbabilityOfAttribute'] = probability_of_attribute

        return attribute_item

    def generate_detected_object_item(
        self,
        nice_item_type : str,
        related_scenedata_id : str,
        custom_item_type : str = "",
        item_id : str = "",
        item_type_count : int = 1,
        probability : float = 1.0,
        attributes : list = [],
        bounding_box : dict = None,
        ):
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
        :param custom_item_type: Allows specifying of the custom NICEItemType, defaults to "". Optional.
        :type custom_item_type: string
        :param item_id: Indicating an ID on the object. E.g. Name of the person Defaults to "". Optional.
        :type item_id: string
        :param item_type_count: Counting the amount of the stated NICEItemType, optional, defaults to 1,
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
        assert nice_item_type in NICEItemType, "This Item Type is not part of the spec."

        detected_object = {}
        detected_object['NICEItemType'] = nice_item_type
        detected_object['RelatedSceneData'] = related_scenedata_id
        detected_object['CustomItemType'] = custom_item_type
        detected_object['ItemID'] = item_id
        detected_object['ItemTypeCount'] = item_type_count
        detected_object['Probability'] = probability
        detected_object['Attributes'] = attributes
        detected_object['BoundingBox'] = bounding_box

        return detected_object

    def add_analysis_list_item(
        self,
        processing_status,
        custom_event_type : str = "",
        total_item_count : int = 0,
        error_message : str = "",
        detected_objects : list = [],
        event_type : str = "",
        ):
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
        :param custom_event_type: Define your event when your EventType is 'Custom'
        :type custom_event_type: string
        :param total_item_count: Total amount of items detected in the scene, defaults to 0
        :type total_item_count: int
        :param error_message: Used to propagate errors, optional, defaults to ""
        :type error_message: string
        :param detected_objects: Holds detected objects, defaults to an empty list
        :type detected_objects: list
        :param event_type: Set internally by the constructor, but may be altered for custom purposes. Optional.
        :type event_type: string

        :raises AssertionError: When the ProcessingStatus is not recognized as part of the spec.
        :raises AssertionError: When the EventType is not recognized as part of the spec.
        """
        analysis_list_item = {}
        analysis_list_item['VersionNumber'] = self.my_version_number

        assert processing_status in ProcessingStatus, \
            "This Processing Status is not part of the spec."
        analysis_list_item['ProcessingStatus'] = processing_status

        if event_type:
            assert event_type in EventType, \
            "This Event Type is not part of the spec."
            analysis_list_item['EventType'] = event_type
        else:
            analysis_list_item['EventType'] = self.event_type

        if custom_event_type:
            analysis_list_item['CustomEventType'] = custom_event_type
        else:
            analysis_list_item['CustomEventType'] = self.custom_event_type

        analysis_list_item['AnalysisID'] = self.analysis_id
        analysis_list_item['AnalysisDescription'] = self.analysis_description
        analysis_list_item['ErrorMessage'] = str(error_message)
        analysis_list_item['TotalItemCount'] = total_item_count
        analysis_list_item['DetectedObjects'] = detected_objects

        self.scenemark['AnalysisList'].append(analysis_list_item)

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

    def add_scenedata_item(
        self,
        scenedata_uri : str,
        datatype : str,
        source_node_description : str = "",
        timestamp : str = "",
        duration : str  = "",
        media_format : str = "",
        encryption : bool = False,
        embedded_scenedata : str = "",
        ):
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
        :raises AssertionError: "This DataType is not part of the spec."
        :raises AssertionError: "This Media Format is not part of the spec."
        """

        scenedata_list_item = {}

        #First, we generate a new id for this new entry
        scenedata_list_item['VersionNumber'] = self.my_version_number
        scenedata_list_item['SceneDataID'] = self.generate_scenedata_id()

        # We update the new item with the URI that you have to provide
        assert scenedata_uri, \
            "No SceneData URI is present."
        scenedata_list_item['SceneDataURI'] = scenedata_uri
        scenedata_list_item['Status'] = "Available at Provided URI"

        # Update the DataType
        assert datatype in DataType, \
            "This DataType is not part of the spec."
        scenedata_list_item['DataType'] = datatype

        # If the DataType is a thumbnail, we update the ThumbnailList
        if datatype == 'Thumbnail':
            self.add_thumbnail_list_item(scenedata_list_item['SceneDataID'])

        # You are allowed to set your own timestamp but will otherwise take the default
        scenedata_list_item['TimeStamp'] = timestamp if timestamp else self.my_timestamp

        assert media_format in MediaFormat, \
            "This Media Format is not part of the spec."
        scenedata_list_item['MediaFormat'] = media_format if media_format else 'UNSPECIFIED'

        # This equals the Node ID that is assigned to your node
        scenedata_list_item['SourceNodeID'] = self.node_id
        scenedata_list_item['Encryption'] = encryption

        # The following parameters are all left out unless you specify them.
        scenedata_list_item['SourceNodeDescription'] = source_node_description
        scenedata_list_item['Duration'] = duration
        scenedata_list_item['EmbeddedSceneData'] = embedded_scenedata

        self.scenemark['SceneDataList'].append(scenedata_list_item)

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
        assert len(str(message)) <= 200
        self.scenemark['NotificationMessage'] = str(message)

    def return_scenemark_to_ns(self, test = False):
        """
        Returns the SceneMark to the NodeSequencer with an HTTP call using the received address

        :param test: If set to True this returns the scenemark
            straight to the caller so you can test the node from Postman or
            some other app, defaults to False
        :type test: bool
        """
        # Update our original request with the updated SceneMark
        self.request_json_validator(self.scenemark, SceneMarkSchema)

        scenemark = json.dumps(self.scenemark)
        if test:
            return scenemark

        # We add the token to the HTTP header.
        ns_header = {'Authorization': 'Bearer ' + self.nodesequencer_address['Token'],
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'}

        verify = False
        if self.nodesequencer_address['Ingress'].startswith("https"):
            verify = True

        # Call NodeSequencer with an updated SceneMark
        answer = requests.post(
            self.nodesequencer_address['Ingress'],
            data=scenemark,
            headers=ns_header,
            verify=verify,
            stream=False)
        print("Returning to Node Sequencer", answer)

    # Helper Functions
    def get_current_utc_timestamp(self):
        """
        Helper function to create a UTC timestamp in the required format.
        """
        return f"{'{:%Y-%m-%dT%H:%M:%S.%f}'.format(datetime.datetime.utcnow())[:-3]}Z"

    def generate_random_id(self, length):
        """
        Helper function to create a random ID
        """
        return ''.join([random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for n in range(length)])

