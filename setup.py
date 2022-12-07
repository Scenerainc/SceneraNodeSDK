from setuptools import setup, find_packages

from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="scenera.node",
    version="0.2.17",
    description="Scenera Node SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://docs.scenera.live/",
    author="Dirk Meulenbelt",
    author_email="dirkmeulenbelt@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    packages=["scenera.node"],
    include_package_data=True,
    install_requires=[
        "PyJWT",
        "cryptography",
        "jsonschema",
        "requests",
        "urllib3"]
)