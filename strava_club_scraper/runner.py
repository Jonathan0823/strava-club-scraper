"""Command-line runner for scraping Strava club activities."""

import argparse
import configparser
from pathlib import Path

from .strava_club_scraper import strava_club_activities


TIMEZONE_ALIASES = {
    "WIB": "Asia/Jakarta",
    "WITA": "Asia/Makassar",
    "WIT": "Asia/Jayapura",
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("settings/config.ini"))
    parser.add_argument("--output", type=Path, default=Path("output/club_activities.csv"))
    args = parser.parse_args(argv)

    config = configparser.ConfigParser()
    if not config.read(args.config, encoding="utf-8"):
        parser.error(f"Config file not found: {args.config}")

    general = config["GENERAL"]
    strava = config["STRAVA"]
    club_ids = [club_id.strip() for club_id in strava["CLUB_IDS"].split(",") if club_id.strip()]
    timezone = TIMEZONE_ALIASES.get(general.get("TIMEZONE", "UTC").upper(), general.get("TIMEZONE", "UTC"))
    activity_types = general.get("ACTIVITIES_TYPE")
    activity_types = [item.strip() for item in activity_types.split(",") if item.strip()] if activity_types else None

    print("A Chrome window will open. Log in manually, complete verification, then press Enter in this PowerShell window.")
    activities = strava_club_activities(
        strava_login="",
        strava_password="",
        club_ids=club_ids,
        filter_activities_type=activity_types,
        filter_date_min=general["DATE_MIN"],
        filter_date_max=general["DATE_MAX"],
        timezone=timezone,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    activities.to_csv(args.output, index=False)
    print(f"Saved {len(activities)} activities to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
