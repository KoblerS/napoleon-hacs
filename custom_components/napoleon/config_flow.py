"""Config flow for Napoleon Grill integration."""
import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
)

from .api import AuthenticationError, NapoleonAylaApi
from .const import CONF_EMAIL, CONF_PASSWORD, CONF_REGION, DEFAULT_REGION, DOMAIN, REGIONS

_LOGGER = logging.getLogger(__name__)

AUTH_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_EMAIL): TextSelector(
            TextSelectorConfig(type=TextSelectorType.EMAIL)
        ),
        vol.Required(CONF_PASSWORD): TextSelector(
            TextSelectorConfig(type=TextSelectorType.PASSWORD)
        ),
        vol.Required(CONF_REGION, default=DEFAULT_REGION): SelectSelector(
            SelectSelectorConfig(options=list(REGIONS.keys()))
        ),
    }
)


async def validate_auth(email: str, password: str, region: str) -> dict[str, Any]:
    """Validate credentials against the Ayla Networks API."""
    api = NapoleonAylaApi(email, password, region)
    return await api.authenticate()


class NapoleonConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Napoleon Grill config flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                region = user_input.get(CONF_REGION, DEFAULT_REGION)
                auth_data = await validate_auth(
                    user_input[CONF_EMAIL], user_input[CONF_PASSWORD], region
                )
                return self.async_create_entry(
                    title=user_input[CONF_EMAIL],
                    data={
                        CONF_EMAIL: user_input[CONF_EMAIL],
                        CONF_PASSWORD: user_input[CONF_PASSWORD],
                        CONF_REGION: region,
                        "access_token": auth_data["access_token"],
                        "refresh_token": auth_data["refresh_token"],
                    },
                )
            except AuthenticationError:
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception("Unexpected error during config flow")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=AUTH_SCHEMA, errors=errors
        )
