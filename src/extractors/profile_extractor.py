thonimport logging
import re
import time
from typing import Any, Dict, Optional
from urllib.parse import urlparse

import requests

class ProfileExtractor:
    """
    Fetches profile details from the Truth Social platform.

    This implementation targets a Mastodon-compatible API shape but is
    defensive enough to handle minor variations in field names.
    """

    def __init__(
        self,
        base_url: str,
        timeout: int = 15,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
        session: Optional[requests.Session] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.session = session or requests.Session()
        self.logger = logger or logging.getLogger(self.__class__.__name__)

    def _extract_username(self, identifier: str) -> str:
        """
        Normalize the identifier into a username.

        Accepts:
        - @username
        - username
        - https://truthsocial.com/@username
        - https://truthsocial.com/users/username
        """
        identifier = identifier.strip()

        if identifier.startswith("@"):
            return identifier[1:]

        if identifier.startswith("http://") or identifier.startswith("https://"):
            parsed = urlparse(identifier)
            path = parsed.path or ""
            # Try @username-style path
            match = re.search(r"@([^/]+)", path)
            if match:
                return match.group(1)
            # Fallback: last non-empty segment
            segments = [p for p in path.split("/") if p]
            if segments:
                return segments[-1]

        # Fallback: assume it's already a username
        return identifier

    def _request(self, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Perform an HTTP GET with simple retry and backoff.
        """
        params = params or {}
        attempt = 0
        last_exception: Optional[Exception] = None

        while attempt <= self.max_retries:
            try:
                response = self.session.get(url, params=params, timeout=self.timeout)
                if 200 <= response.status_code < 300:
                    return response.json()
                self.logger.warning(
                    "Non-success HTTP status %s from %s. Body: %s",
                    response.status_code,
                    response.url,
                    response.text[:500],
                )
            except (requests.RequestException, ValueError) as exc:
                last_exception = exc
                self.logger.warning(
                    "Request error on attempt %s for %s: %s", attempt + 1, url, exc
                )

            attempt += 1
            if attempt <= self.max_retries:
                sleep_for = self.backoff_factor * (2 ** (attempt - 1))
                time.sleep(sleep_for)

        if last_exception:
            raise last_exception
        raise RuntimeError(f"Failed to fetch data from {url} after {self.max_retries} retries")

    def fetch_profile(self, identifier: str) -> Optional[Dict[str, Any]]:
        """
        Fetch a single profile by username or URL.

        Returns a JSON-like dict if successful, otherwise None.
        """
        username = self._extract_username(identifier)
        if not username:
            self.logger.error("Could not resolve username from identifier: %s", identifier)
            return None

        url = f"{self.base_url}/api/v1/accounts/lookup"
        params = {"acct": username}
        self.logger.info("Fetching profile for username '%s' from %s", username, url)

        try:
            profile = self._request(url, params=params)
        except Exception as exc:
            self.logger.error("Failed to fetch profile '%s': %s", username, exc)
            return None

        if not isinstance(profile, dict):
            self.logger.warning(
                "Unexpected profile payload type for '%s': %s", username, type(profile)
            )
            return None

        # Ensure some required fields exist; otherwise consider it invalid.
        if "username" not in profile and "acct" not in profile:
            self.logger.warning("Profile payload for '%s' missing username/acct field", username)
            return None

        return profile