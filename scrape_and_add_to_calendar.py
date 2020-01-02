from datetime import datetime, time
import json
import os

import redis
from requests_oauthlib import OAuth2Session

import astor_wine_gateway
import scraper


redis_instance = redis.from_url(os.environ["REDIS_URL"], decode_responses=True)
GOOGLE_CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]


if __name__ == "__main__":
    mega_tastings = scraper.get_all_mega_tasting_events(astor_wine_gateway)
    if mega_tastings:
        print(f"Found {len(mega_tastings)} mega tastings!")

    for mt in mega_tastings:
        event = {
            "summary": mt["name"],
            "location": "399 Lafayette St, New York, NY 10003",
            "description": mt["description"],
            "start": {
                "dateTime": datetime.combine(mt["date"], time(hour=17)).isoformat(),
                "timeZone": "America/New_York",
            },
            "end": {
                "dateTime": datetime.combine(mt["date"], time(hour=20)).isoformat(),
                "timeZone": "America/New_York",
            },
        }

        for token in redis_instance.smembers("authorized.google.tokens"):
            google = OAuth2Session(GOOGLE_CLIENT_ID, token=json.loads(token))
            google.post(
                "https://www.googleapis.com/calendar/v3/calendars/primary/events", event
            )
