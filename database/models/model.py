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
from typing import Any, Self


class Model(ABC):
    '''
    This class is the super-class for all database models.
    It contains the most basic functions that all models needs.
    '''

    @staticmethod
    @abstractmethod
    def fields() -> list[str] | dict[str, str | None]:
        '''
        Return the list of fields that will be mapped by the build_from_dict method
        Can be a list[str] if fields have the same name in the database and in the class
        or a dict[str, str | None] if fields are named differently. None means that the names are the
        same.
        '''
        pass

    @classmethod
    def build_from_dict(cls, dikt: dict[str, str]) -> Self:
        '''
        Build a new instance of a model using the list of properties defined in the model
        '''
        fields = cls.fields()
        args: dict[str, Any] = {} # pyright: ignore[reportExplicitAny]

        if type(fields) == dict:
            for k, v in fields.items(): # k is the SQL column name and v is the class field name
                if v == None:
                    v = k # We use the same variable name for SQL and object

                if not v in dikt:
                    raise Exception(f'Missing property "{v}" on the dict')

                args[v] = dikt[k]
        elif type(fields) == list:
            for v in fields:
                if not v in dikt:
                    raise Exception(f'Missing property "{v}" on the dict')

                args[v] = dikt[v]

        return cls(**args)

