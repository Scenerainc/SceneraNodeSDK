# pylint: disable=line-too-long
"""
Validates the token in the NodeSequencer header
"""

import jwt

NODESEQUENCER_PUBLIC_KEY = "-----BEGIN RSA PUBLIC KEY-----\nMIIBCgKCAQEAwQJ0bZfrWHxmEaYA/sG6FLx64+yxpH4quK36/wVm4+xhlvF4V7bdvvb4jg5teUZkaGdF96EnW/wQhtLZoYU/YSkT9mCXdm5k/gB0LE22peWuNZ3xFDVm4/O0XD/+20X/h9pux2pbBN+X21zwnil97H8u5VLOcvzy+yiivBOSWicol2xS376xwzX/VZjouxqzMfqRofRGa60y+e4vMzeEdAsu+fSADUj3Zh27ua8d1K2fCEqfClHPFBMB/HbLT9AtJFWBTThJqIaHn6cHtx1/6hk5elenmzoOQA4DdoEIxCjdZ0kkOH/W3aa0GCSKdnuUPFSeg9QRVsV9aC1Kn4Xx4wIDAQAB\n-----END RSA PUBLIC KEY-----"

def validate_jwt_token(token):
    """
    Used to validate the security token in the NodeSequencer Header

    :param token: token, in jwt format
    :type token: string
    """
    jwt.decode(
        token,
        NODESEQUENCER_PUBLIC_KEY,
        algorithms = ['RS256'],
        audience = "Scenera-Node"
        )
