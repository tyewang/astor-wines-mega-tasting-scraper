from datetime import date
from unittest import TestCase

from scraper import get_all_mega_tasting_events
from tests import astor_wine_gateway_with_fixtures


class ScraperTest(TestCase):
    def test_get_all_mega_tasting_events(self):
        events = get_all_mega_tasting_events(astor_wine_gateway_with_fixtures)

        self.assertEqual(events[0]["name"], "New World Wine Mega Tasting")
        self.assertTrue(
            "Why get stuck in Europe when there's a whole world of wine out there"
            in events[0]["description"]
        )
        self.assertEqual(events[0]["date"], date(2019, 9, 18))
