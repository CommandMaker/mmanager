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

from enum import Enum
import sqlite3
from typing import Self, TypeVar

from database.connection import DatabaseConnection
from database.models.model import Model


T = TypeVar('T', bound='Model')

class SQLOperation(Enum):
    EQUALS = '='
    GT = '>'
    LT = '<'
    GTE = '>='
    LTE = '<='
    DIFF = '!='

    LIKE = 'LIKE'


class SQLOrder(Enum):
    ASCENDING = 'ASC'
    DESCENDING = 'DESC'


class SelectQuery:
    '''
    Build an SQL query and fetch results from the database connection
    '''
    def __init__(self, table: str, columns: list[str] | None = None) -> None:
        self.query: list[str] = [f'SELECT {", ".join(columns if columns != None else ["*"])} FROM {table}']
        self.arguments: tuple[str|int|bool, ...] = ()


    def get_query(self) -> str:
        '''
        Return the current SQL query as a valid SQL

        @returns {str} The built query from the current query class
        '''
        return ' '.join(self.query)


    def where(self, needle: str, operation: SQLOperation, haystack: str) -> Self:
        '''
        Add a WHERE clause to the query.

        @param {str} needle The left hand of the clause (a column name)
        @param {SQLOperation} operation The operator to use in the clause (see the enum for the list of operations)
        @param {str} haystack The column to test the needle against
        @returns {Self} The updated query
        '''
        self.query += [f"WHERE {needle} {operation.value} '{haystack}'"]

        return self


    def order_by(self, column: str, order: SQLOrder) -> Self:
        '''
        Add an ORDER BY clause to the query

        @param {str} column The column to order by
        @param {SQLOrder} order The order to sort in
        '''
        self.query += [f'ORDER BY {column} {order}']

        return self


    def limit(self, n: int) -> Self:
        '''
        Add a LIMIT clause to the query.

        @param {int} n The number of elements to return at most
        '''
        self.query += [f'LIMIT {n}']

        return self


    def fetch_all(self, klass: type[T]) -> list[T]:
        '''
        Fetch all rows matching the query built

        @param {type[T]} klass The model class to convert the results to. Must be a class herited from Model
        @returns {list[T]} Returns the list of rows converted to the given model
        '''
        db = DatabaseConnection.get_instance()
        results: list[sqlite3.Row] = db.get_cursor().execute(self.get_query(), self.arguments).fetchall()

        return [klass.build_from_dict(dict(row)) for row in results]


    def fetch_one(self, klass: type[T]) -> T:
        '''
        Fetch the first row matching the query

        @param {type[T]} klass The model to convert the result to
        @returns {T} Returns the result as a model
        '''
        db = DatabaseConnection.get_instance()
        result: sqlite3.Row = db.get_cursor().execute(self.get_query(), self.arguments).fetchone() # pyright: ignore[reportAny] Don't know why it's reported as Any here

        return klass.build_from_dict(dict(result))
