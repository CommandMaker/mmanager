#
# Copyright (C) 2026  CommandMaker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from typing import override
from database.models.model import Model


class Song(Model):
    def __init__(
        self,
        title: str,
        file_name: str,
        album_id: int,
        source_id: int,
        music_id: int | None = None,
        track_number: int | None = None,
        genre_id: int | None = None,
        album_artist_id: int | None = None,
        composer_id: int | None = None,
        disc_number: int | None = None,
        id: int | None = None
    ) -> None:
        self.id: int | None = id
        self.title: str = title
        self.file_name: str = file_name
        self.album_id: int | None = album_id
        self.music_id: int | None = music_id
        self.source_id: int = source_id
        self.track_number: int | None = track_number
        self.genre_id: int | None = genre_id
        self.album_artist_id: int | None = album_artist_id
        self.composer_id: int | None = composer_id
        self.disc_number: int | None = disc_number


    @override
    @staticmethod
    def fields() -> list['str']:
        return ['id', 'title', 'file_name', 'album_id', 'music_id', 'source_id', 'track_number', 'genre_id', 'album_artist_id', 'composer_id', 'disc_number']
