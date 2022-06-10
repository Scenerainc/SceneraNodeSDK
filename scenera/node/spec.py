"""
Provides relevant schemas to match the NICE Specification

For more information: https://www.nicealliance.org/specs/
"""
# pylint: disable=too-many-lines

# pylint: disable=too-few-public-methods
EventType = frozenset([
    "Custom",
    "RegionOfInterest",
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
    "Scheduled",
    "Test",
    ])

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
    "Fire",
    "Accessory",
    "Bag",
    "Furniture",
    "Weapon",
    "Undefined",
    "Test",
    ])

ProcessingStatus = frozenset([
    "CustomAnalysis",
    "Motion",
    "Detected",
    "Recognized",
    "Characterized",
    "Undetected",
    "Failed",
    "Error",
    ])

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
    "Other",
    ])

MediaFormat = frozenset([
    "UNSPECIFIED",
    "JPEG",
    "PNG",
    "H264",
    "H265",
    "RAW",
    "JSON",
    ])

AudioMediaFormat = frozenset([
    "AAC",
    "MP3",
    "WAV",
    ])

Status = frozenset([
    "Available at Provided URI",
    "Upload in Progress"])

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
    23: 'Other',
}
