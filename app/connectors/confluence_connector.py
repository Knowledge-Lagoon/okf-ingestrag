import requests


class ConfluenceConnector:

    def __init__(
        self,
        base_url,
        username,
        api_token
    ):
        self.base_url = base_url.rstrip("/")

        self.auth = (
            username,
            api_token
        )

    def get_page(self, page_id):

        url = (
            f"{self.base_url}"
            f"/wiki/rest/api/content/{page_id}"
            "?expand=body.storage"
        )

        response = requests.get(
            url,
            auth=self.auth
        )

        response.raise_for_status()

        return response.json()