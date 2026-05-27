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


class Album(Model):
    def __init__(self, name: str, folder_name: str, release_year: str, artist_id: int, cover_id: int | None = None, id: int | None = None) -> None:
        self.id: int | None = id
        self.name: str = name
        self.folder_name: str = folder_name
        self.release_year: str = release_year
        self.artist_id: int = artist_id
        self.cover_id: int | None = cover_id


    @override
    @staticmethod
    def fields() -> list[str]:
        return ['id', 'name', 'folder_name', 'release_year', 'artist_id', 'cover_id']
