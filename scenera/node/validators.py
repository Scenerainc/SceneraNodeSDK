"""
This file contains the main SceneMark class and its methods for the Scenera Node SDK.
"""

import logging
import jsonschema
from .logger import configure_logger

logger = logging.getLogger(__name__)
logger = configure_logger(logger, debug=True)

class ValidationError(Exception):
    """
    Self-defined error to raise when the values do not match.
    """
    def __init__(self, msg):
        _ = super().__init__()
        self.msg = msg

def request_json_validator(request, schema, schema_name):
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
        logger.exception(f"Schema validation failed for {schema_name}")
        raise jsonschema.exceptions.ValidationError(_e.message)
    return True
