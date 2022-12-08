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
    "HatOff",
    "LightOff",
    "PosBreak",
    "IllegalStay"
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
