"""Ayla Networks API client for Napoleon grills."""
import logging
from typing import Any

import aiohttp

from .const import DEFAULT_REGION, REGIONS

_LOGGER = logging.getLogger(__name__)


class NapoleonAylaApi:
    """Client for the Ayla Networks API used by Napoleon grills."""

    def __init__(self, email: str, password: str, region: str = DEFAULT_REGION) -> None:
        self._email = email
        self._password = password
        self._region_config = REGIONS[region]
        self._access_token: str | None = None
        self._refresh_token: str | None = None

    @property
    def access_token(self) -> str | None:
        return self._access_token

    @property
    def refresh_token(self) -> str | None:
        return self._refresh_token

    def set_tokens(self, access_token: str, refresh_token: str) -> None:
        self._access_token = access_token
        self._refresh_token = refresh_token

    async def authenticate(self) -> dict[str, Any]:
        """Authenticate and obtain access/refresh tokens."""
        url = f"{self._region_config['base_url_user']}/users/sign_in.json"
        payload = {
            "user": {
                "email": self._email,
                "application": {
                    "app_id": self._region_config["app_id"],
                    "app_secret": self._region_config["app_secret"],
                },
                "password": self._password,
            }
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                if resp.status != 200:
                    body = await resp.text()
                    _LOGGER.error("Authentication failed: %s %s", resp.status, body)
                    raise AuthenticationError(f"Authentication failed: {resp.status}")
                data = await resp.json()
                self._access_token = data["access_token"]
                self._refresh_token = data["refresh_token"]
                return data

    async def get_devices(self) -> list[dict[str, Any]]:
        """Get all devices for the authenticated user."""
        return await self._request(
            "GET", f"{self._region_config['base_url_ads']}/apiv1/devices.json"
        )

    async def get_device_properties(self, dsn: str) -> list[dict[str, Any]]:
        """Get all properties for a device by DSN."""
        return await self._request(
            "GET",
            f"{self._region_config['base_url_ads']}/apiv1/dsns/{dsn}/properties.json",
        )

    async def _request(self, method: str, url: str) -> Any:
        """Make an authenticated API request with automatic token refresh."""
        headers = {"Authorization": f"auth_token {self._access_token}"}

        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=headers) as resp:
                if resp.status == 401:
                    _LOGGER.debug("Token expired, re-authenticating")
                    await self.authenticate()
                    headers["Authorization"] = f"auth_token {self._access_token}"
                    async with session.request(method, url, headers=headers) as retry:
                        if retry.status != 200:
                            raise ApiError(f"Request failed: {retry.status}")
                        return await retry.json()
                if resp.status != 200:
                    raise ApiError(f"Request failed: {resp.status}")
                return await resp.json()


class AuthenticationError(Exception):
    pass


class ApiError(Exception):
    pass
