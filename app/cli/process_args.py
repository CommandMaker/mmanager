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


def process_args(argv: list[str] | None = None) -> argparse.Namespace:
    '''
    Process the given arguments to prepare the dispatch

    @param {list[str]} argv The list of arguments to analyse
    @returns {argparse.Namespace} The args validated and parsed
    '''
    parser = argparse.ArgumentParser(description='Manage your music library efficiently', epilog='Released under GPL3 license. Written by Command_maker. 2026')
    commands = parser.add_subparsers(title='Commands', dest='command', required=True)

    db = commands.add_parser('database', help='Manage the app internal database')
    _ = db.add_argument('subcommand', help='Action to do on the database', choices=['create', 'restore', 'delete', 'update'])
    _ = db.add_argument('--path', '-p', help='Override the default database path')

    fs = commands.add_parser('fs', help='Manage the audio files')
    _ = fs.add_argument('subcommand', help='Action to do on the files', choices=['sort', 'flush'])

    return parser.parse_args(argv)


def dispatch_command(args: argparse.Namespace) -> None:
    '''
    Dispatch the result of the process_arg function to the correct function

    @param {argparse.Namespace} namespace The result of the args parsing
    '''
    command = get_required_str_arg(args, 'command')
    match command:
        case 'database':
            print('database command')
        case 'fs':
            print('fs command')
        case _:
            raise ValueError(f'Unknown command {command}')


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
