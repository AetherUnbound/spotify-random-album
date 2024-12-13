"""
A small app which chooses a random album to play from your liked album library.
"""

import json

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER, ROW, BOTTOM

from . import random_album


CACHE_FILE = "album-cache.json"


class SpotifyRandomAlbumPicker(toga.App):
    def startup(self):
        print("Creating client")
        self._sp_client = random_album.get_client()

        self.albums = []
        self._album_cache = self.paths.cache / CACHE_FILE
        if self._album_cache.exists():
            print("Loading albums from cache")
            try:
                self.albums = json.loads(self._album_cache.read_text())
            except json.JSONDecodeError:
                print("Failed to load cache, loading albums")
        if not self.albums:
            print("Loading albums")
            self.albums = random_album.get_albums(self._sp_client)
            self.save_to_cache()

        main_box = toga.Box(style=Pack(direction=COLUMN))

        # Main content
        self.button_get_album = toga.Button(
            "Get a random album",
            on_press=self.get_album,
            style=Pack(padding=10),
        )

        self.artist_label = toga.Label(
            "",
            style=Pack(
                direction=ROW,
                padding=(30, 10, 5),
                text_align=CENTER,
                alignment=CENTER,
                font_weight="bold",
                font_size=18,
                flex=1,
            ),
        )
        self.album_label = toga.Label(
            "",
            style=Pack(
                direction=ROW,
                padding=(5, 10),
                text_align=CENTER,
                alignment=CENTER,
                font_size=16,
                flex=1,
            ),
        )

        spacer = toga.Box(style=Pack(flex=1))

        # Cache content
        self.button_refresh_cache = toga.Button(
            "Refresh cache",
            on_press=self.refresh_cache,
            style=Pack(padding=10, alignment=BOTTOM),
        )

        main_box.add(self.button_get_album, self.artist_label, self.album_label)
        main_box.add(spacer)
        main_box.add(self.button_refresh_cache)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def get_album(self, button: toga.Button):
        album = random_album.get_random_album(self.albums)
        print(f"{album=}")
        self.artist_label.text = album["artist"]
        self.album_label.text = album["name"]
        self.artist_label.refresh()
        self.album_label.refresh()

    def save_to_cache(self):
        self._album_cache.write_text(json.dumps(self.albums))

    def refresh_cache(self, button: toga.Button):
        self.albums = random_album.get_albums(self._sp_client)
        self.save_to_cache()


def main():
    return SpotifyRandomAlbumPicker()
