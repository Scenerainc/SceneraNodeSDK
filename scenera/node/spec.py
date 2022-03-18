"""
Provides relevant schemas to match the NICE Specification

For more information: https://www.nicealliance.org/specs/
"""
# pylint: disable=too-many-lines
import jsonschema

__author__ = 'Dirk Meulenbelt'
__date__ = '14.03.22'

def request_json_validator(request, schema):
    """
    Used internally to validate incoming and outgoing requests.

    :param request: the request json
    :type request: json
    :param schema: the schema found in the Spec
    :type schema: json
    :raises ValidationError: Represents a JSON Schema validation error.
    """
    try:
        jsonschema.validate(instance = request, schema = schema)
    except jsonschema.exceptions.ValidationError as _e:
        raise jsonschema.exceptions.ValidationError(_e.message)
    return True

class Spec:
    """
    Holds information relating to the Scenera Specification
    """
    # pylint: disable=too-few-public-methods
    EventType = frozenset([
        "Custom",
        "ItemPresence",
        "Loitering",
        "Intrusion",
        "Falldown",
        "Violence",
        "Fire",
        "Abandonment",
        "SpeedGate",
        "Xray",
        "Facility"])

    NICEItemType = frozenset([
        "Motion",
        "Face",
        "Human",
        "Vehicle",
        "Label",
        "Animal",
        "TextLogoQRCode",
        "Custom",
        "Scene",
        "Undefined"])

    ProcessingStatus = frozenset([
        "CustomAnalysis",
        "Motion",
        "Detected",
        "Recognized",
        "Characterized",
        "Undetected",
        "Failed",
        "Error"])

    Status = frozenset([
        "Available at Provided URI",
        "Upload in Progress"])

    DataType = frozenset([
        "Thumbnail",
        "RGBStill",
        "IRStill",
        "DepthStill",
        "RGBStereoStill",
        "ThermalStill",
        "RGBVideo",
        "IRVideo",
        "DepthVideo",
        "RGBStereoVideo",
        "ThermalVideo"
        "Audio",
        "Temperature",
        "Humidity",
        "PIR",
        "CarbonMonoxide",
        "AudioTranscript",
        "IRDetection",
        "Pressure",
        "Proximity",
        "LiquidLevel",
        "Acceleration",
        "Rotation",
        "Other"])

    MediaFormat = frozenset([
        "UNSPECIFIED",
        "JPEG",
        "PNG",
        "H264",
        "H265",
        "RAW",
        "JSON"])

    AudioMediaFormat = frozenset([
        "AAC",
        "MP3",
        "WAV"])

    # The following three specs are related to the Encryption
    CryptographicCurve = frozenset([
        "P256"])

    HashMethod = frozenset([
        "MD5",
        "SHA1",
        "SHA256"])

    KeyType = frozenset([
        "EC",
        "RSA"])

    DataTypeEnumDict = {
        0 : 'Thumbnail',
        1 : 'RGBStill',
        2 : 'IRStill',
        3 : 'DepthStill',
        4 : 'RGBStereoStill',
        5 : 'ThermalStill',
        6 : 'RGBVideo',
        7 : 'IRVideo',
        8 : 'DepthVideo',
        9 : 'RGBStereoVideo',
        10: 'ThermalVision',
        11: 'Audio',
        12: 'Temperature',
        13: 'Humidity',
        14: 'PIR',
        15: 'CarbonMonoxide',
        16: 'AudioTranscript',
        17: 'IRDetection',
        18: 'Pressure',
        19: 'Proximity',
        20: 'LiquidLevel',
        21: 'Acceleration',
        22: 'Rotatioan',
        23: 'Other'
    }

    # pylint: disable=line-too-long
    SceneMarkSchema = {
        "$schema": "http://json-schema.org/draft-06/schema#",
        "type": "object",
        "title": "SceneMark",
        "description": "The SceneMark contains data describing what has been captured in SceneData and either contains references to SceneData or contains the SceneData itself.",
        "properties": {
            "Version": {
                "type": "string",
                "enum": [
                    "1.0"
                ]
            },
            "TimeStamp": {
                "type": [
                    "string",
                    "null"
                ],
                "description": "Time stamp for when the SceneMark is first generated."
            },
            "SceneMarkID": {
                "type": "string",
                "description": "Unique ID for a SceneMark. This ID is unique across the NICE ecosystem."
            },
            "DestinationID": {
                "type": [
                    "array",
                    "null"
                ],
                "description": "DataService or App ID initiated the request for this SceneMark",
                "items": {
                    "type": "string"
                }
            },
            "SceneMarkStatus": {
                "type": "string",
                "enum": [
                    "Removed",
                    "Active",
                    "Processed"
                ]
            },
            "NodeID": {
                "type": "string"
            },
            "VersionControl": {
                "type": "object",
                "properties": {
                    "DataPipelineInstanceID": {
                        "type": "string"
                    },
                    "VersionList": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "VersionNumber": {
                                    "type": "number"
                                },
                                "DateTimeStamp": {
                                    "type": [
                                        "string",
                                        "null"
                                    ]
                                },
                                "NodeID": {
                                    "type": "string"
                                }
                            },
                            "required": [
                                "VersionNumber",
                                "NodeID"
                            ]
                        }
                    }
                }
            },
            "ThumbnailList": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "VersionNumber": {
                            "type": "number"
                        },
                        "SceneDataID": {
                            "type": "string",
                            "description": "SceneDataID should appear in the SceneDataList that is inclulded in the SeneMark."
                        }
                    },
                    "required": [
                        "VersionNumber",
                        "SceneDataID"
                    ]
                }
            },
            "AnalysisList": {
                "type": "array",
                "uniqueItems": True,
                "items": {
                    "type": "object",
                    "properties": {
                        "VersionNumber": {
                            "type": "number"
                        },
                        "AnalysisID": {
                            "type": [
                                "string",
                                "null"
                            ],
                            "description": "Each algorithm and set of weights has a unique ID that is defined by NICE. This value shall be carried in this record."
                        },
                        "EventType": {
                            "type": "string",
                            "enum": [
                                "ItemPresence",
                                "Custom",
                                "Loitering",
                                "Intrusion",
                                "Falldown",
                                "Violence",
                                "Fire",
                                "Abandonment",
                                "SpeedGate",
                                "Xray",
                                "Facility"
                            ]
                        },
                        "CustomEventType": {
                            "type": [
                                "string",
                                "null"
                            ]
                        },
                        "AnalysisDescription": {
                            "type": [
                                "string",
                                "null"
                            ]
                        },
                        "ProcessingStatus": {
                            "type": "string",
                            "enum": [
                                "Motion",
                                "Detected",
                                "Recognized",
                                "Characterized",
                                "Undetected",
                                "Failed",
                                "Error",
                                "CustomAnalysis"
                            ]
                        },
                        "ErrorMessage": {
                            "type": [
                                "string",
                                "null"
                            ]
                        },
                        "TotalItemCount": {
                            "type": [
                                "number",
                                "null"
                            ]
                        },
                        "DetectedObjects": {
                            "type": [
                                "array",
                                "null"
                            ],
                            "uniqueItems": True,
                            "items": {
                                "type": "object",
                                "properties": {
                                    "NICEItemType": {
                                        "type": "string",
                                        "description": "NICE defines diferent DeviceModes which target specific types of data associated with the DeviceMode.",
                                        "enum": [
                                            "Motion",
                                            "Face",
                                            "Human",
                                            "Vehicle",
                                            "Label",
                                            "TextLogoQRCode",
                                            "Animal",
                                            "Custom",
                                            "Scene"
                                        ]
                                    },
                                    "CustomItemType": {
                                        "type": [
                                            "string",
                                            "null"
                                        ],
                                        "description": "Devices may have proprietary AI algorithms embedded in the device or processing node. If this algorithm was used, the label generated by the algorithm shall be carreid in this field."
                                    },
                                    "ItemID": {
                                        "type": [
                                            "string",
                                            "null"
                                        ],
                                        "description": "Unique ID that is associated with this instance of object. This is an optional field that may be used to track objects across different scenemarks."
                                    },
                                    "Probability": {
                                        "type": [
                                            "number",
                                            "null"
                                        ],
                                        "description": "Certainty of the Attribute According to the Algorithm"
                                    },
                                    "Attributes": {
                                        "type": [
                                            "array",
                                            "null"
                                        ],
                                        "description": "Different AI algorithms are capable of identifying different attribute of objects that have been identified. For example if a face is detected the attribute may be \"smiling\". These attributes depend on the AI algorithm used and are not specified.",
                                        "uniqueItems": True,
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "Attribute": {
                                                    "type": "string",
                                                    "description": "Attribute of face recognized - mood etc"
                                                },
                                                "Value": {
                                                    "type": "string"
                                                },
                                                "ProbabilityofAttribute": {
                                                    "type": [
                                                        "number",
                                                        "null"
                                                    ],
                                                    "description": "Degree of certainty of the attribute"
                                                },
                                                "VersionNumber": {
                                                    "type": "number",
                                                    "description": "Unique ID for the algorithm."
                                                }
                                            },
                                            "required": []
                                        }
                                    },
                                    "BoundingBox": {
                                        "type": [
                                            "object",
                                            "null"
                                        ],
                                        "properties": {
                                            "XCoordinate": {
                                                "type": "number"
                                            },
                                            "YCoordinate": {
                                                "type": "number"
                                            },
                                            "Height": {
                                                "type": "number"
                                            },
                                            "Width": {
                                                "type": "number"
                                            }
                                        },
                                        "required": [
                                            "Height",
                                            "Width",
                                            "XCoordinate",
                                            "YCoordinate"
                                        ]
                                    },
                                    "RelatedSceneData": {
                                        "type": "string"
                                    },
                                    "ItemTypeCount": {
                                        "type": [
                                            "number",
                                            "null"
                                        ]
                                    }
                                },
                                "required": []
                            }
                        }
                    },
                    "required": []
                }
            },
            "ParentSceneMarks": {
                "type": [
                    "array",
                    "null"
                ],
                "items": {
                    "type": "object",
                    "properties": {
                        "VersionNumber": {
                            "type": "number"
                        },
                        "SceneMarkID": {
                            "type": "string"
                        }
                    }
                }
            },
            "ChildSceneMarks": {
                "type": [
                    "array",
                    "null"
                ],
                "items": {
                    "type": "object",
                    "properties": {
                        "VersionNumber": {
                            "type": "number"
                        },
                        "SceneMarkID": {
                            "type": "string"
                        }
                    }
                }
            },
            "SceneDataList": {
                "type": "array",
                "items": {
                    "type": "object",
                    "description": "For a particular SceneMark there may be several SceneData objects. This array contains one or more SceneData objects.",
                    "properties": {
                        "VersionNumber": {
                            "type": "number"
                        },
                        "TimeStamp": {
                            "type": [
                                "string",
                                "null"
                            ]
                        },
                        "SourceNodeID": {
                            "type": "string"
                        },
                        "SourceNodeDescription": {
                            "type": [
                                "string",
                                "null"
                            ]
                        },
                        "Duration": {
                            "type": [
                                "string",
                                "integer",
                                "number",
                                "null"
                            ]
                        },
                        "DataType": {
                            "type": "string",
                            "description": "Types of data that is in the SceneData object.",
                            "enum": [
                                "RGBStill",
                                "IRStill",
                                "DepthStill",
                                "RGBStereoStill",
                                "ThermalStill",
                                "RGBVideo",
                                "IRVideo",
                                "DepthVideo",
                                "RGBStereoVideo",
                                "ThermalVideo",
                                "Audio",
                                "Temperature",
                                "Humidity",
                                "PIR",
                                "CarbonMonoxide",
                                "AudioTranscript",
                                "IRDetection",
                                "Pressure",
                                "Proximity",
                                "LiquidLevel",
                                "Acceleration",
                                "Rotation",
                                "Thumbnail",
                                "Other"
                            ]
                        },
                        "Status": {
                            "type": "string",
                            "enum": [
                                "Available at Provided URI",
                                "Upload in Progress"
                            ]
                        },
                        "MediaFormat": {
                            "type": [
                                "string",
                            ],
                            "enum": [
                                "UNSPECIFIED",
                                "JPEG",
                                "PNG",
                                "H.264",
                                "H.265",
                                "RAW",
                                "JSON"
                            ]
                        },
                        "Resolution": {
                            "type": [
                                "object",
                                "null"
                            ],
                            "properties": {
                                "Height": {
                                    "type": "integer"
                                },
                                "Width": {
                                    "type": "integer"
                                }
                            }
                        },
                        "SceneDataID": {
                            "type": "string",
                            "description": "Unique Identifier for the SceneData referenced by this data structure."
                        },
                        "SceneDataURI": {
                            "type": "string",
                            "description": "This is URI to an external data object."
                        },
                        "EmbeddedSceneData": {
                            "type": [
                                "string",
                                "null"
                            ],
                            "description": "Data may be directly embedded in the SceneMark. The Data is encoded as Base64."
                        },
                        "Encryption": {
                            "Encryption": {
                                "type": [
                                    "object",
                                    "null"
                                ],
                                "required": [],
                                "oneOf": [
                                    {
                                        "type": "object",
                                        "properties": {
                                            "EncryptionOn": {
                                                "type": "boolean",
                                                "enum": [
                                                    False
                                                ]
                                            }
                                        },
                                        "required": [
                                            "EncryptionOn"
                                        ]
                                    },
                                    {
                                        "type": "object",
                                        "properties": {
                                            "EncryptionOn": {
                                                "type": "boolean",
                                                "enum": [
                                                    True
                                                ]
                                            },
                                            "SceneEncryptionKeyID": {
                                                "type": "string",
                                                "description": "Unique Key Identifier that enables the key used to encrypt the data. If EncryptionOn is False this value will be ignored."
                                            },
                                            "PrivacyServerEndPoint": {
                                                "type": "object",
                                                "properties": {
                                                    "AppEndPoint": {
                                                        "ApplicationEndPointSpecifier": {
                                                            "type": "object",
                                                            "properties": {
                                                                "APIVersion": {
                                                                    "type": "string",
                                                                    "enum": [
                                                                        "1.0"
                                                                    ]
                                                                },
                                                                "EndPointID": {
                                                                    "type": "string",
                                                                    "description": "The NICE Identifier for the Application that is ultimatley the end point for messages."
                                                                },
                                                                "X.509Certificate": {
                                                                    "type": "string"
                                                                },
                                                                "AccessToken": {
                                                                    "type": "string",
                                                                    "description": "This token is used by the receiving NICE entity. It shall always comply ot the JWT (RFC 7519) format"
                                                                }
                                                            },
                                                            "required": [
                                                                "APIVersion",
                                                                "EndPointID"
                                                            ]
                                                        }
                                                    },
                                                    "NetEndPoint": {
                                                        "NetworkEndPointSpecifier": {
                                                            "type": "object",
                                                            "properties": {
                                                                "APIVersion": {
                                                                    "type": "string",
                                                                    "enum": [
                                                                        "1.0"
                                                                    ]
                                                                },
                                                                "EndPointID": {
                                                                    "type": "string"
                                                                },
                                                                "NodeID": {
                                                                    "type": "string"
                                                                },
                                                                "PortID": {
                                                                    "type": "string"
                                                                },
                                                                "Scheme": {
                                                                    "type": "array",
                                                                    "uniqueItems": True,
                                                                    "items": {
                                                                        "anyOf": [
                                                                            {
                                                                                "MQTTScheme": {
                                                                                    "type": "object",
                                                                                    "title": "Network end point specifier for MQTT",
                                                                                    "properties": {
                                                                                        "Protocol": {
                                                                                            "type": "string",
                                                                                            "enum": [
                                                                                                "MQTT"
                                                                                            ]
                                                                                        },
                                                                                        "Authority": {
                                                                                            "type": "string"
                                                                                        },
                                                                                        "Username": {
                                                                                            "type": "string"
                                                                                        },
                                                                                        "Password": {
                                                                                            "type": "string",
                                                                                            "description": "Network AccessToken."
                                                                                        },
                                                                                        "ClientID": {
                                                                                            "type": "string"
                                                                                        },
                                                                                        "QoS": {
                                                                                            "type": "integer",
                                                                                            "enum": [
                                                                                                0,
                                                                                                1,
                                                                                                2
                                                                                            ]
                                                                                        }
                                                                                    },
                                                                                    "required": [
                                                                                        "Protocol",
                                                                                        "Authority",
                                                                                        "Username",
                                                                                        "Password",
                                                                                        "ClientID"
                                                                                    ]
                                                                                }
                                                                            },
                                                                            {
                                                                                "WebAPIScheme": {
                                                                                    "type": "object",
                                                                                    "title": "Network end point specifier for WebAPI",
                                                                                    "properties": {
                                                                                        "Protocol": {
                                                                                            "type": "string",
                                                                                            "enum": [
                                                                                                "WebAPI"
                                                                                            ]
                                                                                        },
                                                                                        "Authority": {
                                                                                            "type": "string"
                                                                                        },
                                                                                        "AccessToken": {
                                                                                            "type": "string"
                                                                                        },
                                                                                        "Role": {
                                                                                            "type": "string",
                                                                                            "description": "If set to Client, the port shall initiate GET or SET data requests. If Server then the port shall act as a server. ",
                                                                                            "enum": [
                                                                                                "Client",
                                                                                                "Server"
                                                                                            ]
                                                                                        },
                                                                                        "ValidationKey": {
                                                                                            "$ref": "#/definitions/PublicKey"
                                                                                        }
                                                                                    },
                                                                                    "required": [
                                                                                        "Protocol",
                                                                                        "Authority"
                                                                                    ]
                                                                                }
                                                                            },
                                                                            {
                                                                                "WebRTCScheme": {
                                                                                    "type": "object",
                                                                                    "title": "Network end point specifier for WebRTC",
                                                                                    "properties": {
                                                                                        "Protocol": {
                                                                                            "type": "string",
                                                                                            "enum": [
                                                                                                "WebRTC"
                                                                                            ]
                                                                                        },
                                                                                        "IceServers": {
                                                                                            "type": "array",
                                                                                            "uniqueItems": True,
                                                                                            "items": {
                                                                                                "type": "object",
                                                                                                "properties": {
                                                                                                    "urls": {
                                                                                                        "type": "array",
                                                                                                        "uniqueItems": True,
                                                                                                        "items": {
                                                                                                            "type": "string",
                                                                                                            "description": "STUN/TURN server URL. e.g. turn:turnserver.example.org"
                                                                                                        }
                                                                                                    },
                                                                                                    "username": {
                                                                                                        "type": "string"
                                                                                                    },
                                                                                                    "credential": {
                                                                                                        "type": "string"
                                                                                                    }
                                                                                                },
                                                                                                "required": [
                                                                                                    "urls"
                                                                                                ]
                                                                                            }
                                                                                        }
                                                                                    },
                                                                                    "required": [
                                                                                        "Protocol"
                                                                                    ]
                                                                                }
                                                                            },
                                                                            {
                                                                                "type": "object",
                                                                                "title": "Network end point specifier for local connection",
                                                                                "properties": {
                                                                                    "Protocol": {
                                                                                        "type": "string",
                                                                                        "enum": [
                                                                                            "Local"
                                                                                        ]
                                                                                    }
                                                                                },
                                                                                "required": [
                                                                                    "Protocol"
                                                                                ]
                                                                            }
                                                                        ]
                                                                    }
                                                                }
                                                            },
                                                            "required": [
                                                                "APIVersion",
                                                                "EndPointID",
                                                                "Scheme"
                                                            ]
                                                        }
                                                    }
                                                },
                                                "required": [
                                                    "NetEndPoint"
                                                ]
                                            }
                                        },
                                        "required": [
                                            "EncryptionOn",
                                            "SceneEncryptionKeyID"
                                        ]
                                    }
                                ]
                            }
                        }
                    },
                    "required": [
                        "TimeStamp",
                        "Encryption",
                        "SceneDataID"
                    ]
                }
            },
            "SceneModeConfig": {
                "type": [
                    "array",
                    "null"
                ],
                "items": {
                    "type": "object",
                    "additionalProperties": {
                        "not": {}
                    },
                    "properties": {
                        "CustomAnalysisStage": {
                            "type": "string"
                        },
                        "AnalysisRegion": {
                            "type": "object",
                            "properties": {
                                "ROICoords": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "Coords": {
                                                "type": "array",
                                                "items": {
                                                    "type": "object",
                                                    "properties": {
                                                        "XCoord": {
                                                            "type": "integer"
                                                        },
                                                        "YCoord": {
                                                            "type": "integer"
                                                        }
                                                    },
                                                    "required": [
                                                        "XCoord",
                                                        "YCoord"
                                                    ]
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "Resolution": {
                            "type": "string"
                        },
                        "Threshold": {
                            "type": "number"
                        },
                        "Scheduling": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "additionalProperties": {
                                    "not": {}
                                },
                                "properties": {
                                    "SchedulingType": {
                                        "type": "string"
                                    },
                                    "StartTime": {
                                        "type": "string"
                                    },
                                    "EndTime": {
                                        "type": "string"
                                    }
                                },
                                "required": [
                                    "SchedulingType",
                                    "StartTime",
                                    "EndTime"
                                ]
                            }
                        }
                    },
                    "required": [
                        "CustomAnalysisStage",
                        "AnalysisRegion",
                        "Resolution",
                        "Threshold",
                        "Scheduling"
                    ]
                }
            }
        },
        "required": [
            "SceneMarkID",
            "Version",
            "SceneMarkStatus"
        ]
    }

    NodesequencerHeaderSchema = {
        "$schema": "http://json-schema.org/draft-06/schema#",
        "$ref": "#/definitions/Welcome6",
        "definitions": {
            "Welcome6": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "Ingress": {
                        "type": "string",
                        "format": "uri",
                        "qt-uri-protocols": [
                            "http"
                        ]
                    },
                    "Token": {
                        "type": "string"
                    },
                    "NodeInput": {
                        "$ref": "#/definitions/NodeInput"
                    }
                },
                "required": [
                    "Ingress",
                    "Token"
                ],
                "title": "Welcome6"
            },
            "NodeInput": {
                "type": ["object","null"],
                "additionalProperties": False,
                "properties": {
                    "DataTypeMode": {
                        "type": "integer"
                    },
                    "RegionsOfInterest": {
                        "type": "array",
                        "items": {
                            "$ref": "#/definitions/RegionsOfInterest"
                        }
                    }
                },
                "required": [
                    "DataTypeMode",
                ],
                "title": "NodeInput"
            },
            "RegionsOfInterest": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "Polygon": {
                        "type": "array",
                        "items": {
                            "$ref": "#/definitions/Polygon"
                        }
                    }
                },
                "required": [
                    "Polygon"
                ],
                "title": "RegionsOfInterest"
            },
            "Polygon": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "X": {
                        "type": "number"
                    },
                    "Y": {
                        "type": "number"
                    }
                },
                "required": [
                    "X",
                    "Y"
                ],
                "title": "Polygon"
            }
        }
    }
