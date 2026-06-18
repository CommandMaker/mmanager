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

from app.tags.abstract_parser import AbstractParser
from app.tags.parsers.id3 import ID3Parser


parsers_list: list[type[AbstractParser]] = [ID3Parser]

class MusicTag:
    def __init__(self, audio_file: str) -> None:
        '''
        Build a MusicTag instance based on the tags present in the audio file
        '''
        self.audio_file: str = audio_file
        parser = self.__get_parser()

        tags = parser.read()
        print(tags)


    def __get_parser(self) -> AbstractParser:
        for parser in parsers_list:
            if parser.detect(self.audio_file):
                return parser(self.audio_file)

        raise Exception(f'No parser found for file "{self.audio_file}"')
