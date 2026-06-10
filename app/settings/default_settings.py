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

import os
import sys

from app.settings.settings import Settings


def load_default_settings() -> None:
    '''
    Apply the app default settings
    '''
    user_folder = os.path.expanduser('~user') if sys.platform.startswith('win32') else os.path.expanduser('~')
    config_folder = os.path.join(user_folder, 'AppData/Roaming/' if sys.platform.startswith('win32') else '.config/mmanager/')
    database_path = os.path.join(config_folder, 'database.db')

    settings = Settings.get_instance()
    settings.set('config_folder', config_folder)
    settings.set('database_path', database_path)
