import os
import json
import random
import requests
from collections import defaultdict
from dotenv import load_dotenv
from typing import Iterator, Tuple

load_dotenv()


class DistanceFinder:
    def __init__(
        self, cities_path: str, api_key: str, country: str = None, mode: str = "driving"
    ):
        """
        Args:
            - `cities_path`: path to a txt file with cities in format: city: city1,city2\ncity2: city1,...
            - `api_key`: Google Maps API key
        """

        self._url = "https://maps.googleapis.com/maps/api/directions/json"

        self.api_key = api_key
        self.cities_path = cities_path
        self.country = country
        self.mode = mode

        self.distances = defaultdict(dict)
        self._cache = {}

    def _get_shortest_distance(self, origin, destination) -> int:
        if self.country:
            origin += ", " + self.country
            destination += ", " + self.country

        params = {
            "origin": origin,
            "destination": destination,
            "key": self.api_key,
            "mode": self.mode,
        }

        response = requests.get(self._url, params=params)
        if response.status_code == 200:
            directions = response.json()
            if directions["status"] == "OK":
                route = directions["routes"][0]
                leg = route["legs"][0]
                return round(leg["distance"]["value"] / 1000.0)
            else:
                return None
        else:
            return None

    def _get_cities(self) -> Iterator[Tuple[str, str]]:
        """Get cities from file"""

        with open(self.cities_path, "r") as f:
            for row in f.readlines():
                if not row:
                    continue

                city, connections = row.split(":")
                city = city.strip()
                for c in connections.split(","):
                    c = c.strip()
                    yield city, c

    def find(self, save_file=None) -> None:
        """Find shortest distances between cities"""

        for city, conn in self._get_cities():
            if f"{conn}-{city}" in self._cache:
                self.distances[city][conn] = self._cache[f"{conn}-{city}"]

            self.distances[city][conn] = self._cache[f"{conn}-{city}"] = (
                self._get_shortest_distance(city, conn)
            )

        if save_file:
            with open(save_file, "w") as f:
                json.dump(self.distances, f, indent=4)


if __name__ == "__main__":
    api_key = os.getenv("API_KEY")
    cities_path = os.path.join(os.getcwd(), "cities.txt")

    finder = DistanceFinder(cities_path=cities_path, api_key=api_key)
    finder.find(save_file="distances.json")
