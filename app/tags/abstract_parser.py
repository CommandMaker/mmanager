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

from abc import ABC, abstractmethod

class AbstractParser(ABC):

    def __init__(self, file_path: str):
        self.file_path: str = file_path

        with open(self.file_path, 'rb') as file:
            self.buffer: bytes = file.read()


    @staticmethod
    @abstractmethod
    def detect(file: str) -> bool:
        '''
        Return True if the parser can parse this file

        @param {str} file The path of the file to parse
        @returns {bool} True if this parser can parse the file, False otherwise
        '''
        pass


    @abstractmethod
    def read(self) -> dict[str, str]:
        '''
        Read tags from the given file and return them in a dict

        @returns {dict[str, str]} The list of tags
        '''
        pass


    @abstractmethod
    def write(self, tags: dict[str, str]) -> None:
        '''
        Write the given tags to the audio file

        @param {dict[str, str]} tags The tags to write
        '''
        pass
