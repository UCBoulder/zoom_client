import pathlib
import setuptools, os

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# Pull requirements from the text file
requirement_path = HERE / "requirements.txt"
install_requires = []
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()

# This call to setup() does all the work
setuptools.setup(
    name="zoom_client",
    version="0.0.2",
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
    install_requires=install_requires,
)
