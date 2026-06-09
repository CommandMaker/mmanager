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

from app.settings.settings import Settings


def create_folder_if_needed() -> None:
    '''
    Create the default config folder if it doesn't exists
    '''
    settings = Settings.get_instance()
    config_folder = settings.get('config_folder')

    if not os.path.exists(config_folder):
        os.mkdir(config_folder)
