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

from app.cli.log.logger import log
from app.prepare_app import prepare_app
from app.settings.default_settings import load_default_settings
from app.settings.settings import Settings


def process_args(argv: list[str] | None = None) -> argparse.Namespace:
    '''
    Process the given arguments to prepare the dispatch

    @param {list[str]} argv The list of arguments to analyse
    @returns {argparse.Namespace} The args validated and parsed
    '''
    parser = argparse.ArgumentParser(description='Manage your music library efficiently', epilog='Released under GPL3 license. Written by Command_maker. 2026')

    _ = parser.add_argument('--database', help='Override the default database path', type=str)
    _ = parser.add_argument('--quiet', '-q', action='store_true', help='Disable logging')

    commands = parser.add_subparsers(title='Commands', dest='command', required=True)

    db = commands.add_parser('database', help='Manage the app internal database')
    _ = db.add_argument('subcommand', help='Action to do on the database', choices=['create', 'rebuild', 'delete', 'update'])

    fs = commands.add_parser('fs', help='Manage the audio files')
    _ = fs.add_argument('subcommand', help='Action to do on the files', choices=['sort', 'flush'])

    return parser.parse_args(argv)


def dispatch_command(args: argparse.Namespace) -> None:
    '''
    Dispatch the result of the process_arg function to the correct function

    @param {argparse.Namespace} namespace The result of the args parsing
    '''

    load_default_settings()
    log('Loading default settings')
    override_default_settings(args)
    prepare_app()

    command = get_required_str_arg(args, 'command')
    match command:
        case 'database':
            print('database command')
            print(Settings.get_instance().get('database_path'))
        case 'fs':
            print('fs command')
        case _:
            raise ValueError(f'Unknown command {command}')


def override_default_settings(args: argparse.Namespace) -> None:
    '''
    Override the default settings with the ones provided by the user

    @param {argparse.Namespace} args The args of the app
    '''
    settings = Settings.get_instance()
    db_path = get_str_arg(args, 'database')
    quiet = get_bool_arg(args, 'quiet')

    if quiet == True:
        settings.set('log_disabled', True)

    if db_path != None:
        log(f'Overriding default database path to {db_path}')
        settings.set('database_path', db_path)


#==============================================
#               Helper functions
#==============================================
def get_required_str_arg(args: argparse.Namespace, key: str) -> str:
    '''
    Return a string positional argument from the parser

    @param {argparse.Namespace} args The parsed args
    @param {str} key The key of the positional argument
    @returns {str} The value of the argument
    '''
    if type(getattr(args, key, None)) == str:
        return getattr(args, key, '')

    return ''


def get_str_arg(args: argparse.Namespace, key: str, fallback: str | None = None) -> str | None:
    '''
    Return the value of an optional argument. If not specified, return `fallback`

    @param {argparse.Namespace} args The args of the app
    @param {str} key The key of the arg
    @param {str | None} fallback The fallback value if the arg was not provided
    @returns {str | None} The arg value or the fallback
    '''
    return getattr(args, key, fallback)


def get_bool_arg(args: argparse.Namespace, key: str, fallback: bool | None = None) -> bool | None:
    '''
    Return the value of an optional argument. If not specified, return `fallback`

    @param {argparse.Namespace} args The args of the app
    @param {bool} key The key of the arg
    @param {bool | None} fallback The fallback value if the arg was not provided
    @returns {bool | None} The arg value or the fallback
    '''
    return getattr(args, key, fallback)
