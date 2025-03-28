import logging
import requests
from typing import List
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class RestAdapter:
    """
    Rest adapter class uses a persistent session and sets default configuration.

    Args:
        base_url (str): The base URL for the API.
        headers (dict): Default headers (optional).
        auth (Any): Authentication information (optional).
        proxies (dict): Dictionary of proxy addresses for HTTP(s) (optional).
        logger (Logger): Custom logger object (optional).
    """

    def __init__(
        self,
        base_url: str = "",
        headers: dict = {},
        auth=None,
        proxies: dict = {},
        logger=None,
    ):
        self.base_url = base_url
        self.logger = logger or logging.getLogger(__name__)

        self.session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        if headers:
            self.session.headers.update(headers)
        if auth:
            self.session.auth = auth
        if proxies:
            self.session.proxies.update(proxies)

    def _send_request(
        self,
        method: str,
        endpoint: str,
        params: dict = {},
        data: dict = {},
        cookies: dict = {},
        verify: bool | str = None,
        timeout: int = None,
        allow_redirects: bool = True,
    ) -> dict | str:
        """
        Prepare the request to be sent. Send the prepared request and return the response.

        Args:
            method (str): HTTP method ('GET', 'POST', etc.).
            endpoint (str): API endpoint (e.g., '/users', '/posts').
            params (dict): URL parameters, defaults to empty dictionary (optional).
            data (dict): Data sent in the request body, defaults to empty dictionary (optional).
            cookies (dict): Cookie data in the request, defaults to empty dictionary (optional).
            verify (bool, str): Boolean whether to enforce SSL authentication, or supply a certificate to use. Defaults to None (optional).
            timeout (int): Number of seconds to wait for a response. Defaults to None (optional).
            allow_redirects (bool): Allow HTTP redirects to different URLs. Defaults to True (optional).

        Returns:
            (dict | str): JSON serialized response body or None if an error occurs.

        Raises:
            requests.exceptions.HTTPError: An HTTP error occurred.
            requests.exceptions.ConnectionError: A connection error occurred.
            requests.exceptions.Timeout: A timeout error occurred.
            requests.exceptions.RequestException: An unexpected error occurred.
        """
        self.logger.debug(f"Request [{method}] - {self.base_url} {endpoint}")
        url = self.base_url + endpoint
        req = requests.Request(
            method,
            url,
            headers=self.session.headers,
            params=params,
            data=data,
            cookies=cookies,
        )
        prep_req = self.session.prepare_request(req)
        try:
            response = self.session.send(
                prep_req,
                verify=verify,
                timeout=timeout,
                allow_redirects=allow_redirects,
            )
            response.raise_for_status()
            self.logger.debug(f"Status [{response.status_code}] - {response.reason}")
            if response:
                content_type = response.headers.get("Content-Type", "").lower()
                if "application/json" in content_type:
                    return response.json()
                elif "text/html" in content_type:
                    return response.text
                else:
                    return response.content
        except requests.exceptions.HTTPError as errh:
            self.logger.error(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            self.logger.error(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            self.logger.error(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            self.logger.error(f"An Unexpected Error: {err}")

    def get(
        self,
        endpoint: str,
        params: dict = None,
        cookies: dict = None,
        verify: bool | str = None,
        timeout: int = None,
        allow_redirects: bool = True,
    ) -> dict:
        """
        Make a GET request.

        Args:
            endpoint (str): API endpoint.
            params (dict): URL parametersm, defaults to None (optional).
            cookies (dict): Cookie data in the request, defaults to None (optional).
            verify (bool, str): Boolean whether to enforce SSL authentication, or supply a certificate to use. Defaults to None (optional).
            timeout (int): Number of seconds to wait for a response. Defaults to None (optional).
            allow_redirects (bool): Allow HTTP redirects to different URLs. Defaults to True (optional).

        Returns:
            dict: JSON serialized response body or None if an error occurs.
        """
        return self._send_request(
            "GET",
            endpoint,
            params=params,
            cookies=cookies,
            verify=verify,
            timeout=timeout,
            allow_redirects=allow_redirects,
        )

    def post(
        self,
        endpoint: str,
        data: dict = None,
        params: dict = None,
        cookies: dict = None,
        verify: bool | str = None,
        timeout: int = None,
        allow_redirects: bool = True,
    ) -> dict:
        """
        Make a POST request.

        Args:
            endpoint (str): API endpoint.
            data (dict): Data sent in the request body, defaults to None (optional).
            params (dict): URL parametersm, defaults to None (optional).
            cookies (dict): Cookie data in the request, defaults to None (optional).
            verify (bool, str): Boolean whether to enforce SSL authentication, or supply a certificate to use. Defaults to None (optional).
            timeout (int): Number of seconds to wait for a response. Defaults to None (optional).
            allow_redirects (bool): Allow HTTP redirects to different URLs. Defaults to True (optional).

        Returns:
            dict: JSON serialized response body or None if an error occurs.
        """
        return self._send_request(
            "POST",
            endpoint,
            data=data,
            params=params,
            cookies=cookies,
            verify=verify,
            timeout=timeout,
            allow_redirects=allow_redirects,
        )

    def put(
        self,
        endpoint: str,
        data: dict = None,
        params: dict = None,
        cookies: dict = None,
        verify: bool | str = None,
        timeout: int = None,
        allow_redirects: bool = True,
    ) -> dict:
        """
        Make a PUT request.

        Args:
            endpoint (str): API endpoint.
            data (dict): Data sent in the request body, defaults to None (optional).
            params (dict): URL parametersm, defaults to None (optional).
            cookies (dict): Cookie data in the request, defaults to None (optional).
            verify (bool, str): Boolean whether to enforce SSL authentication, or supply a certificate to use. Defaults to None (optional).
            timeout (int): Number of seconds to wait for a response. Defaults to None (optional).
            allow_redirects (bool): Allow HTTP redirects to different URLs. Defaults to True (optional).

        Returns:
            dict: JSON serialized response body or None if an error occurs.
        """
        return self._send_request(
            "PUT",
            endpoint,
            data=data,
            params=params,
            cookies=cookies,
            verify=verify,
            timeout=timeout,
            allow_redirects=allow_redirects,
        )

    def delete(
        self,
        endpoint: str,
        params: dict = None,
        cookies: dict = None,
        verify: bool | str = None,
        timeout: int = None,
        allow_redirects: bool = True,
    ) -> dict:
        """
        Make a DELETE request.

        Args:
            endpoint (str): API endpoint.
            params (dict): URL parametersm, defaults to None (optional).
            cookies (dict): Cookie data in the request, defaults to None (optional).
            verify (bool, str): Boolean whether to enforce SSL authentication, or supply a certificate to use. Defaults to None (optional).
            timeout (int): Number of seconds to wait for a response. Defaults to None (optional).
            allow_redirects (bool): Allow HTTP redirects to different URLs. Defaults to True (optional).

        Returns:
            dict: JSON serialized response body or None if an error occurs.
        """
        return self._send_request(
            "DELETE",
            endpoint,
            params=params,
            cookies=cookies,
            verify=verify,
            timeout=timeout,
            allow_redirects=allow_redirects,
        )


class MSGraphApi:
    """
    Class to interact with Microsoft Graph API.

    Args:
        tenant_id (str): The tenant ID for the Azure AD application.
        client_id (str): The client ID for the Azure AD application.
        client_secret (str): The client secret for the Azure AD application.
        logger (Logger): Custom logger object (optional).
    """

    def __init__(self, tenant_id: str, client_id: str, client_secret: str, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.tenant_id = tenant_id
        self.client_id = (client_id,)
        self.client_secret = client_secret

    def request_access_token(
        self,
    ) -> None:
        """
        Uses tenant ID, client ID, and client secret to request an access token with privileges outlined in the application object.
        """
        rest = RestAdapter("https://login.microsoftonline.com", logger=self.logger)
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "https://graph.microsoft.com/.default",
        }
        res = rest.post(f"/{self.tenant_id}/oauth2/v2.0/token", data=data)
        access_token = res.get("access_token")
        headers = {"Authorization": f"Bearer {access_token}"}
        self.rest = RestAdapter(
            "https://graph.microsoft.com/v1.0", headers=headers, logger=self.logger
        )

    def get_group_members(self, group_id: str) -> dict:
        """
        Get all members that belong to a specific group.

        Args:
            group_id (str): GUID of the desired group.

        Returns:
            dict: JSON serialized response body or None if an error occurs.
        """
        endpoint = f"/groups/{group_id}/members"
        return self.rest.get(endpoint)


class TenoviApi:
    """
    Class to interact with Tenovi API.

    Args:
        client_domain (str): The client domain for the Tenovi API.
        api_key (str): The API key for authentication.
        logger (Logger): Custom logger object (optional).
    """

    def __init__(self, client_domain: str, api_key: str, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        headers = {"Authorization": f"Api-Key {api_key}"}
        self.rest = RestAdapter(
            f"https://api2.tenovi.com/clients/{client_domain}",
            headers=headers,
            logger=self.logger,
        )

    def get_devices(
        self,
    ) -> List[dict]:
        """
        Get a list of devices.

        Returns:
            List[dict]: List of devices.
        """
        return self.rest.get("/hwi/hwi-devices")

    def get_readings(
        self, hwi_device_id: str, metric: str = "", created_gte: datetime | str = None
    ) -> List[dict]:
        """
        Get readings for a specific device.

        Args:
            hwi_device_id (str): The hardware ID of the device.
            metric (str): The name of the metric data to filter by (optional).
            created_gte (datetime, str): The earliest creation date to filter by (optional).

        Returns:
            List[dict]: List of readings.
        """
        params = {}
        if metric:
            params["metric__name"] = metric
        if created_gte:
            if not isinstance(created_gte, str):
                created_gte = created_gte.strftime("%Y-%m-%dT%H:%M:%SZ")
            params["created__gte"] = created_gte
        return self.rest.get(
            f"/hwi/hwi-devices/{hwi_device_id}/measurements/", params=params
        )
