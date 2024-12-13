"""
A small app which chooses a random album to play from your liked album library.
"""

import json

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER, ROW, BOTTOM, HIDDEN, VISIBLE

from . import random_album


CACHE_FILE = "album-cache.json"


class SpotifyRandomAlbumPicker(toga.App):
    def startup(self):
        print("Creating client")
        self._sp_client = random_album.get_client()

        self.albums = []
        self._album_cache = self.paths.cache / CACHE_FILE

        box_main = toga.Box(style=Pack(direction=COLUMN))

        # Main content
        self.button_get_album = toga.Button(
            "Get a random album",
            on_press=self.get_album,
            style=Pack(padding=10),
        )

        self.label_artist = toga.Label(
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
        self.label_album = toga.Label(
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
        self.label_album_count = toga.Label(
            f"Total albums: {len(self.albums)}",
            style=Pack(text_align=CENTER, font_size=12, flex=1),
        )
        self.button_refresh_cache = toga.Button(
            "Refresh cache",
            on_press=self.refresh_cache,
            style=Pack(padding=10, alignment=BOTTOM),
        )
        self.progress_bar_refresh_cache = toga.ProgressBar(
            style=Pack(visibility=HIDDEN)
        )

        box_main.add(self.button_get_album, self.label_artist, self.label_album)
        box_main.add(spacer)
        box_main.add(
            self.progress_bar_refresh_cache,
            self.label_album_count,
            self.button_refresh_cache,
        )

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = box_main
        self.main_window.show()

    def on_running(self) -> None:
        print("Loading from cache")
        if self._album_cache.exists():
            print("Loading albums from cache")
            try:
                self.albums = json.loads(self._album_cache.read_text())
                self.update_album_count_label()
            except json.JSONDecodeError:
                print("Failed to load cache, loading albums")
        if not self.albums:
            print("Loading albums")
            yield from self.refresh_cache(None)


    def get_album(self, button: toga.Button):
        album = random_album.get_random_album(self.albums)
        print(f"{album=}")
        self.label_artist.text = album["artist"]
        self.label_album.text = album["name"]
        self.label_artist.refresh()
        self.label_album.refresh()

    def save_to_cache(self):
        self._album_cache.write_text(json.dumps(self.albums))

    def update_album_count_label(self):
        self.label_album_count.text = f"Total albums: {len(self.albums)}"
        self.label_album_count.refresh()

    def refresh_cache(self, button: toga.Button | None):
        self.label_album_count.text = "Refreshing cache..."
        # Redraw (see: https://github.com/beeware/toga/issues/1102)
        yield 0.1
        yield from self.update_albums()
        self.save_to_cache()
        self.update_album_count_label()

    def update_albums(self):
        self.albums = []
        self.set_up_progress_bar()
        for max_albums, albums in random_album.get_albums(self._sp_client):
            self.albums.extend(albums)
            total_albums = len(self.albums)
            self.progress_bar_refresh_cache.max = max_albums
            self.progress_bar_refresh_cache.value = total_albums
            self.label_album_count.text = (
                f"Refreshing cache... ({total_albums}/{max_albums})"
            )
            # Redraw
            yield 0.1
        self.tear_down_progress_bar()

    def set_up_progress_bar(self) -> None:
        self.progress_bar_refresh_cache.max = None
        self.progress_bar_refresh_cache.value = 0
        self.progress_bar_refresh_cache.style.visibility = VISIBLE
        self.progress_bar_refresh_cache.start()

    def tear_down_progress_bar(self) -> None:
        self.progress_bar_refresh_cache.stop()
        self.progress_bar_refresh_cache.style.visibility = HIDDEN
        self.progress_bar_refresh_cache.value = 0


def main():
    return SpotifyRandomAlbumPicker()
