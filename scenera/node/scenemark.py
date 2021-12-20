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

    Parameters
    ----------
    request : incoming request including a SceneMark and a NodeSequencerAddress
    node_id : string, env variable assigned to the Node through the Developer Portal.
        The Node ID is the unique identifier of the Node.
    event_type : string, env variable assigned to the Node through the Developer Portal.
        The main thing this Node is 'interested in'. Can take a range of values from
        the specification:

        "Custom",\n
        "ItemPresence",\n
        "Loitering",\n
        "Intrusion",\n
        "Falldown",\n
        "Violence",\n
        "Fire",\n
        "Abandonment",\n
        "SpeedGate",\n
        "Xray",\n
        "Facility"

    custom_event_type : string, default "", set when the EventType is set to "Custom"
    analysis_description : string, default "", env variable assigned to the Node
        through the Developer Portal. Used to describe what the analysis is about,
        what it is 'doing'. By default set to an empty string.
    analysis_id : string, default "", env variable assigned to the Node through the Developer Portal.
        Should be a unique identifier refering to the particular algorithm
        used within the node.
    """
    def __init__(
        self,
        request,
        node_id : str,
        event_type : str,
        custom_event_type : str = "",
        analysis_description : str = "",
        analysis_id : str = "",
        ):

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

        Parameters
        ----------
        request_type : string
            "SM" for SceneMark,
            "NS" for the NodeSequencer Address
        name : string
            The name you want to save the json as. Defaults to "scenemark" or
            "nodesequencer_address" based on request_type setting
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

        Parameters
        ----------
        request : the request json
        schema : the (json) schema (found in spec.py)

        Raises
        ------
        ValidationError
            Represents a JSON Schema validation error.
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

        Returns
        -------
        * Float representing the Version Number of the Node.
        """
        try:
            #return self.scenemark['VersionControl']['VersionList'][-1]['VersionNumber'] + 1.0
            return max([vc_item['VersionNumber'] for vc_item in self.scenemark['VersionControl']['VersionList']]) + 1.0
        except:
            raise ValidationError("The VersionControl item is missing or malformed")

    def get_scenedata_datatype_uri_dict(self):
        """
        Creates a dictionary that has the datatype as key, and the uri as value,
        like so:

        Returns
        -------
        * scenedata_data_type_uri_dict : dict of {datatype -> scenedata_uri}

        Example
        -------
        {
            'Thumbnail': https://scenedatauri.example.com/1234_thumb.jpg,
            'RGBStill': https://scenedatauri.example.com/1234_still.jpg,
            'RGBVideo': https://scenedatauri.example.com/1234_vid.mp4,
        }
        """
        return {scenedata_item['DataType']:scenedata_item['SceneDataURI'] \
            for scenedata_item in self.scenemark['SceneDataList']}

    def get_scenedata_id_uri_dict(self):
        """
        Creates a dictionary that has the datatype as key, and the uri as value,
        like so:

        Returns
        -------
        * scenedata_id_uri_dict : dict of {scenedata_id -> scenedata_uri}

        Example
        -------
        {
            'SDT_4f2b308f-851a-43ae-819a-0a255dc194a0_dd37_73ac01': https://scenedatauri.example.com/1234_thumb.jpg,
            'SDT_4f2b308f-851a-43ae-819a-0a255dc194a0_dd37_73ac02': https://scenedatauri.example.com/1234_still.jpg,
            'SDT_4f2b308f-851a-43ae-819a-0a255dc194a0_dd37_73ac03': https://scenedatauri.example.com/1234_vid.mp4,
        }
        """
        return {scenedata_item['SceneDataID']:scenedata_item['SceneDataURI'] \
            for scenedata_item in self.scenemark['SceneDataList']}

    def get_scenedata_uri_list(self, exclude_thumbnail = False):
        """
        Creates a dictionary that has the datatype as key, and the uri as value,
        like so:

        Parameters
        ----------
        exclude_thumbnail : bool, default False
            excludes the 'Thumbnail' DataType from the list

        Returns
        -------
        * scenedata_uri_list : a list of scenedata_uris

        Example
        -------
        [
            https://scenedatauri.example.com/1234_thumb.jpg,
            https://scenedatauri.example.com/1234_still.jpg,
            https://scenedatauri.example.com/1234_vid.mp4
        ]
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

        Parameters
        ----------
        scenedata_uri : string

        Returns / Raises
        ----------------
        * SceneDataID, or a Validation Error "No match" if there is no match.
        """
        for scenedata in self.scenemark['SceneDataList']:
            if scenedata['SceneDataURI'] == uri:
                return scenedata['SceneDataID']
        raise ValidationError("No match found")

    def get_uri_from_id(self, id : str):
        """
        Gets the SceneDataURI of the SceneDataID you put in.

        Parameters
        ----------
        scenedata_id : string

        Returns / Raises
        ----------------
        * SceneDataURI, or a Valiation Error "No match" if there is no match.
        """
        for scenedata in self.scenemark['SceneDataList']:
            if scenedata['SceneDataID'] == id:
                return scenedata['SceneDataURI']
        raise ValidationError("No match found")

    def generate_scenedata_id(self):
        """
        Generates a SceneDataID using the Node ID

        Returns
        -------
        * scenedata_id : string

        Example
        -------
        SDT_9cdff73f-5db1-4e64-9656-ef83bdfeeb90_0001_e4041246
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

        Parameters
        ----------
        xc : int, top-left x coordinate
        yc : int, top-left y coordinate
        height : int, height of the bounding box
        width : int, width of the bounding box

        Returns
        -------
        * A dictionary bounding box object, see example

        Example
        -------
        {
            "XCoordinate": 10,
            "YCoordinate": 30,
            "Height": 400,
            "Width": 400
        }
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

        Parameters
        ----------
        scenedata_id : string

        Returns
        -------
        * SceneDataURI, or "No match" if there is no match.

        Example
        -------
        {
            "VersionNumber": 1.0,
            "Attribute": "Mood",
            "Value": "Anger",
            "ProbabilityOfAttribute": 0.8
        }
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
        Gets the SceneDataURI of the SceneDataID you put in.

        Parameters
        ----------
        nice_item_type : string,
            indicating the NICEITemType found
        related_scenedata_id : string,
            mandatory indication of what item the algorithm ran on
        custom_item_type : string, default "", allows specifying the custom
            NICEItemType
        item_id ; string, default "", indicating an ID on the object, e.g.
            the person's name
        item_type_count : int, default 1, counting the amount of the stated NICEItemType
        probability : float, default 1.0, indicating the confidence on the item
        attributes : list, default [], containing attribute items
        bounding_box : dictionary, default {}, containing the bounding box

        Returns
        -------
        * dictionary containing a DetectedObject item, see example.

        Example:
        --------
        {
            "NICEItemType": "Human",
            "CustomItemType": "",
            "ItemID": "Chris",
            "ItemTypeCount": 1,
            "Probability": 0.93,
            "Attributes": [
                {
                    "VersionNumber": 1.0,
                    "Attribute": "Mood",
                    "Value": "Anger",
                    "ProbabilityOfAttribute": 0.8
                }
            ],
            "BoundingBox": {
                "XCoordinate": 10,
                "YCoordinate": 30,
                "Height": 10,
                "Width": 10
            },
            "RelatedSceneData": "SDT_9cdff73f-5db1-4e64-9656-ef83bdfeeb90_0001_e4041246"
        }
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
        Updates the SceneMark state with the unique analysis list item
        that is added by an AI Node. This could be considered the main
        event of the Node SDKs

        Parameters
        ----------
        processing_status : string, taking one the following values:
            "CustomAnalysis",\n
            "Motion",\n
            "Detected",\n
            "Recognized",\n
            "Characterized",\n
            "Undetected",\n
            "Failed",\n
            "Error"
        custom_event_type : string, default "", set if the above processing status
            equals CustomAnalysis
        total_item_count : int, default 0, total amount of items detected in the scene
        error_message : string, default "", used to propagate errors
        detected_objects : list, default [], of objects, generated
        event_type : string, set internally by the initialization of the scenemark
            object, but may be changed for custom purposes

        Example:
        --------
        {
            "VersionNumber": 1.0,
            "AnalysisID": "9cdff73f-5db1-4e64-9656-ef83bdfeeb90",
            "AnalysisDescription": "Loitering detection",
            "EventType": "Loitering",
            "CustomEventType": "",
            "ProcessingStatus": "Detected",
            "ErrorMessage": "",
            "TotalItemCount": 4,
            "DetectedObjects": [ .. ]
        }

        Contains the list of DetectedObjects item within itself.
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
        image as the thumbnail to be displayed.

        Parameters
        ----------
        scenedata_id : string

        Note
        ----
        Use the Thumbnail id of any existing SceneData, such as a SceneData item
        that you have added yourself.

        Example
        -------
        {
            "VersionNumber": 1.0,
            "SceneDataID": "SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_8a7d01"
        }
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
        Adds a SceneData item to the SceneMark

        Example
        -------
        {
            "VersionNumber": 2.0,
            "SceneDataID": "SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_123456",
            "TimeStamp": "2021-10-29T21:12:17.245Z",
            "SourceNodeID": "83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7",
            "SourceNodeDescription": "Scenera Bridge",
            "Duration": "30",
            "DataType": "RGBVideo",
            "Status": "Upload in Progress",
            "MediaFormat": "H.264",
            "SceneDataURI": "https://sduri.example.com/vid.mp4",
            "Resolution": {
                "Height": 100,
                "Width": 100
            },
            "EmbeddedSceneData": None,
            "Encryption": False
        }

        Parameters
        ----------
        scenedata_uri : string, the uri where the
        datatype : str,
        source_node_description : str = "",
        timestamp : str = "",
        duration : str  = "",
        media_format : str = "",
        encryption : bool = False,
        embedded_scenedata : str = "",
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

        Example:
        --------
        {
            "VersionNumber": 2.0,
            "DateTimeStamp": "2021-07-19T16:25:21.647Z",
            "NodeID": "NodeID"
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

        Parameters
        ----------
        message : a string that is displayed in the app, capped at 200 characters

        """
        assert len(str(message)) <= 200
        self.scenemark['NotificationMessage'] = str(message)

    def return_scenemark_to_ns(self, test = False):
        """
        Returns the SceneMark to the NodeSequencer using the received address

        Parameters
        ----------
        test : bool, default False, if set to True this returns the scenemark
            straight to the caller so you can test the node from Postman or
            some other app

        Returns
        -------
        * SceneMark
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

