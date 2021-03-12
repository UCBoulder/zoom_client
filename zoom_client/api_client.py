import logging
import json
import requests
import jwt
import datetime

requests.packages.urllib3.disable_warnings()


class client:
    def __init__(self, root_request_url, key, secret, data_type):
        self.root_request_url = root_request_url
        self.key = key
        self.secret = secret
        self.data_type = data_type

    def generate_jwt(self):
        headers = {
            "alg": "HS256",
            "typ": "JWT",
        }

        encoded = jwt.encode(
            {
                "iss": self.key,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
            },
            self.secret,
            algorithm="HS256",
            headers=headers,
        )

        return {
            "Authorization": "Bearer " + encoded.decode("utf-8"),
            "Content-type": "application/json",
        }

    def do_request(self, request_type, resource, request_parameters, body={}):

        if request_type == "get":
            rsp = requests.get(
                self.root_request_url + resource,
                params=request_parameters,
                headers=self.generate_jwt(),
                verify=False,
            )

        elif request_type == "delete":
            rsp = requests.delete(
                self.root_request_url + resource,
                params=request_parameters,
                headers=self.generate_jwt(),
                verify=False,
            )

        elif request_type == "patch":
            rsp = requests.patch(
                self.root_request_url + resource,
                params=request_parameters,
                data=body,
                headers=self.generate_jwt(),
                verify=False,
            )

        elif request_type == "post":
            rsp = requests.post(
                self.root_request_url + resource,
                params=request_parameters,
                data=body,
                headers=self.generate_jwt(),
                verify=False,
            )

        if "Retry-After" in rsp.headers.keys():
            logging.warning("Retry-After detected: " + str(rsp.headers["Retry-After"]))
            logging.warning(
                "X-RateLimit-Limit: " + str(rsp.headers["X-RateLimit-Limit"])
            )
            logging.warning(
                "X-RateLimit-Remaining: " + str(rsp.headers["X-RateLimit-Remaining"])
            )

        try:
            result = rsp.json()
        except:
            result = rsp

        rsp.close()

        return result
