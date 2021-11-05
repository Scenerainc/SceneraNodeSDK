"""
Unittests
"""

import unittest
import jsonschema
from scenera.node import SceneMark, ValidationError, spec

class SceneMarkTestCase(unittest.TestCase):

    def setUp(self):
        self.sm = SceneMark(
            Request(),
            node_id = "unit_test_node",
            event_type = "Custom",
            custom_event_type = "Unit Test Event",
            analysis_description = "Unit Test",
            analysis_id = "83723ea6-9907-409d-86ea-01499c26841c"
        )

    def test_internal_settings(self):
        self.assertEqual(self.sm.node_id, "unit_test_node")
        self.assertEqual(self.sm.event_type, "Custom")
        self.assertEqual(self.sm.custom_event_type, "Unit Test Event")
        self.assertEqual(self.sm.analysis_description, "Unit Test")
        self.assertEqual(self.sm.analysis_id, "83723ea6-9907-409d-86ea-01499c26841c")

    def incorrect_scenemark_json_raises_error(self):
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            self.sm.request_json_validator(
                {"Some_incorrect_schema": "fails"},
                spec.SceneMarkSchema)

    def correct_scenemark_json_passes(self):
        self.assertTrue(
            self.sm.request_json_validator(
                self.sm.scenemark,
                spec.SceneMarkSchema))

    def incorrect_nodesequencer_address_json_raises_error(self):
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            self.sm.request_json_validator(
                {"Some_incorrect_schema": "fails"},
                spec.NodesequencerAddressSchema)

    def correct_nodesequencer_address_json_passes(self):
        self.assertTrue(
            self.sm.request_json_validator(
                self.sm.nodesequencer_address,
                spec.NodesequencerAddressSchema))

    def test_get_my_version_number(self):
        # Set to 3.0 because the initialisation has already
        # updated the VersionControl
        self.assertEqual(self.sm.get_my_version_number(), 3.0)

        #This can be left at 2.0 because it's the class attribute
        self.assertEqual(self.sm.my_version_number, 2.0)

    def test_get_scenedata_datatype_uri_dict(self):
        datatype_uri_dict = self.sm.get_scenedata_datatype_uri_dict()
        self.assertEqual(datatype_uri_dict['Thumbnail'], 'https://sduri.example.com/thumb.jpg')
        self.assertEqual(datatype_uri_dict['RGBStill'], 'https://sduri.example.com/still.jpg')
        self.assertEqual(datatype_uri_dict['RGBVideo'], 'https://sduri.example.com/vid.mp4')

    def test_get_scenedata_id_to_uri_dict(self):
        sd_id_uri_dict = self.sm.get_scenedata_id_uri_dict()
        self.assertEqual(
            sd_id_uri_dict['SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_8a7d01'],
            'https://sduri.example.com/thumb.jpg')
        self.assertEqual(
            sd_id_uri_dict['SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_4ef702'],
            'https://sduri.example.com/still.jpg')
        self.assertEqual(
            sd_id_uri_dict['SDT_83d6a043-00d9-49aa-a295-86a041fff6d8_d3e7_80f203'],
            'https://sduri.example.com/vid.mp4')

    def test_get_scenedata_uri_list(self):
        uri_list = self.sm.get_scenedata_uri_list()
        self.assertEqual(uri_list[0], 'https://sduri.example.com/thumb.jpg')
        self.assertEqual(uri_list[1], 'https://sduri.example.com/still.jpg')
        self.assertEqual(uri_list[2], 'https://sduri.example.com/vid.mp4')

    def test_get_scenedata_uri_list_exclude_thumb(self):
        uri_list = self.sm.get_scenedata_uri_list(True)
        self.assertEqual(uri_list[0], 'https://sduri.example.com/still.jpg')
        self.assertEqual(uri_list[1], 'https://sduri.example.com/vid.mp4')

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
        ref = f"SDT_{self.sm.node_id}_0001_{self.sm.generate_random_id(6)}"
        sd_id = self.sm.generate_scenedata_id()
        self.assertEqual(ref[:23], sd_id[:23])

    def test_generate_bounding_box(self):
        bounding_box = self.sm.generate_bounding_box(1,2,3,4)
        self.assertEqual(bounding_box['XCoordinate'], 1)
        self.assertEqual(bounding_box['YCoordinate'], 2)
        self.assertEqual(bounding_box['Height'], 3)
        self.assertEqual(bounding_box['Width'], 4)

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
            self.sm.generate_bounding_box(1,2,3,4)
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
        self.assertEqual(detected_object['BoundingBox']['XCoordinate'],1)
        self.assertEqual(detected_object['BoundingBox']['YCoordinate'],2)
        self.assertEqual(detected_object['BoundingBox']['Height'],3)
        self.assertEqual(detected_object['BoundingBox']['Width'],4)

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
            'custom-event-type',
            4,
            'some error happened',
            ['filler'],
            'Loitering'
        )
        self.assertEqual(self.sm.scenemark['AnalysisList'][-1]['VersionNumber'],
            self.sm.my_version_number)
        self.assertEqual(self.sm.scenemark['AnalysisList'][-1]['ProcessingStatus'], 'Detected')
        self.assertEqual(self.sm.scenemark['AnalysisList'][-1]['CustomEventType'],
            'custom-event-type')
        self.assertEqual(self.sm.scenemark['AnalysisList'][-1]['TotalItemCount'], 4)
        self.assertEqual(self.sm.scenemark['AnalysisList'][-1]['ErrorMessage'],
            'some error happened')
        self.assertEqual(self.sm.scenemark['AnalysisList'][-1]['DetectedObjects'], ['filler'])
        self.assertEqual(self.sm.scenemark['AnalysisList'][-1]['EventType'], 'Loitering')

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
            2.0)
        self.assertTrue(
            self.sm.scenemark['VersionControl']['VersionList'][-1]['DateTimeStamp'])
        self.assertTrue(
            self.sm.scenemark['VersionControl']['VersionList'][-1]['NodeID'],
            self.sm.node_id)

    def test_return_scenemark_to_ns(self):
        scenemark = self.sm.return_scenemark_to_ns(test = True)
        self.assertEqual(scenemark[0],"{")

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
                            "VersionNumber": 1.0,
                            "DateTimeStamp": "2021-07-19T16: 25: 21.647Z",
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
                        "VersionNumber": 1.0,
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
                    }
                ],
                "SceneModeConfig": None
            },
            "NodeSequencerAddress": {
                "Ingress": "http://localhost:5008/nodesequencer/1.0/setscenemark",
                "Token": "example-token-kjasdfpoisdjfpoiasdjfoipasjfopiasjdfpo"
            }
        }


if __name__ == '__main__':
    unittest.main()