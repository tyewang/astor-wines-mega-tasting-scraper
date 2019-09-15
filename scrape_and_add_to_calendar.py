from datetime import datetime, time
import os
import pickle

import redis

import astor_wine_gateway
import scraper


redis_instance = redis.from_url(os.environ["REDIS_URL"], decode_responses=True)


if __name__ == "__main__":
    mega_tastings = scraper.get_all_mega_tasting_events(astor_wine_gateway)
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

        for pickled_session in redis_instance.lrange(
            "authorized.google.sessions", 0, -1
        ):
            session = pickle.loads(pickled_session)
            session.post("calendar/v3/calendars/primary/events", event)
