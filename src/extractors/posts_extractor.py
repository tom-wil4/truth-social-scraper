thonimport logging
import time
from typing import Any, Dict, List, Optional

import requests

class PostsExtractor:
    """
    Fetches original posts ("truths") for a given Truth Social account.

    Uses a Mastodon-style statuses endpoint. It excludes replies by default.
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

    def _request(self, url: str, params: Optional[Dict[str, Any]] = None) -> Any:
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

    def fetch_posts(self, account_id: str, limit: int = 40) -> List[Dict[str, Any]]:
        """
        Fetch original posts for an account, excluding replies.

        :param account_id: Truth Social internal account ID
        :param limit: Maximum number of posts to fetch
        """
        url = f"{self.base_url}/api/v1/accounts/{account_id}/statuses"
        params: Dict[str, Any] = {
            "limit": max(1, min(limit, 80)),  # clamp to a reasonable range
            "exclude_replies": "true",
        }
        self.logger.info(
            "Fetching up to %s posts for account_id=%s from %s", params["limit"], account_id, url
        )

        try:
            payload = self._request(url, params=params)
        except Exception as exc:
            self.logger.error("Failed to fetch posts for account_id=%s: %s", account_id, exc)
            return []

        if not isinstance(payload, list):
            self.logger.warning(
                "Unexpected posts payload type for account_id=%s: %s",
                account_id,
                type(payload),
            )
            return []

        # Filter out anything that looks like a reply, just in case
        posts: List[Dict[str, Any]] = []
        for item in payload:
            if not isinstance(item, dict):
                continue
            if item.get("in_reply_to_id") is None and item.get("in_reply_to_account_id") is None:
                posts.append(item)

        return posts