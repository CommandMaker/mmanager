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

#==============================================
#               Helper functions
#==============================================
import argparse


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
