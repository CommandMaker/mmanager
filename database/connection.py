#
# Copyright (C) 2026  Command_maker
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

import sqlite3
import os


class DatabaseConnection:
    '''
    This class is mainly used as an abstraction layer to the sqlite3 module,
    in case some custom operations must be done before interacting
    '''
    instance: DatabaseConnection | None = None

    def __init__(self, db_path: str) -> None:
        '''
        Create a new database connection.
        Automatically open the connection after checking the health of the connection
        '''
        self.db_path: str = db_path
        self.closed: bool = True

        _ = self.check_health()

        self.connection: sqlite3.Connection = self.open_connection()


    def check_health(self) -> bool:
        '''
        Check the specified database file to avoid any errors while opening

        @returns {bool} If the file is valid
        '''
        if not os.path.exists(self.db_path) or os.path.isdir(self.db_path):
            raise ValueError('The specified database path does not exists or is not a database file')

        return True


    def open_connection(self) -> sqlite3.Connection:
        '''
        Open a database connection
        This function is not meant to be used by the user as it is automatically called by the __init__ function

        @returns {sqlite3.Connection}
        '''
        self.closed = True
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row

        return connection


    def close_connection(self) -> None:
        '''
        Close the connection to the database
        '''
        if self.closed:
            return

        self.connection.close()
        self.closed = True
        DatabaseConnection.instance = None


    def get_cursor(self) -> sqlite3.Cursor:
        '''
        Return the cursor of the connection

        @returns {sqlite3.Cursor}
        '''
        return self.connection.cursor()


    def load_sql_schema(self) -> None:
        '''
        Load the SQL schema file to create the database
        '''
        schema_file = os.path.join(os.path.dirname(__file__), 'schema.sql')

        if not os.path.exists(schema_file):
            raise Exception('The SQL schema file does not exists')

        with open(schema_file, 'r') as schema:
            _ = self.get_cursor().executescript(schema.read())
            self.commit()


    def commit(self) -> None:
        '''
        Commit changes to the database
        '''
        self.connection.commit()


    @staticmethod
    def get_instance(db_path: str | None = None) -> DatabaseConnection:
        '''
        Return the instance of the connection or create one if connection is not opened

        @returns {DatabaseConnection}
        '''
        if DatabaseConnection.instance == None:
            DatabaseConnection.instance = DatabaseConnection(db_path if db_path != None else '')
            return DatabaseConnection.instance

        return DatabaseConnection.instance
