nodesequencer_header_schema = {
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
                "NodeToken": {
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
                    "type": ["integer", "null"]
                },
                "RegionsOfInterest": {
                    "type": ["array", "null"],
                    "items": {
                        "$ref": "#/definitions/RegionsOfInterest"
                    }
                }
            },
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
