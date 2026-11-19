"""Timezone-aware, deterministic conflicts and merged schedule gaps."""
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo


def parse_time(value, tz):
    if "dateTime" in value:
        dt = datetime.fromisoformat(value["dateTime"].replace("Z", "+00:00"))
        return dt.replace(tzinfo=tz) if dt.tzinfo is None else dt.astimezone(tz)
    return datetime.combine(datetime.fromisoformat(value["date"]).date(), time.min, tzinfo=tz)


def analyze(events, day, zone="America/Los_Angeles", minimum_minutes=30):
    tz = ZoneInfo(zone)
    begin = datetime.combine(day, time(9), tzinfo=tz)
    end = datetime.combine(day, time(17), tzinfo=tz)
    busy = []
    for e in events:
        if e.get("status") == "cancelled" or e.get("transparency") == "transparent":
            continue
        a, b = parse_time(e["start"], tz), parse_time(e["end"], tz)
        if b > begin and a < end:
            busy.append((max(a, begin), min(b, end), e.get("summary", "Untitled")))
    busy.sort()
    conflicts = [{"first": x[2], "second": y[2]} for i, x in enumerate(busy)
                 for y in busy[i+1:] if y[0] < x[1]]
    cursor, gaps = begin, []
    for a, b, _ in busy + [(end, end, "")]:
        if a - cursor >= timedelta(minutes=minimum_minutes):
            gaps.append({"start": cursor.isoformat(), "end": a.isoformat(),
                         "minutes": int((a-cursor).total_seconds()/60)})
        cursor = max(cursor, b)
    return {"date": day.isoformat(), "timezone": zone, "conflicts": conflicts, "gaps": gaps}
