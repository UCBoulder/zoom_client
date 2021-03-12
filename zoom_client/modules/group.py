import logging
import json
import time
from datetime import datetime
from ratelimit import limits, sleep_and_retry


class group:
    def __init__(self, controller, *args, **kwargs):
        self.zoom = controller

    def add_members(self, group_id, user_emails):
        # Special note: uses user emails as opposed to ID's

        logging.info(
            "Adding {} users to group with id {}".format(
                str(len(user_emails)), group_id
            )
        )

        def chunks(l, n):
            for i in range(0, len(l), n):
                yield l[i : i + n]

        for chunk in list(chunks(user_emails, 30)):
            logging.info("Processing adding chunk of 30 or less users to group...")
            post_data = {"members": [{"email": x} for x in chunk]}
            result = self.zoom.api_client.do_request(
                "post",
                "groups/" + group_id + "/members",
                "",
                body=json.dumps(post_data),
            )
            # simple check to make sure we don't exceed rate limits, this needs improvement!
            time.sleep(5)

        return result

    def delete_members(self, group_id, user_ids):
        # Special note: uses user ID's as oppposed to emails
        logging.info(
            "Removing {} users from group with id {}".format(
                str(len(user_ids)), group_id
            )
        )

        def chunks(l, n):
            for i in range(0, len(l), n):
                yield l[i : i + n]

        for chunk in list(chunks(user_ids, 30)):
            logging.info("Processing removing chunk of 30 or less users from group...")
            for user_id in chunk:
                result = self.zoom.api_client.do_request(
                    "delete", "groups/" + group_id + "/members/" + user_id, ""
                )
            # simple check to make sure we don't exceed rate limits, this needs improvement!
            # 30 requests per second are permissable and well below actual Edu account limits
            time.sleep(1)

        return result
