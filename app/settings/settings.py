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


import json
import os
from typing import TypeVar, cast


type json_value_t = str | int | bool | list[json_value_t] | dict[str, json_value_t]
type json_t = dict[str, json_value_t] | list[json_value_t]
T = TypeVar('T', bound='json_value_t')

class Settings:
    instance: Settings | None = None
    '''
    Don't use this directly, use Settings.get_instance()
    '''

    __settings: dict[str, json_value_t]

    def __init__(self) -> None:
        self.__settings = {}


    def set(self, key: str, value: json_value_t) -> None:
        '''
        Add or replace a value in the settings

        @param {str} key The key to access the setting
        @param {str | int | bool} value The value to save
        '''
        self.__settings[key] = value


    def get(self, key: str, _: type[T] = str) -> T:
        '''
        Get the value assigned to the specified key

        @param {str} key The key to access the setting
        @param {type[T]} _ The type of the value
        @returns {T} The value of the settings if it exists. Error otherwise
        '''
        if not self.has(key):
            raise ValueError(f'Settings doesn\'t contains the key "{key}"')

        return self.__settings[key] # pyright: ignore[reportReturnType]


    def has(self, key: str) -> bool:
        '''
        Return True if the settings contains the specified key. False otherwise

        @param {str} key
        @returns {bool}
        '''
        return key in self.__settings


    @staticmethod
    def get_instance() -> Settings:
        '''
        Return the current instance or build a new one if needed

        @returns {Settings}
        '''
        if Settings.instance == None:
            Settings.instance = Settings()

        return Settings.instance
