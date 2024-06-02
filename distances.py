import os
import random
import requests
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()


def get_shortest_distance(
    api_key, origin, destination, country="poland", mode="driving"
) -> int:
    url = "https://maps.googleapis.com/maps/api/directions/json"
    if country:
        origin += ", " + country
        destination += ", " + country

    params = {
        "origin": origin,
        "destination": destination,
        "key": api_key,
        "mode": mode,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        directions = response.json()
        if directions["status"] == "OK":
            route = directions["routes"][0]
            leg = route["legs"][0]
            return leg["distance"]["value"] / 1000.0
        else:
            return None
    else:
        return None


DISTANCES = defaultdict(dict)
CACHE = {}
CITIES = """
szczecin: zielona-gora,gdansk,torun,poznan
gdansk: szczecin, torun, olsztyn
olsztyn: gdansk, torun, bialystok, warszawa
bialystok:olsztyn,warszawa
zielona-gora: szczecin, poznan, wroclaw
poznan: zielona-gora,szczecin,torun,lodz,opole
torun:szczecin,gdansk,olsztyn,warszawa,lodz,poznan
warszawa: lodz, torun, olsztyn, bialystok, lublin, kielce
lublin: warszawa,kielce,rzeszow
wroclaw:zielona-gora,poznan,lodz,opole
opole: wroclas,poznan,lodz,katowice
lodz:poznan,torun,warszawa,kielce,katowice,opole,wroclaw
katowice:opole,lodz,kielce,krakow
kielce:lodz,warszawa,lublin,rzeszow,krakow,katowice
krakow:katowice,kielce,rzeszow
rzeszow:krakow,kielce,lublin
"""


def get_cities():
    for row in CITIES.split("\n"):
        if not row:
            continue

        city, connections = row.split(":")
        city = city.strip()
        for c in connections.split(","):
            c = c.strip()
            yield city, c


# Example usage
if __name__ == "__main__":
    api_key = os.getenv("API_KEY")
    origin = "zielona-gora"
    destination = "poznan"

    for city, c in get_cities():
        if f"{c}-{city}" in CACHE:
            DISTANCES[city][c] = CACHE[f"{c}-{city}"]

        DISTANCES[city][c] = CACHE[f"{c}-{city}"] = get_shortest_distance(
            api_key, city, c, country="poland"
        )
        break

    print(dict(DISTANCES))
