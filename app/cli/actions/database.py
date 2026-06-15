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

import argparse
import glob
import os

from app.cli.helpers import get_required_str_arg, get_str_arg
from app.cli.log.logger import log


def dispatch_database_command(args: argparse.Namespace) -> None:
    '''
    Dispatch the given database command

    @param {argparse.Namespace} args The CLI args
    '''
    subcommand = get_required_str_arg(args, 'subcommand')

    match subcommand:
        case 'rebuild':
            rebuild_database(args)
        case 'update':
            log('Not implemented yet')
        case _:
            log('Unknown subcommand')


def rebuild_database(args: argparse.Namespace) -> None:
    '''
    Rebuild the database from scratch from the given source
    The source is given by the `source` CLI argument. It can be either `fs` to rebuild a database
    from audio files in a file system or `ipod` (not implemented yet) to rebuild from an iPod database

    @param {argparse.Namespace} args The CLI args
    '''
    source = get_str_arg(args, 'source')
    source_path = get_str_arg(args, 'path')

    if source == None or source_path == None:
        raise Exception('You must specify a source and a source path to rebuild the database from')

    if source == 'ipod':
        raise ValueError('The rebuild from an iPod is not supported yet. Follow the GitHub to see the updates')
    elif source == 'fs':
        if not os.path.exists(source_path) or not os.path.isdir(source_path):
            raise ValueError('The given source path does not exists or is not a directory')

        log(f'Recreating database from audio files in {source_path}. This can take a while')
        log('Searching recursively for audio file')

        filetypes = ('mp3', 'm4a', 'flac')
        files: list[str] = []
        for f in filetypes:
            files.extend(glob.glob(source_path.rstrip('/') + '/**/*.' + f, recursive=True))

        log(f'Found {len(files)} files')
