"""
Configures a logger to be used throughout the SDk
"""

import logging

def configure_logger(
    logger,
    fmt: str = None,
    debug: bool = False) -> logging.Logger:
    # pylint: disable=line-too-long
    """
    Helper to configure the logger

    :param logger: the logger
    :type logger: logging.logger
    :param fmt: format structure
    :type fmt: string
    :param debug: debug on or off
    :type debug: bool
    :type token: string
    """
    if not fmt:
        fmt = "[%(asctime)s - %(levelname)s] %(name)s: [%(filename)s:%(lineno)s - %(funcName)s() ] %(message)s"
    formatter = logging.Formatter(fmt)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    if debug:
        logger.setLevel(logging.DEBUG)
    return logger
