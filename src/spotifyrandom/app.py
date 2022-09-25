"""
A small app which chooses a random album to play from your liked album library.
"""
import logging
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from . import random_album

log = logging.getLogger("main-app")


class SpotifyRandomAlbumPicker(toga.App):
    def startup(self):
        log.info("Creating client")
        self._sp_client = random_album.get_client()
        log.info("Loading albums")
        self.albums = random_album.get_albums(self._sp_client)
        main_box = toga.Box(style=Pack(direction=COLUMN))

        button = toga.Button(
            "Get a random album",
            on_press=self.get_album,
            style=Pack(padding=5),
        )

        self.name_label = toga.Label(
            "",
            style=Pack(
                padding=(10, 5),
                text_align="center",
            ),
        )

        main_box.add(button)
        main_box.add(self.name_label)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def get_album(self, button: toga.Button):
        album = random_album.get_random_album(self.albums)
        album_text = f"{album['artist']} | {album['name']}"
        self.name_label.text = album_text


def main():
    return SpotifyRandomAlbumPicker()
