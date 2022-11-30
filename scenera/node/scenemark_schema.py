scenemark_schema = {
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
                            "RegionOfInterest",
                            "Custom",
                            "Loitering",
                            "Intrusion",
                            "Falldown",
                            "Violence",
                            "Fire",
                            "Abandonment",
                            "SpeedGate",
                            "Xray",
                            "Facility",
                            "Scheduled",
                            "Test"
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
                                        "Scene",
                                        "Fire",
                                        "Furniture",
                                        "Bag",
                                        "Accessory",
                                        "Weapon",
                                        "Undefined",
                                        "Test"
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
            "type": ["array", "null"],
            "description": "This defines the depth of analysis performed and whether a resut of an output can be used to drive a subsequent capture of frames.",
            "uniqueItems": True,
            "items": {
                "type": "object",
                "description": "If this value is set to 20s the node should not generaate another SceneMark for 20s after the first SceneMark was generated.",
                "properties": {
                    "Analysis": {
                        "type": "string",
                        "enum": [
                            "Motion",
                            "Snapshot",
                            "Scheduled",
                            "Continuous",
                            "Label",
                            "ItemPresence",
                            "Loitering",
                            "Intrusion",
                            "Falldown",
                            "Violence",
                            "Fire",
                            "Abandonment",
                            "SpeedGate",
                            "Xray",
                            "Facility",
                            "Custom"
                        ]
                    },
                    "AnalysisStage": {
                        "type": "string",
                        "enum": [
                            "Motion",
                            "Detect",
                            "Recognize",
                            "Characterize"
                        ]
                    },
                    "CustomAnalysisID": {
                        "type": ["string", "null"],
                        "description": "Each algorithm and set of weights has a unique ID that is defined by NICE. This value shall be carried in this record."
                    },
                    "AnalysisDescription": {
                        "type": ["string", "null"],
                        "description": "Description of algorithm."
                    },
                    "CustomAnalysisStage": {
                        "type": ["string", "null"],
                        "description": "This defines analysis stages that are proprietary."
                    },
                    "LabelRefDataList": {
                        "type": "array",
                        "description": "For a specific label the following are reference data such as images for the particular label. The Node shall process these images to create the appropriate reference vector and store which RefDataIDs have been used to create the vector. If new RefDataIDs are detected in the SceneMode object the vector shall be regenerated with the listed RefData.",
                        "uniqueItems": True,
                        "items": {
                            "type": "object",
                            "properties": {
                                "LabelName": {
                                    "type": "string",
                                    "description": "Label name for example for facial recognition this would be the name or id of an individual."
                                },
                                "RefDataList": {
                                    "type": "array",
                                    "uniqueItems": True,
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "RefDataID": {
                                                "type": "string"
                                            },
                                            "RefDataEndPoint": {
                                                "$ref": "#/definitions/EndPoint"
                                            }
                                        },
                                        "required": [
                                            "RefDataID"
                                        ]
                                    }
                                },
                                "RefData": {
                                    "type": "array",
                                    "uniqueItems": True,
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "RefDataID": {
                                                "type": "string"
                                            },
                                            "RefData": {
                                                "type": "string",
                                                "description": "Reference data encoded in Base64. For example an image of a persons face."
                                            },
                                            "Encryption": {
                                                "$ref": "#/definitions/Encryption"
                                            }
                                        },
                                        "required": [
                                            "RefDataID",
                                            "RefData",
                                            "Encryption"
                                        ]
                                    }
                                },
                                "ProcessingStage": {
                                    "type": "string",
                                    "description": "This indicates which analysis stage should use the reference data.",
                                    "enum": [
                                        "CustomAnalysis",
                                        "Motion",
                                        "Detect",
                                        "Recognize",
                                        "Characterize"
                                    ]
                                }
                            },
                            "required": [
                                "ProcessingStage",
                                "LabelName"
                            ]
                        }
                    },
                    "AnalysisThreshold": {
                        "type": "number",
                        "description": "The output of the analysis should be greater than this value to trigger the Capture Sequence."
                    },
                    "AnalysisSampleRate": {
                        "type": "number"
                    },
                    "AnalysisRegion": {
                        "type": "object",
                        "properties": {
                            "ROIType": {
                                "type": "string",
                                "enum": [
                                    "MultiPolygon",
                                    "MultiLine",
                                    "SingleLine",
                                    "SinglePolygon"
                                ]
                            },
                            "ROICoords": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "Severity": {
                                            "type": "string"
                                        },
                                        "Coords": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "XCoord": {
                                                        "type": "number"
                                                    },
                                                    "YCoord": {
                                                        "type": "number"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "IgnoreObjectDetection": {
                        "type": "object",
                        "properties": {
                            "ObjectLargerThan": {
                                "type": "number",
                                "description": "If object is larger than this fraction of screen Area, ignore inferencing or Motion Detection"
                            },
                            "ObjectSmallerThan": {
                                "type": "number",
                                "description": "if smaller than this value (fraction of screen), ignore inferencing or Motion Detection"
                            }
                        }
                    },
                    "Scheduling": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "SchedulingType": {
                                    "type": "string",
                                    "enum": [
                                        "Default",
                                        "ScheduledOnce",
                                        "ScheduledHourly",
                                        "ScheduledDaily",
                                        "ScheduledWeekDay",
                                        "ScheduledWeekEnd",
                                        "ScheduledWeekly",
                                        "ScheduledMonthly",
                                        "ScheduledAnnually",
                                        "Sunday",
                                        "Monday",
                                        "Tuesday",
                                        "Wednesday",
                                        "Thursday",
                                        "Friday",
                                        "Saturday",
                                        "Holiday"
                                    ]
                                },
                                "StartTime": {
                                    "type": "string"
                                },
                                "EndTime": {
                                    "type": "string"
                                }
                            }
                        }
                    },
                    "Encryption": {
                        "$ref": "#/definitions/Encryption"
                    },
                    "Filters": {
                        "type": "object",
                        "description": "These items are used to either explicitly trigger a SceneMark or should be ignored when they are triggered.",
                        "properties": {
                            "IgnoreTheseDetectedItems": {
                                "type": "array",
                                "description": "If the algorithm detects any items in this list, these should items should be ignored.",
                                "items": {
                                    "type": "string"
                                }
                            },
                            "TriggerOnTheseDetectedItems": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                    "description": "The SceneMarks should only be triggered if one of the items in the list are detected."
                                }
                            }
                        }
                    },
                    "MinimumSceneData": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "DataType": {
                                    "type": "string",
                                    "enum": [
                                        "RGBStill",
                                        "RGBVideo"
                                    ]
                                },
                                "Count": {
                                    "type": "integer"
                                },
                                "Required": {
                                    "type": "boolean"
                                }
                            }
                        }
                    },
                    "AnalysisParams": {
                        "type": "array",
                        "items": [
                            {
                                "type": "object",
                                "properties": {
                                    "ParamName": {
                                        "type": "string"
                                    },
                                    "ParamValue": {
                                        "type": "number"
                                    }
                                }
                            }
                        ]
                    },
                    "SceneMarkWindow": {
                        "type": "number",
                        "description": "The period of time during which after a first SceneMark is generate a second SceneMark is not generated. For example if set to 10 no new SceneMark should be sent for 10 seconds."
                    },
                    "SceneMarkFrequency": {
                        "type": "number",
                        "description": "If \"Analysis\" is \"Continuous\" this is the period for generating each new SceneMark."
                    },
                    "AIServer": {
                        "type": "object",
                        "properties": {
                            "Protocol": {
                                "type": "string"
                            },
                            "Authority": {
                                "type": "string"
                            },
                            "ID": {
                                "type": "string"
                            },
                            "Pass": {
                                "type": "string"
                            }
                        }
                    },
                    "Blur": {
                        "type": ["array", "null"],
                        "items": {
                            "type": "string",
                            "enum": [
                                "Face",
                                "Text"
                            ]
                        }
                    },
                    "DrawBoundingBoxes": {
                        "type": ["object", "null"],
                        "description": "If true draw bounding box on detected items.",
                        "properties": {
                            "Draw": {
                                "type": "boolean"
                            },
                            "ExecuteOnPipeline": {
                                "type": "boolean"
                            }
                        }
                    },
                    "Resolution": {
                        "type": ["object", "null"],
                        "properties": {
                            "Height": {
                                "type": "integer"
                            },
                            "Width": {
                                "type": "integer"
                            }
                        }
                    }
                },
                "required": []
            }
        }
    },
    "required": [
        "SceneMarkID",
        "Version",
        "SceneMarkStatus"
    ]
}
