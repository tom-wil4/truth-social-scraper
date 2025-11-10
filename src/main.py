thonimport argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Ensure project root is on sys.path so we can import src.* as a namespace package
CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.extractors.profile_extractor import ProfileExtractor  # type: ignore  # noqa: E402
from src.extractors.posts_extractor import PostsExtractor  # type: ignore  # noqa: E402
from src.extractors.replies_extractor import RepliesExtractor  # type: ignore  # noqa: E402
from src.outputs.data_formatter import (  # type: ignore  # noqa: E402
    format_post,
    format_profile,
    format_reply,
    write_json,
)

def load_settings() -> Dict[str, Any]:
    config_path = CURRENT_FILE.parent / "config" / "settings.json"
    if not config_path.exists():
        raise FileNotFoundError(f"settings.json not found at {config_path}")
    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)

def configure_logging(level: str) -> None:
    log_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Truth Social Scraper - extract public profile, posts, and replies data."
    )
    parser.add_argument(
        "--input",
        "-i",
        help="Single Truth Social username or profile URL (e.g., @realDonaldTrump or https://truthsocial.com/@realDonaldTrump).",
    )
    parser.add_argument(
        "--input-file",
        "-f",
        help="Path to a text file containing usernames or profile URLs, one per line.",
    )
    parser.add_argument(
        "--mode",
        "-m",
        choices=["profile", "posts", "replies", "all"],
        default="all",
        help="What to scrape: profile only, posts only, replies only, or all.",
    )
    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        default=40,
        help="Maximum number of posts/replies to fetch per profile (where applicable).",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Path to output JSON file. Defaults to data/output_<timestamp>.json inside the project.",
    )
    return parser.parse_args()

def load_inputs(args: argparse.Namespace) -> List[str]:
    inputs: List[str] = []
    if args.input:
        inputs.append(args.input.strip())
    if args.input_file:
        file_path = Path(args.input_file)
        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {file_path}")
        with file_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    inputs.append(line)
    if not inputs:
        raise ValueError("No input provided. Use --input or --input-file.")
    return inputs

def build_output_path(args: argparse.Namespace, settings: Dict[str, Any]) -> Path:
    if args.output:
        return Path(args.output).resolve()
    from datetime import datetime

    output_dir_setting = settings.get("output_dir", "data")
    output_dir = PROJECT_ROOT / output_dir_setting
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    return output_dir / f"output_{timestamp}.json"

def main() -> None:
    settings = load_settings()
    configure_logging(settings.get("log_level", "INFO"))
    logger = logging.getLogger("main")

    args = parse_args()

    try:
        inputs = load_inputs(args)
    except Exception as exc:
        logger.error("Failed to load input: %s", exc)
        sys.exit(1)

    base_url = settings.get("base_url", "https://truthsocial.com")
    timeout = settings.get("request_timeout", 15)
    max_retries = settings.get("max_retries", 3)
    backoff_factor = settings.get("backoff_factor", 0.5)

    profile_extractor = ProfileExtractor(
        base_url=base_url,
        timeout=timeout,
        max_retries=max_retries,
        backoff_factor=backoff_factor,
    )
    posts_extractor = PostsExtractor(
        base_url=base_url,
        timeout=timeout,
        max_retries=max_retries,
        backoff_factor=backoff_factor,
    )
    replies_extractor = RepliesExtractor(
        base_url=base_url,
        timeout=timeout,
        max_retries=max_retries,
        backoff_factor=backoff_factor,
    )

    results: List[Dict[str, Any]] = []

    for input_value in inputs:
        logger.info("Processing input: %s", input_value)
        try:
            raw_profile: Optional[Dict[str, Any]] = None
            if args.mode in ("profile", "posts", "replies", "all"):
                raw_profile = profile_extractor.fetch_profile(input_value)
                if raw_profile is None:
                    logger.warning("No profile data found for input: %s", input_value)
                    continue

            if args.mode in ("profile", "all"):
                profile_obj = format_profile(raw_profile, input_value)
                results.append(profile_obj)

            account_id = raw_profile.get("id") if raw_profile else None
            username = raw_profile.get("username") if raw_profile else None

            if not account_id or not username:
                if args.mode in ("posts", "replies", "all"):
                    logger.warning(
                        "Account ID or username missing for input %s; skipping posts/replies.",
                        input_value,
                    )
                continue

            if args.mode in ("posts", "all"):
                raw_posts = posts_extractor.fetch_posts(account_id=account_id, limit=args.limit)
                for post in raw_posts:
                    results.append(format_post(post, username=username, account_id=account_id))

            if args.mode in ("replies", "all"):
                raw_replies = replies_extractor.fetch_replies(
                    account_id=account_id, limit=args.limit
                )
                for reply in raw_replies:
                    results.append(
                        format_reply(reply, username=username, account_id=account_id)
                    )

        except Exception as exc:
            logger.exception(
                "Unexpected error while processing input %s: %s", input_value, exc
            )

    if not results:
        logger.warning("No data was collected; exiting without writing output.")
        sys.exit(0)

    output_path = build_output_path(args, settings)
    try:
        write_json(results, output_path)
        logger.info("Scraping complete. Output written to %s", output_path)
    except Exception as exc:
        logger.error("Failed to write output JSON: %s", exc)
        sys.exit(1)

if __name__ == "__main__":
    main()