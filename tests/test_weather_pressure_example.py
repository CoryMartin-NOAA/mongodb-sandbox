from datetime import datetime, timezone
from types import SimpleNamespace
import unittest

from weather_pressure_example import (
    build_weather_observation,
    insert_and_fetch_surface_pressure,
    serialize_for_display,
)


class FakeCollection:
    def __init__(self) -> None:
        self.saved_document = None

    def insert_one(self, document):
        self.saved_document = dict(document, _id="example-id")
        return SimpleNamespace(inserted_id="example-id")

    def find_one(self, query):
        if query == {"_id": "example-id"}:
            return self.saved_document
        return None


class WeatherPressureExampleTests(unittest.TestCase):
    def test_build_weather_observation_contains_required_fields(self):
        valid_time = datetime(2026, 8, 12, 12, 0, tzinfo=timezone.utc)
        added_time = datetime(2026, 8, 12, 12, 5, tzinfo=timezone.utc)

        observation = build_weather_observation(
            valid_time=valid_time,
            added_time=added_time,
            latitude=39.74,
            longitude=-104.99,
            pressure_hpa=1008.4,
        )

        self.assertEqual(observation["valid_time"], valid_time)
        self.assertEqual(observation["added_time"], added_time)
        self.assertEqual(observation["latitude"], 39.74)
        self.assertEqual(observation["longitude"], -104.99)
        self.assertEqual(observation["pressure_hpa"], 1008.4)

    def test_insert_and_fetch_surface_pressure_round_trips_document(self):
        collection = FakeCollection()
        observation = build_weather_observation(
            valid_time=datetime(2026, 8, 12, 12, 0, tzinfo=timezone.utc),
            added_time=datetime(2026, 8, 12, 12, 1, tzinfo=timezone.utc),
            latitude=35.0,
            longitude=-97.0,
            pressure_hpa=1005.6,
        )

        stored_document = insert_and_fetch_surface_pressure(collection, observation)

        self.assertEqual(stored_document["_id"], "example-id")
        self.assertEqual(stored_document["pressure_hpa"], 1005.6)

    def test_serialize_for_display_formats_datetimes_and_object_id(self):
        document = {
            "_id": 123,
            "valid_time": datetime(2026, 8, 12, 12, 0, tzinfo=timezone.utc),
            "added_time": datetime(2026, 8, 12, 12, 1, tzinfo=timezone.utc),
        }

        formatted = serialize_for_display(document)

        self.assertEqual(formatted["_id"], "123")
        self.assertEqual(formatted["valid_time"], "2026-08-12T12:00:00+00:00")
        self.assertEqual(formatted["added_time"], "2026-08-12T12:01:00+00:00")


if __name__ == "__main__":
    unittest.main()
