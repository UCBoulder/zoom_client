"""
Pre-reqs: Python 3.x and requests library
By: Dave Bunten

License: MIT (see license.txt)
"""

import os
import sys
import logging
import json
import time
import math
import csv
from datetime import datetime,timedelta
import tzlocal
import argparse
import random
import assets.zoom.controller as controller

if __name__ == "__main__":

    run_path = os.path.dirname(os.path.realpath(__file__))

    #reduce the number of informational messages from the requests lib
    logging.getLogger('requests').setLevel(logging.WARNING)

    #open config file with api key/secret information
    config_file = open(run_path+"/config/config.json")
    config_data = json.load(config_file)

    #create Zoom python client
    zoom = controller.controller(config_data)

    zoom.users.get_current_users()
    zoom_user_counts = zoom.users.get_current_user_type_counts()


