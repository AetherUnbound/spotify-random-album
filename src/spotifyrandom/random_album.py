import random
from pathlib import Path

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from spotifyrandom import env


SCOPE = "user-library-read"


def extract_album(items: list) -> list:
    albums = []
    for item in items:
        album = item["album"]
        artists = [artist["name"] for artist in album["artists"]]
        albums.append({"artist": " // ".join(artists), "name": album["name"]})
    return albums


def get_albums(sp) -> list[dict]:
    albums = []
    print("Getting initial results")
    results = sp.current_user_saved_albums(limit=50)
    albums.extend(extract_album(results["items"]))
    while results["next"]:
        print(f"Getting {results['limit'] + results['offset']} of {results['total']}")
        results = sp.next(results)
        albums.extend(extract_album(results["items"]))
    return albums


def get_client():
    oauth = SpotifyOAuth(
        client_id=env.SPOTIPY_CLIENT_ID,
        client_secret=env.SPOTIPY_CLIENT_SECRET,
        redirect_uri=env.SPOTIPY_REDIRECT_URI,
        scope=SCOPE,
        cache_path=Path(__file__).parent / "resources" / "cache-spotipy.json",
    )
    return spotipy.Spotify(auth_manager=oauth)


def get_random_album(albums) -> dict:
    return albums[random.randint(0, len(albums) - 1)]
