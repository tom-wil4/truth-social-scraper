thonimport json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

def _get_bool(value: Any) -> Optional[bool]:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        v = value.strip().lower()
        if v in {"true", "yes", "1"}:
            return True
        if v in {"false", "no", "0"}:
            return False
    return None

def _safe_int(value: Any) -> Optional[int]:
    if isinstance(value, int):
        return value
    try:
        return int(value)
    except (TypeError, ValueError):
        return None

def _extract_profile_url(raw: Dict[str, Any]) -> Optional[str]:
    if "url" in raw:
        return raw.get("url")
    return raw.get("profile_url")

def _extract_website(raw: Dict[str, Any]) -> Optional[str]:
    # Truth Social / Mastodon-style profiles may store website in 'fields' or 'website'
    if "website" in raw:
        return raw.get("website")

    fields = raw.get("fields") or []
    if isinstance(fields, list):
        for field in fields:
            if not isinstance(field, dict):
                continue
            name = str(field.get("name", "")).strip().lower()
            if name in {"website", "site", "url"}:
                return field.get("value")
    return None

def format_profile(raw_profile: Dict[str, Any], input_value: str) -> Dict[str, Any]:
    """
    Normalize profile payload into the documented JSON structure.
    """
    username = raw_profile.get("username") or raw_profile.get("acct")
    display_name = raw_profile.get("display_name") or raw_profile.get("displayName")
    description = raw_profile.get("note") or raw_profile.get("description")

    followers = _safe_int(
        raw_profile.get("followers_count") or raw_profile.get("followersCount")
    )
    following = _safe_int(
        raw_profile.get("following_count") or raw_profile.get("followingCount")
    )
    posts_and_replies = _safe_int(
        raw_profile.get("statuses_count") or raw_profile.get("postsAndRepliesCount")
    )

    verified = _get_bool(raw_profile.get("verified"))

    profile_obj: Dict[str, Any] = {
        "input": input_value,
        "id": raw_profile.get("id"),
        "url": _extract_profile_url(raw_profile),
        "username": username,
        "displayName": display_name,
        "description": description,
        "website": _extract_website(raw_profile),
        "avatar": raw_profile.get("avatar"),
        "header": raw_profile.get("header"),
        "followersCount": followers,
        "followingCount": following,
        "postsAndRepliesCount": posts_and_replies,
        "createdAt": raw_profile.get("created_at") or raw_profile.get("createdAt"),
        "verified": verified,
    }
    return profile_obj

def _extract_media_attachments(raw_status: Dict[str, Any]) -> List[Dict[str, Any]]:
    media_items: List[Dict[str, Any]] = []
    attachments = raw_status.get("media_attachments") or raw_status.get("mediaAttachments") or []
    if not isinstance(attachments, list):
        return media_items

    for item in attachments:
        if not isinstance(item, dict):
            continue
        media_items.append(
            {
                "id": item.get("id"),
                "type": item.get("type"),
                "url": item.get("url"),
                "previewUrl": item.get("preview_url") or item.get("previewUrl"),
            }
        )
    return media_items

def _base_status_fields(
    raw_status: Dict[str, Any], username: str, account_id: str
) -> Dict[str, Any]:
    replies_count = _safe_int(
        raw_status.get("replies_count") or raw_status.get("repliesCount")
    )
    reblogs_count = _safe_int(
        raw_status.get("reblogs_count") or raw_status.get("reblogsCount")
    )
    favourites_count = _safe_int(
        raw_status.get("favourites_count")
        or raw_status.get("favorites_count")
        or raw_status.get("favouritesCount")
        or raw_status.get("favoritesCount")
    )

    return {
        "id": raw_status.get("id"),
        "accountId": account_id,
        "username": username,
        "createdAt": raw_status.get("created_at") or raw_status.get("createdAt"),
        "url": raw_status.get("url"),
        "content": raw_status.get("content"),
        "mediaAttachments": _extract_media_attachments(raw_status),
        "repliesCount": replies_count,
        "reblogsCount": reblogs_count,
        "favouritesCount": favourites_count,
    }

def format_post(raw_status: Dict[str, Any], username: str, account_id: str) -> Dict[str, Any]:
    """
    Normalize an original post into the documented JSON structure.
    """
    base = _base_status_fields(raw_status, username, account_id)
    base["type"] = "post"
    return base

def format_reply(raw_status: Dict[str, Any], username: str, account_id: str) -> Dict[str, Any]:
    """
    Normalize a reply into the documented JSON structure.
    """
    base = _base_status_fields(raw_status, username, account_id)
    base["type"] = "reply"
    return base

def write_json(data: Any, output_path: Path) -> None:
    """
    Serialize data to JSON at output_path, creating parent directories as needed.
    """
    output_path = output_path.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    logger.info("Writing %s records to %s", len(data) if isinstance(data, list) else "N/A", output_path)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)