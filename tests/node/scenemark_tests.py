"""
Unit-tests for the Node AI SDK
"""

import unittest
import jsonschema
from scenera.node import SceneMark, spec
from scenera.node.validators import ValidationError
from scenera.node.utils import (
    extract_node_datatype_mode,
    get_latest_scenedata_version_number,
    get_my_version_number,
    get_regions_of_interest
    )

class SceneMarkTestCase(unittest.TestCase):

    def setUp(self):
        self.sm = SceneMark(
            Request(),
            node_id = "unit_test_node",
            disable_token_verification = True
        )

    def test_internal_settings(self):
        self.assertEqual(self.sm.node_id, "unit_test_node")

    def incorrect_scenemark_json_raises_error(self):
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            self.sm.request_json_validator(
                {"Some_incorrect_schema": "fails"},
                spec.SceneMarkSchema)

    def correct_scenemark_json_passes(self):
        self.assertTrue(
            self.sm.request_json_validator(
                self.sm.scenemark,
                spec.Spec.SceneMarkSchema))

    def incorrect_nodesequencer_address_json_raises_error(self):
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            self.sm.request_json_validator(
                {"Some_incorrect_schema": "fails"},
                spec.Spec.NodesequencerAddressSchema)

    def correct_nodesequencer_address_json_passes(self):
        self.assertTrue(
            self.sm.request_json_validator(
                self.sm.nodesequencer_address,
                spec.Spec.NodesequencerAddressSchema))

    def test_get_my_version_number(self):
        # Set to 4.0 because the initialisation has already
        # updated the VersionControl
        self.assertEqual(get_my_version_number(self.sm.scenemark), 4.0)

        #This can be left at 3.0 because it's the class attribute
        self.assertEqual(self.sm.my_version_number, 3.0)

    def test_extract_node_datatype_mode(self):
        self.assertEqual(extract_node_datatype_mode(self.sm.nodesequencer_header), 'RGBVideo')

    def test_extra_node_datatype_mode_missing_setting(self):
        self.sm.nodesequencer_header['NodeInput'] = {}
        self.assertEqual(extract_node_datatype_mode(self.sm.nodesequencer_header), 'RGBStill')

    def test_get_regions_of_interest(self):
        regions_of_interest = [
            [(0.1, 0.2),(0.3, 0.4),(0.5, 0.6)],
            [(0.7, 0.8),(0.9, 0.10),(0.11, 0.12),(0.13,0.14),(0.15,0.16),(0.17,0.18)]
            ]
        self.assertEqual(regions_of_interest, get_regions_of_interest(self.sm.nodesequencer_header))

    def test_get_latest_scenedata_version_number(self):
        self.assertEqual(get_latest_scenedata_version_number(self.sm.scenemark), 2.0)

    def test_get_scenedata_id_to_uri_dict(self):
        sd_id_uri_dict = self.sm.get_scenedata_id_uri_dict(targets_only=False)
        self.assertEqual(
            sd_id_uri_dict['SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_8a7d01'],
            'https://sduri.example.com/thumb.jpg')
        self.assertEqual(
            sd_id_uri_dict['SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_4ef702'],
            'https://sduri.example.com/still.jpg')
        self.assertEqual(
            sd_id_uri_dict['SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_80f203'],
            'https://sduri.example.com/vid.mp4')
        self.assertEqual(
            sd_id_uri_dict['SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_80f205'],
            'https://sduri.example.com/vid2.mp4')

    def test_get_scenedata_id_to_uri_dict_only_target(self):
        self.sm.node_datatype_mode = "RGBVideo"
        sd_id_uri_dict = self.sm.get_scenedata_id_uri_dict(targets_only=True)
        self.assertEqual(
            sd_id_uri_dict['SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_80f205'],
            'https://sduri.example.com/vid2.mp4')
        with self.assertRaises(KeyError):
            _ = sd_id_uri_dict['SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_8a7d01']
        with self.assertRaises(KeyError):
            _ = sd_id_uri_dict['SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_4ef702']

    def test_get_uri_scenedata_id_dict(self):
        sd_id_uri_dict = self.sm.get_uri_scenedata_id_dict(targets_only=False)
        self.assertEqual(
            sd_id_uri_dict['https://sduri.example.com/thumb.jpg'],
            'SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_8a7d01')
        self.assertEqual(
            sd_id_uri_dict['https://sduri.example.com/still.jpg'],
            'SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_4ef702')
        self.assertEqual(
            sd_id_uri_dict['https://sduri.example.com/vid.mp4'],
            'SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_80f203')
        self.assertEqual(
            sd_id_uri_dict['https://sduri.example.com/vid2.mp4'],
            'SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_80f205')

    def test_get_uri_scenedata_id_dict_only_target(self):
        sd_id_uri_dict = self.sm.get_uri_scenedata_id_dict(targets_only=True)
        with self.assertRaises(KeyError):
            _ = sd_id_uri_dict['https://sduri.example.com/thumb.jpg']
        with self.assertRaises(KeyError):
            _ = sd_id_uri_dict['https://sduri.example.com/still.jpg']
        self.assertEqual(
            sd_id_uri_dict['https://sduri.example.com/vid2.mp4'],
            'SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_80f205')

    def test_get_scenedata_uri_list(self):
        self.sm.node_datatype_mode = "RGBStill"
        uri_list = self.sm.get_scenedata_uri_list()
        self.assertEqual(uri_list[0], 'https://sduri.example.com/still2.jpg')

    def test_get_id_from_uri(self):
        thumb = self.sm.get_id_from_uri('https://sduri.example.com/thumb.jpg')
        still = self.sm.get_id_from_uri('https://sduri.example.com/still.jpg')
        vid = self.sm.get_id_from_uri('https://sduri.example.com/vid.mp4')
        self.assertEqual(thumb, 'SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_8a7d01')
        self.assertEqual(still, 'SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_4ef702')
        self.assertEqual(vid, 'SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_80f203')
        with self.assertRaises(ValidationError):
            self.sm.get_uri_from_id("wrong URI")

    def test_get_uri_from_id(self):
        thumb = self.sm.get_uri_from_id('SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_8a7d01')
        still = self.sm.get_uri_from_id('SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_4ef702')
        vid = self.sm.get_uri_from_id('SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_80f203')
        self.assertEqual(thumb, 'https://sduri.example.com/thumb.jpg')
        self.assertEqual(still, 'https://sduri.example.com/still.jpg')
        self.assertEqual(vid, 'https://sduri.example.com/vid.mp4')
        with self.assertRaises(ValidationError):
            self.sm.get_uri_from_id("wrong ID")

    def test_generate_scenedata_id(self):
        ref = f"SDT_{self.sm.node_id}_{self.sm.device_id}_{self.sm.generate_random_id(6)}"
        sd_id = self.sm.generate_scenedata_id()
        self.assertEqual(ref[:23], sd_id[:23])

    def test_generate_bounding_box(self):
        bounding_box = self.sm.generate_bounding_box(0.1,0.2,0.3,0.4)
        self.assertEqual(bounding_box['XCoordinate'], 0.1)
        self.assertEqual(bounding_box['YCoordinate'], 0.2)
        self.assertEqual(bounding_box['Height'], 0.3)
        self.assertEqual(bounding_box['Width'], 0.4)

    def test_generate_bounding_box_wrong_datatype_fail(self):
        with self.assertRaises(AssertionError):
            _ = self.sm.generate_bounding_box('1','2','3','4')

    def test_generate_attribute_item(self):
        attribute_item = self.sm.generate_attribute_item(
            attribute = 'some-attribute',
            value = 'some-value',
            probability_of_attribute = 0.90
        )
        self.assertEqual(attribute_item['VersionNumber'],
            self.sm.my_version_number)
        self.assertEqual(attribute_item['Attribute'], 'some-attribute')
        self.assertEqual(attribute_item['Value'], 'some-value')
        self.assertEqual(attribute_item['ProbabilityOfAttribute'], 0.90)

    def test_generate_detected_object_item(self):
        detected_object = self.sm.generate_detected_object_item(
            'Human',
            'scenedata-id',
            'custom-item-type',
            'item-id',
            3,
            0.3,
            [self.sm.generate_attribute_item('mood', 'anger', 0.82)],
            self.sm.generate_bounding_box(0.1,0.2,0.3,0.4)
        )
        self.assertEqual(detected_object['NICEItemType'],'Human')
        self.assertEqual(detected_object['RelatedSceneData'],'scenedata-id')
        self.assertEqual(detected_object['CustomItemType'], 'custom-item-type')
        self.assertEqual(detected_object['ItemID'], 'item-id')
        self.assertEqual(detected_object['ItemTypeCount'], 3)
        self.assertEqual(detected_object['Probability'], 0.3)
        self.assertEqual(detected_object['Attributes'][0]['VersionNumber'],
            self.sm.my_version_number)
        self.assertEqual(detected_object['Attributes'][0]['Attribute'], 'mood')
        self.assertEqual(detected_object['Attributes'][0]['Value'], 'anger')
        self.assertEqual(detected_object['Attributes'][0]['ProbabilityOfAttribute'],
            0.82)
        self.assertEqual(detected_object['BoundingBox']['XCoordinate'],0.1)
        self.assertEqual(detected_object['BoundingBox']['YCoordinate'],0.2)
        self.assertEqual(detected_object['BoundingBox']['Height'],0.3)
        self.assertEqual(detected_object['BoundingBox']['Width'],0.4)

    def test_generate_detected_object_item_fail_false_item_type(self):
        with self.assertRaises(AssertionError):
            _ = self.sm.generate_detected_object_item(
            'IncorrectItemType',
            'scenedata-id',
            'custom-item-type',
            'item-id',
            3,
            0.3,
            [self.sm.generate_attribute_item('mood', 'anger', 0.82)],
            self.sm.generate_bounding_box(1,2,3,4)
            )

    def test_add_analysis_list_item(self):
        self.sm.add_analysis_list_item(
            'Detected',
            'Custom',
            'custom-event-type',
            'a-descr',
            'a-id',
            4,
            'some error happened',
            ['filler'],
        )
        self.assertEqual(self.sm.scenemark['AnalysisList'][-1]['VersionNumber'],
            self.sm.my_version_number)
        self.assertEqual(self.sm.scenemark['AnalysisList'][-1]['ProcessingStatus'], 'Detected')
        self.assertEqual(self.sm.scenemark['AnalysisList'][-1]['CustomEventType'],
            'custom-event-type')

        self.assertEqual(self.sm.scenemark['AnalysisList'][-1]['AnalysisDescription'], 'a-descr')
        self.assertEqual(self.sm.scenemark['AnalysisList'][-1]['AnalysisID'], 'a-id')

        self.assertEqual(self.sm.scenemark['AnalysisList'][-1]['TotalItemCount'], 4)
        self.assertEqual(self.sm.scenemark['AnalysisList'][-1]['ErrorMessage'],
            'some error happened')
        self.assertEqual(self.sm.scenemark['AnalysisList'][-1]['DetectedObjects'], ['filler'])

    def test_add_analysis_list_item_false_processing_status(self):
        with self.assertRaises(AssertionError):
            self.sm.add_analysis_list_item(
                'IncorrectProcessingStatus',
                'custom-event-type',
                4,
                'some error happened',
                [],
                'Loitering'
                )

    def test_add_analysis_list_item_false_event_type(self):
        with self.assertRaises(AssertionError):
            self.sm.add_analysis_list_item(
                'Detected',
                'custom-event-type',
                4,
                'some error happened',
                [],
                'IncorrectEventType'
                )

    def test_update_scendata_item(self):
        self.sm.update_scenedata_item("SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_8a7d01", "VersionNumber", 4.0)
        self.assertEqual(self.sm.scenemark['SceneDataList'][0]['VersionNumber'], 4.0)

    def test_update_scenedata_item_wrong_key_value(self):
        with self.assertRaises(KeyError):
            self.sm.update_scenedata_item(
                "SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_8a7d01",
                "Lalala",
                "Lololo")

    def test_add_thumbnail_list_item(self):
        self.sm.add_thumbnail_list_item('some-scenedata-id')
        self.assertEqual(self.sm.scenemark['ThumbnailList'][-1]['VersionNumber'],
            self.sm.my_version_number)
        self.assertEqual(self.sm.scenemark['ThumbnailList'][-1]['SceneDataID'],
            'some-scenedata-id')

    def test_add_scenedata_item(self):
        self.sm.add_scenedata_item(
            'some-uri',
            'RGBStill',
            'source-node-description',
            'sometimestamp',
            '30',
            'JPEG',
            False,
            'some-embedded-scenedata-id')
        self.assertEqual(self.sm.scenemark['SceneDataList'][-1]['VersionNumber'],
            self.sm.my_version_number)
        self.assertTrue(self.sm.scenemark['SceneDataList'][-1]['SceneDataID'])
        self.assertEqual(self.sm.scenemark['SceneDataList'][-1]['SceneDataURI'],
            'some-uri')
        self.assertEqual(self.sm.scenemark['SceneDataList'][-1]['DataType'],
            'RGBStill')
        self.assertEqual(self.sm.scenemark['SceneDataList'][-1]['SourceNodeDescription'],
            'source-node-description')
        self.assertEqual(self.sm.scenemark['SceneDataList'][-1]['TimeStamp'],
            'sometimestamp')
        self.assertEqual(self.sm.scenemark['SceneDataList'][-1]['Duration'],
            '30')
        self.assertEqual(self.sm.scenemark['SceneDataList'][-1]['MediaFormat'],
            'JPEG')
        self.assertEqual(self.sm.scenemark['SceneDataList'][-1]['SourceNodeID'],
            self.sm.node_id)
        self.assertEqual(self.sm.scenemark['SceneDataList'][-1]['Encryption'],
            False)
        self.assertEqual(self.sm.scenemark['SceneDataList'][-1]['EmbeddedSceneData'],
            'some-embedded-scenedata-id')

    def test_add_scenedata_item_wrong_datatype(self):
        with self.assertRaises(AssertionError):
            self.sm.add_scenedata_item(
                'some-uri',
                'WrongDataType',
                'source-node-description',
                'sometimestamp',
                '30',
                'JPEG',
                False,
                'some-embedded-scenedata-id')

    def test_add_scenedata_item_wrong_media_format(self):
        with self.assertRaises(AssertionError):
            self.sm.add_scenedata_item(
                'some-uri',
                'RGBStill',
                'source-node-description',
                'sometimestamp',
                '30',
                'WrongMediaFormat',
                False,
                'some-embedded-scenedata-id')

    def test_add_version_control_item(self):
        self.assertEqual(
            self.sm.scenemark['VersionControl']['VersionList'][-1]['VersionNumber'],
            3.0)
        self.assertTrue(
            self.sm.scenemark['VersionControl']['VersionList'][-1]['DateTimeStamp'])
        self.assertTrue(
            self.sm.scenemark['VersionControl']['VersionList'][-1]['NodeID'],
            self.sm.node_id)

    def test_return_scenemark_to_ns(self):
        scenemark = self.sm.return_scenemark_to_ns(test = True)
        self.assertEqual(scenemark[0],"{")

    def test_add_notification_message(self):
        message = "This is a push notification"
        self.sm.add_custom_notification_message(message)
        self.assertEqual(self.sm.scenemark['NotificationMessage'], message)

class Request:
    def __init__(self):
        self.json = {
            "SceneMark": {
                "TimeStamp": "2021-10-29T21: 12: 17.245Z",
                "Version": "1.0",
                "SceneMarkID": "SMK_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_32cc6c",
                "SceneMarkStatus": "Active",
                "NotificationMessage": "",
                "NodeID": "83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7",
                "VersionControl": {
                    "DataPipelineInstanceID": "7e58d8bb-9545-4177-a508-40ece9cba7f5",
                    "VersionList": [
                        {
                            "VersionNumber": 2.0,
                            "DateTimeStamp": "2021-07-19T16:26:21.647Z",
                            "NodeID": "SecondNode"
                        },
                        {
                            "VersionNumber": 1.0,
                            "DateTimeStamp": "2021-07-19T16:25:21.647Z",
                            "NodeID": "FirstNode"
                        }
                    ]
                },
                "ThumbnailList": [
                    {
                        "VersionNumber": 1.0,
                        "SceneDataID": "SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_8a7d01"
                    }
                ],
                "AnalysisList": [
                    {
                        "VersionNumber": 1.0,
                        "AnalysisID": "0001-0002-AI2",
                        "AnalysisDescription": "General Detection of Humans",
                        "EventType": "Loitering",
                        "CustomEventType": "Write whatever here.",
                        "ProcessingStatus": "Detected",
                        "ErrorMessage": "",
                        "TotalItemCount": 1,
                        "DetectedObjects": [
                            {
                                "NICEItemType": "Human",
                                "CustomItemType": "",
                                "ItemID": "_123_",
                                "ItemTypeCount": 1,
                                "Probability": 0.73,
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
                                "RelatedSceneData": "SDT_00000013-60ed-9b3e-8002-000000001951_0001_e4041246"
                            }
                        ]
                    }
                ],
                "ParentSceneMarks": None,
                "ChildSceneMarks": None,
                "SceneDataList": [
                    {
                        "VersionNumber": 1.0,
                        "SceneDataID": "SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_8a7d01",
                        "TimeStamp": "2021-10-29T21: 12: 17.245Z",
                        "SourceNodeID": "83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7",
                        "SourceNodeDescription": "Scenera Bridge",
                        "Duration": None,
                        "DataType": "Thumbnail",
                        "Status": "Available at Provided URI",
                        "MediaFormat": "JPEG",
                        "SceneDataURI": "https://sduri.example.com/thumb.jpg",
                        "Resolution": {
                            "Height": 100,
                            "Width": 100
                        },
                        "EmbeddedSceneData": None,
                        "Encryption": {
                            "EncryptionOn": False,
                            "SceneEncryptionKeyID": None,
                            "PrivacyServerEndPoint": None
                        }
                    },
                    {
                        "VersionNumber": 1.0,
                        "SceneDataID": "SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_4ef702",
                        "TimeStamp": "2021-10-29T21:12:17.245Z",
                        "SourceNodeID": "83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7",
                        "SourceNodeDescription": "Scenera Bridge",
                        "Duration": None,
                        "DataType": "RGBStill",
                        "Status": "Available at Provided URI",
                        "MediaFormat": "JPEG",
                        "SceneDataURI": "https://sduri.example.com/still.jpg",
                        "Resolution": {
                            "Height": 100,
                            "Width": 100
                        },
                        "EmbeddedSceneData": None,
                        "Encryption": {
                            "EncryptionOn": False,
                            "SceneEncryptionKeyID": None,
                            "PrivacyServerEndPoint": None
                        }
                    },
                    {
                        "VersionNumber": .0,
                        "SceneDataID": "SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_80f203",
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
                        "Encryption": {
                            "EncryptionOn": False,
                            "SceneEncryptionKeyID": None,
                            "PrivacyServerEndPoint": None
                        }
                    },
                    {
                        "VersionNumber": 2.0,
                        "SceneDataID": "SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_80f205",
                        "TimeStamp": "2021-10-29T21:12:17.245Z",
                        "SourceNodeID": "83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7",
                        "SourceNodeDescription": "Scenera Bridge",
                        "Duration": "30",
                        "DataType": "RGBVideo",
                        "Status": "Upload in Progress",
                        "MediaFormat": "H.264",
                        "SceneDataURI": "https://sduri.example.com/vid2.mp4",
                        "Resolution": {
                            "Height": 100,
                            "Width": 100
                        },
                        "EmbeddedSceneData": None,
                        "Encryption": {
                            "EncryptionOn": False,
                            "SceneEncryptionKeyID": None,
                            "PrivacyServerEndPoint": None
                        }
                    },
                    {
                        "VersionNumber": 2.0,
                        "SceneDataID": "SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_80f204",
                        "TimeStamp": "2021-10-29T21:12:17.245Z",
                        "SourceNodeID": "83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7",
                        "SourceNodeDescription": "Scenera Bridge",
                        "Duration": "",
                        "DataType": "RGBStill",
                        "Status": "Available at Provided URI",
                        "MediaFormat": "JPEG",
                        "SceneDataURI": "https://sduri.example.com/still2.jpg",
                        "Resolution": {
                            "Height": 100,
                            "Width": 100
                        },
                        "EmbeddedSceneData": None,
                        "Encryption": {
                            "EncryptionOn": False,
                            "SceneEncryptionKeyID": None,
                            "PrivacyServerEndPoint": None
                        }
                    }
                ],
                "SceneModeConfig": None
            },
            "NodeSequencerHeader": {
                "Ingress": "http://localhost:5008/nodesequencer/1.0/setscenemark",
                "Token": "example-token-kjasdfpoisdjfpoiasdjfoipasjfopiasjdfpo",
                "NodeToken": "example-nodetoken-lalalalalalala",
                "NodeInput": {
                    "DataTypeMode": 6,
                    "RegionsOfInterest": [
                        {
                            "Polygon": [
                                {
                                    "X": 0.1,
                                    "Y": 0.2
                                },
                                {
                                    "X": 0.3,
                                    "Y": 0.4
                                },
                                {
                                    "X": 0.5,
                                    "Y": 0.6
                                }
                            ]
                        },
                        {
                            "Polygon": [
                                {
                                    "X": 0.7,
                                    "Y": 0.8
                                },
                                {
                                    "X": 0.9,
                                    "Y": 0.10
                                },
                                {
                                    "X": 0.11,
                                    "Y": 0.12
                                },
                                {
                                    "X": 0.13,
                                    "Y": 0.14
                                },
                                {
                                    "X": 0.15,
                                    "Y": 0.16
                                },
                                {
                                    "X": 0.17,
                                    "Y": 0.18
                                }
                            ]
                        }
                    ]
                }
            }
        }

if __name__ == '__main__':
    unittest.main()