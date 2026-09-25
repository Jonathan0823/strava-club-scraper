"""Command-line runner for scraping Strava club activities."""

import argparse
from pathlib import Path

from .strava_club_scraper import strava_club_activities


TIMEZONE_ALIASES = {
    'WIB': 'Asia/Jakarta',
    'WITA': 'Asia/Makassar',
    'WIT': 'Asia/Jayapura',
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--club-id', dest='club_ids', action='append', required=True, help='Club ID; repeat for multiple clubs')
    parser.add_argument('--date-min', required=True, help='First activity date, YYYY-MM-DD')
    parser.add_argument('--date-max', required=True, help='Last activity date, YYYY-MM-DD')
    parser.add_argument('--timezone', default='WIB', help='Timezone, e.g. WIB or Asia/Jakarta (default: WIB)')
    parser.add_argument('--num-entries', type=int, default=100, help='Number of feed entries to request (default: 100)')
    parser.add_argument('--activity-request-delay', type=float, default=5, help='Seconds between activity requests (default: 5)')
    parser.add_argument('--rate-limit-retries', type=int, default=3, help='Retries after rate limiting (default: 3)')
    parser.add_argument('--activity-type', dest='activity_types', action='append', help='Activity type; repeat to filter multiple types')
    parser.add_argument('--output', type=Path, default=Path('output/club_activities.csv'))
    args = parser.parse_args(argv)
    if args.num_entries < 1:
        parser.error('--num-entries must be greater than 0')
    if args.activity_request_delay < 0:
        parser.error('--activity-request-delay must not be negative')
    if not 0 <= args.rate_limit_retries <= 3:
        parser.error('--rate-limit-retries must be between 0 and 3')

    timezone = TIMEZONE_ALIASES.get(args.timezone.upper(), args.timezone)
    print('Log in manually in the Selenium Chrome window if needed, complete verification, then press Enter here.')
    activities = strava_club_activities(
        strava_login='',
        strava_password='',
        club_ids=args.club_ids,
        filter_activities_type=args.activity_types,
        filter_date_min=args.date_min,
        filter_date_max=args.date_max,
        timezone=timezone,
        num_entries=args.num_entries,
        activity_request_delay=args.activity_request_delay,
        rate_limit_retries=args.rate_limit_retries,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    activities.to_csv(args.output, index=False)
    print(f'Saved {len(activities)} activities to {args.output}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
