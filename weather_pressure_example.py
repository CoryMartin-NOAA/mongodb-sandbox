from __future__ import annotations

import argparse
import os
from datetime import datetime, timezone
from pprint import pprint
from typing import Any


def parse_iso8601(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def build_weather_observation(
    *,
    valid_time: datetime,
    latitude: float,
    longitude: float,
    pressure_hpa: float,
    added_time: datetime | None = None,
) -> dict[str, Any]:
    if valid_time.tzinfo is None:
        valid_time = valid_time.replace(tzinfo=timezone.utc)

    if added_time is None:
        added_time = datetime.now(timezone.utc)
    elif added_time.tzinfo is None:
        added_time = added_time.replace(tzinfo=timezone.utc)

    return {
        "valid_time": valid_time,
        "added_time": added_time,
        "latitude": latitude,
        "longitude": longitude,
        "pressure_hpa": pressure_hpa,
    }


def insert_and_fetch_surface_pressure(collection: Any, observation: dict[str, Any]) -> dict[str, Any]:
    result = collection.insert_one(observation)
    return collection.find_one({"_id": result.inserted_id})


def serialize_for_display(document: dict[str, Any]) -> dict[str, Any]:
    formatted = dict(document)
    if "_id" in formatted:
        formatted["_id"] = str(formatted["_id"])

    for key in ("valid_time", "added_time"):
        value = formatted.get(key)
        if isinstance(value, datetime):
            formatted[key] = value.isoformat()

    return formatted


def get_collection(uri: str, database_name: str, collection_name: str) -> tuple[Any, Any]:
    from pymongo import MongoClient

    client = MongoClient(uri)
    return client, client[database_name][collection_name]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Insert a made-up surface pressure observation into MongoDB and read it back."
    )
    parser.add_argument(
        "--uri",
        default=os.environ.get("MONGODB_URI", "mongodb://localhost:27017/"),
        help="MongoDB connection string.",
    )
    parser.add_argument("--database", default="weather_demo", help="MongoDB database name.")
    parser.add_argument("--collection", default="surface_pressure", help="MongoDB collection name.")
    parser.add_argument(
        "--valid-time",
        default="2026-08-12T12:00:00Z",
        help="Observation valid time in ISO 8601 format.",
    )
    parser.add_argument("--latitude", type=float, default=40.02, help="Observation latitude.")
    parser.add_argument("--longitude", type=float, default=-105.25, help="Observation longitude.")
    parser.add_argument(
        "--pressure-hpa",
        type=float,
        default=1013.2,
        help="Surface pressure in hectopascals.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    observation = build_weather_observation(
        valid_time=parse_iso8601(args.valid_time),
        latitude=args.latitude,
        longitude=args.longitude,
        pressure_hpa=args.pressure_hpa,
    )

    client, collection = get_collection(args.uri, args.database, args.collection)
    try:
        stored_document = insert_and_fetch_surface_pressure(collection, observation)
    finally:
        client.close()

    print("Inserted and fetched document:")
    pprint(serialize_for_display(stored_document))


if __name__ == "__main__":
    main()
