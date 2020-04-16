import logging
from datetime import datetime, timedelta


class report:
    def __init__(self, controller, *args, **kwargs):
        self.zoom = controller

    def get_daily_report_current_month(self):
        """
        Finds Zoom daily report information for current month

        returns:
            resulting response from the Zoom web api request with dates in the format:
            {'date': '2018-07-01', 'new_users': 1, 'meetings': 1, 'participants': 1, 'meeting_minutes': 1}
        """
        year = str(int(datetime.now().strftime("%Y")))
        month = str(int(datetime.now().strftime("%m")))

        result = self.zoom.api_client.do_request(
            "get", "report/daily", {"year": year, "month": month}
        )

        return result

    def get_daily_report_yesterday(self):
        """
        Finds Zoom daily report information for yesterday

        returns:
            resulting response from the Zoom web api request in the format:
            {'date': '2018-07-01', 'new_users': 1, 'meetings': 1, 'participants': 1, 'meeting_minutes': 1}
        """
        today = datetime.now()
        yesterday = today - timedelta(1)
        yesterday_str = yesterday.strftime("%Y-%m-%d")

        year = str(int(yesterday.strftime("%Y")))
        month = str(int(yesterday.strftime("%m")))

        result = self.zoom.api_client.do_request(
            "get", "report/daily", {"year": year, "month": month}
        )

        for item in result["dates"]:
            if item["date"] == yesterday_str:
                return item

        return {}
