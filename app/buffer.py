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


import struct
from typing import cast


def read(format: str, buffer: bytes, offset: int, size: int) -> int:
    '''
    Read bytes from the given buffers starting at offset according to the fomat
    See struct.unpack to see how to format

    @param {str} format The format to read bytes with
    @param {bytes} buffer The buffer to read from
    @param {int} offset The offset to start at
    @returns {int} The read bytes
    '''
    return cast(int, struct.unpack(format, buffer[offset:offset+size])[0])


def read_uint_msb(buffer: bytes, offset: int) -> int:
    '''
    Read an unsigned 4-bytes integer stored in big endian (most significant byte first)

    @param {bytes} buffer The buffer to read from
    @param {int} offset The offset to read at
    @returns {int}
    '''
    return read('>I', buffer, offset, 4)


def read_uint_lsb(buffer: bytes, offset: int) -> int:
    '''
    Read an unsigned 4-bytes integer stored in little endian (less significant byte first)

    @param {bytes} buffer The buffer to read from
    @param {int} offset The offset to read at
    @returns {int}
    '''
    return read('<I', buffer, offset, 4)


def read_ushort_msb(buffer: bytes, offset: int) -> int:
    '''
    Read an unsigned 2-bytes short integer stored in big endian (most significant byte first)

    @param {bytes} buffer The buffer to read from
    @param {int} offset The offset to read at
    @returns {int}
    '''
    return read('>H', buffer, offset, 2)


def read_ushort_lsb(buffer: bytes, offset: int) -> int:
    '''
    Read an unsigned 2-bytes short integer stored in little endian (less significant byte first)

    @param {bytes} buffer The buffer to read from
    @param {int} offset The offset to read at
    @returns {int}
    '''
    return read('<H', buffer, offset, 2)


def read_uchar(buffer: bytes, offset: int) -> int:
    '''
    Read an unsigned 1-byte char

    @param {bytes} buffer The buffer to read from
    @param {int} offset The offset to read at
    @returns {int}
    '''
    return read('@B', buffer, offset, 1)
