""" setup.py for zoom_client """
import os
import pathlib

import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# Pull requirements from the text file
REQUIREMENT_PATH = HERE / "requirements.txt"
INSTALL_REQUIRES = []
if os.path.isfile(REQUIREMENT_PATH):
    with open(REQUIREMENT_PATH) as f:
        INSTALL_REQUIRES = f.read().splitlines()

# This call to setup() does all the work
setuptools.setup(
    name="zoom_client",
    version="0.0.4",
    description="Zoom (Video Communications) API Client",
    long_description=README,
    long_description_content_type="text/markdown",
    author="CU Boulder, OIT",
    author_email="dabu5788@colorado.edu",
    license="MIT",
    keywords="zoom api requests",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["zoom_client", "zoom_client.modules"],
    python_requires=">=3.6",
    install_requires=INSTALL_REQUIRES,
)
