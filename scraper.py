from datetime import date
import re

from bs4 import BeautifulSoup
from dateutil.parser import parse


def get_all_mega_tasting_events(astor_wine_gateway):
    soup = BeautifulSoup(astor_wine_gateway.get_tastings_index(), "lxml")
    tasting_event_tags = soup.find_all("a", class_="tastingEvent")
    return _build_events_from_tags(tasting_event_tags, astor_wine_gateway)


def _build_events_from_tags(tags, astor_wine_gateway):
    events = []
    for t in tags:
        name = _get_mega_tasting_name(t)
        if not name:
            continue

        description = _get_description_from_tag(t, astor_wine_gateway)
        date_of_event = _get_date_from_description(description)
        events.append({"name": name, "description": description, "date": date_of_event})

    return events


def _get_mega_tasting_name(tasting_event_tag):
    try:
        return next(
            (
                s
                for s in tasting_event_tag.strings
                if re.search("mega.*tasting", s, flags=re.I)
            )
        )
    except StopIteration:
        return None


def _get_description_from_tag(tasting_event_tag, astor_wine_gateway):
    soup = BeautifulSoup(
        astor_wine_gateway.get_tasting(tasting_event_tag["href"]), "lxml"
    )
    description = soup.find("div", class_="supporting-text")

    return "".join(description.strings)


def _get_date_from_description(description):
    weekdays = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    result = re.search(f'{"|".join(weekdays)}, \w+ \d+', description)
    return parse(result.group(0)).date()
