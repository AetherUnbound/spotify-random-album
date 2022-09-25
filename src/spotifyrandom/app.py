"""
A small app which chooses a random album to play from your liked album library.
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER, ROW

from . import random_album


class SpotifyRandomAlbumPicker(toga.App):
    def startup(self):
        print("Creating client")
        self._sp_client = random_album.get_client()
        print("Loading albums")
        self.albums = random_album.get_albums(self._sp_client)
        main_box = toga.Box(style=Pack(direction=COLUMN))

        button = toga.Button(
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
                font_size=24,
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
                font_size=22,
                flex=1,
            ),
        )

        main_box.add(button)
        main_box.add(self.artist_label)
        main_box.add(self.album_label)

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


def main():
    return SpotifyRandomAlbumPicker()
