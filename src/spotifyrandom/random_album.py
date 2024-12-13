import random
from pathlib import Path

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from toga import ProgressBar
from toga.style.pack import HIDDEN, VISIBLE

from spotifyrandom import env


SCOPE = "user-library-read"


def extract_album(items: list) -> list:
    albums = []
    for item in items:
        album = item["album"]
        artists = [artist["name"] for artist in album["artists"]]
        albums.append({"artist": " // ".join(artists), "name": album["name"]})
    return albums


def set_up_progress_bar(progress, max_value, value) -> None:
    progress.max = max_value
    progress.value = value
    progress.style.visibility = VISIBLE
    progress.start()
    progress.refresh()


def tear_down_progress_bar(progress) -> None:
    progress.stop()
    progress.style.visibility = HIDDEN
    progress.value = 0
    progress.refresh()


def get_albums(sp, progress: ProgressBar | None = None) -> list[dict]:
    albums = []
    print("Getting initial results")
    results = sp.current_user_saved_albums(limit=50)
    albums.extend(extract_album(results["items"]))
    if progress:
        set_up_progress_bar(progress, results["total"], len(results["items"]))
    while results["next"]:
        print(f"Getting {results['limit'] + results['offset']} of {results['total']}")
        results = sp.next(results)
        albums.extend(extract_album(results["items"]))
        if progress:
            progress.value += len(results["items"])
        break
    if progress:
        tear_down_progress_bar(progress)
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
