# Zoom Client

A Python client for interfacing with the Zoom API to perform various tasks.

## Requirements and Documentation

* Python >= 3.6: [https://www.python.org/downloads/](https://www.python.org/downloads/)
* Enable Zoom API key: [https://zoom.us/developer/api/credential](https://zoom.us/developer/api/credential)

Zoom API documentation can be found at the following URL: [https://marketplace.zoom.us/docs/api-reference/zoom-api](https://marketplace.zoom.us/docs/api-reference/zoom-api)

## Installation from GitHub

```shell
pip install git+https://github.com/CUBoulder-OIT/zoom_client@main#egg=zoom_client
```

## Distribution Packaging

```shell
python setup.py sdist bdist_wheel
```

## Usage

1. Ensure requirements outlined above are completed.
2. Provide necessary &lt;bracketed&gt; areas in examples/sample_config.json specific to your account

## Example
```python
#open config file with api key/secret information
config_file = open(run_path+"/config/config.json")
config_data = json.load(config_file)

#create Zoom python client
zoom = controller.controller(config_data)

zoom.users.get_current_users()
zoom_user_counts = zoom.users.get_current_user_type_counts()
```

## Notice

All trademarks, service marks and company names are the property of their respective owners.

Reference in this site to any specific commercial product, process, or service, or the use of any trade, firm or corporation name is for the information and convenience of the public, and does not constitute endorsement, recommendation, or favoring by the University of Colorado.

## License

MIT - See LICENSE
