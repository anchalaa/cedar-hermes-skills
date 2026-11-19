"""Audit an exported calendar locally; no network, credentials, or writes."""
import argparse
import json
from datetime import date
from pathlib import Path
from zoneinfo import ZoneInfo

from calendar_logic import analyze, parse_time


def audit(path, day, timezone, minimum):
    if minimum < 1:
        raise ValueError('Minimum focus duration must be positive')
    raw = json.loads(Path(path).read_text(encoding='utf-8'))
    events = raw.get('items') if isinstance(raw, dict) else raw
    if not isinstance(events, list):
        raise ValueError('Expected an event list or an object containing items')
    zone = ZoneInfo(timezone)
    included = []
    for index, event in enumerate(events):
        if not isinstance(event, dict):
            raise ValueError(f'Event {index} must be an object')
        if event.get('status') == 'cancelled' or event.get('transparency') == 'transparent':
            continue
        if event.get('recurrence'):
            raise ValueError(f'Event {index}: expand recurring events before export')
        for endpoint in ['start', 'end']:
            value = event.get(endpoint)
            if not isinstance(value, dict) or sum(k in value for k in ['date', 'dateTime']) != 1:
                raise ValueError(f'Event {index}: {endpoint} needs exactly one date or dateTime')
        if ('date' in event['start']) != ('date' in event['end']):
            raise ValueError(f'Event {index}: start and end must use the same format')
        if parse_time(event['end'], zone) <= parse_time(event['start'], zone):
            raise ValueError(f'Event {index}: end must be after start')
        included.append(event)
    result = analyze(included, day, timezone, minimum)
    result.update(working_window='09:00–17:00', minimum_minutes=minimum,
                  input_events=len(events), blocking_events_in_export=len(included))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--events', required=True)
    parser.add_argument('--date', required=True, type=date.fromisoformat)
    parser.add_argument('--timezone', default='America/Los_Angeles')
    parser.add_argument('--minimum-minutes', type=int, default=60)
    args = parser.parse_args()
    try:
        print(json.dumps(audit(args.events, args.date, args.timezone, args.minimum_minutes), indent=2))
    except (ValueError, KeyError, TypeError, OSError) as error:
        parser.exit(2, f'Calendar audit failed: {error}\n')


if __name__ == '__main__':
    main()
