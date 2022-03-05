"""
zoom_client class and related methods for gathering data
and making changes to Zoom groups
"""
import logging
import json
import time


class Group:
    """
    zoom_client group class for gathering data and making changes to Zoom groups
    """

    def __init__(self, client):
        self.zoom = client

    @staticmethod
    def chunks(big_list, count):
        """Helper method for chunking big lists into smaller ones"""
        for i in range(0, len(big_list), count):
            yield big_list[i : i + count]

    def add_members(self, group_id, user_emails):
        """Add members to Zoom group in batch by list of userid's"""
        # Special note: uses user emails as opposed to ID's

        logging.info("Adding %s users to group with id %s", len(user_emails), group_id)

        for chunk in list(self.chunks(user_emails, 30)):
            logging.info("Processing adding chunk of 30 or less users to group...")
            post_data = {"members": [{"email": x} for x in chunk]}
            result = self.zoom.client.do_request(
                "post",
                "groups/" + group_id + "/members",
                "",
                body=json.dumps(post_data),
            )
            # simple check to make sure we don't exceed rate limits, this needs improvement!
            time.sleep(5)

        return result

    def delete_members(self, group_id, user_ids):
        """Delete members from Zoom group in batch by list of userid's"""
        # Special note: uses user ID's as oppposed to emails
        logging.info("Removing %s users from group with id %s", len(user_ids), group_id)

        for chunk in list(self.chunks(user_ids, 30)):
            logging.info("Processing removing chunk of 30 or less users from group...")
            for user_id in chunk:
                result = self.zoom.client.do_request(
                    "delete", "groups/" + group_id + "/members/" + user_id, ""
                )
            # simple check to make sure we don't exceed rate limits, this needs improvement!
            # 30 requests per second are permissable and well below actual Edu account limits
            time.sleep(1)

        return result
