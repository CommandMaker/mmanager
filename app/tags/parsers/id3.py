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

from dataclasses import dataclass
from typing import override
from app.buffer import read_uchar, read_uint_msb, read_ushort_lsb, read_ushort_msb
from app.tags.abstract_parser import AbstractParser


class ID3Parser(AbstractParser):

    @override
    @staticmethod
    def detect(file: str) -> bool:
        '''
        Return True if the file contains ID3v2.3 tags

        @param {str} file The path of the file to parse
        @returns {bool} True if this parser can parse the file, False otherwise
        '''
        with open(file, 'rb') as f:
            buffer = f.read()
            id3 = read_ushort_msb(buffer, 0) << 8 | read_uchar(buffer, 2)
            id3_version = read_ushort_msb(buffer, 3)

            return id3 == 0x494433 and id3_version == 0x0300


    @override
    def read(self) -> dict[str, str]:
        header = self.__read_header()
        offset = 0xdd

        print(self.__read_frame(offset))

        return {}


    @override
    def write(self, tags: dict[str, str]) -> None:
        pass


    def __read_header(self) -> ID3Header:
        '''
        Read ID3 header

        @returns {ID3Header} The header parsed
        '''
        id3_version = read_ushort_msb(self.buffer, 3)
        flags = read_uchar(self.buffer, 5)
        is_unsynchronized = (flags >> 7) & 1
        has_extended_header = (flags >> 6) & 1
        is_experimental = (flags >> 5) & 1

        tag_size = 0

        for i in range(6, 10):
            tag_size = (tag_size << 7) | read_uchar(self.buffer, i) & 0x7F # Discard the MSB bit of each byte as it is always 0

        return ID3Header(
            version=id3_version,
            tag_size=tag_size,
            unsynchronisation=is_unsynchronized,
            extended_header=has_extended_header,
            experimental=is_experimental
        )


    def __read_frame_header(self, offset: int) -> ID3FrameHeader:
        '''
        Read the frame header at the given offset

        @param {int} offset The offset of the header in the buffer
        @returns {dict[str, int]} The header parsed
        '''
        frame_id = read_uint_msb(self.buffer, offset)
        frame_size = read_uint_msb(self.buffer, offset + 4)
        frame_flags = read_ushort_msb(self.buffer, offset + 8)

        # To see the frame flags and their purposes, see https://id3.org/id3v2.3.0#Frame_header_flags
        tag_alter_preservation = (frame_flags >> 15) & 1
        file_alter_preservation = (frame_flags >> 14) & 1
        read_only = (frame_flags >> 13) & 1
        compressed = (frame_flags >> 7) & 1
        encrypted = (frame_flags >> 6) & 1
        grouping_identity = (frame_flags >> 5) & 1

        return ID3FrameHeader(
            frame_id=frame_id,
            size=frame_size,
            flag_tag_alter_preservation=tag_alter_preservation,
            flag_file_alter_preservation=file_alter_preservation,
            flag_read_only=read_only,
            flag_compression=compressed,
            flag_encryption=encrypted,
            flag_grouping_identity=grouping_identity
        )


    def __read_frame(self, offset: int) -> ID3Frame | None:
        '''
        Read the frame that starts at the given offset
        '''
        header = self.__read_frame_header(offset)

        if (header.frame_id >> 24) == 0x54:
            return self.__read_text_frame(offset, header)
        elif header.frame_id == 0x55534C54:
            return self.__read_uslt_frame(offset, header)
        elif header.frame_id == 0x41504943:
            return self.__read_apic_frame(offset, header)


    def __read_text_frame(self, offset: int, header: ID3FrameHeader) -> ID3TextFrame:
        '''
        Read the text frame starting at the given offset

        @param {int} offset The starting offset of the frame
        @param {ID3FrameHeader} header The already decoded frame header
        @returns {ID3TextFrame}
        '''
        frame = ID3TextFrame(header, offset)

        offset = offset + header.header_size

        frame.text_encoding = read_uchar(self.buffer, offset)

        if frame.text_encoding == 0x00:
            # Decode ISO-8859-1 string
            size = frame.header.size - 1
            value = self.__read_iso_8859_1_string(offset + 1, size)
            frame.value = value
            frame.byte_size = size
            frame.length = len(value)
        elif frame.text_encoding == 0x01:
            # Decode Unicode string
            size = frame.header.size - 3
            bytes_order, value = self.__read_unicode_string(offset + 1, size)
            frame.byte_order = 'BE' if bytes_order == 0xFEFF else 'LE'
            frame.value = value
            frame.length = len(value)
            frame.byte_size = size

        return frame


    def __read_iso_8859_1_string(self, offset: int, size: int) -> str:
        '''
        Read the ISO-8859-1 string located at offset

        @param {int} offset The position of the first byte of the string
        @param {int} size The size (in bytes) of the string
        @returns {str} The decoded string
        '''
        string = ''

        i = 0

        while i < size:
            string += chr(read_uchar(self.buffer, offset + i))
            i += 1

        return string


    def __read_unicode_string(self, offset: int, size: int) -> tuple[int, str]:
        '''
        Read the Unicode string located at offset

        @param {int} offset The position of the first byte of the string
        @param {int} size The size (in bytes) of the string
        @returns {tuple[int, str]} First param is the byte order of the string and the second is the value
        '''
        bytes_order = read_ushort_msb(self.buffer, offset)
        rchar = read_ushort_msb
        string = ''

        if bytes_order == 0xFFFE:
            rchar = read_ushort_lsb

        i = 0
        while i < size:
            string += chr(rchar(self.buffer, offset + 2 + i))
            i += 2

        return bytes_order, string


    def __read_uslt_frame(self, offset: int, header: ID3FrameHeader) -> ID3USLTFrame:
        '''
        Read an USLT (UnSynchronised Lyrics Text) frame

        @param {int} offset The starting byte position of the frame
        @param {ID3FrameHeader} header The header of the frame
        @returns {ID3USLTFrame}
        '''
        frame = ID3USLTFrame(header, offset)

        offset += frame.header.header_size
        frame.text_encoding = read_uchar(self.buffer, offset)

        if frame.text_encoding == 0x00:
            frame.language = self.__read_iso_8859_1_string(offset + 1, 3)
            frame.content_descriptor = self.__read_iso_8859_1_string(offset + 4, offset + 4 - self.buffer.find(0x00, offset + 4))
            frame.content_descriptor_size = offset + 4 - self.buffer.find(0x00, offset + 4) + 1 # Search for the next 0x00 byte in the buffer
            frame.content_descriptor_length = len(frame.content_descriptor)

            size = frame.header.size - 4 - frame.content_descriptor_size
            frame.byte_size = size
            frame.value = self.__read_iso_8859_1_string(offset + 5, size)
            frame.length = len(frame.value)
        elif frame.text_encoding == 0x01:
            # TODO: finish text decoding for Unicode

            # _, frame.language = self.__read_unicode_string(offset + 1, 3)
            # size = frame.header.size - 4 - frame.content_descriptor_size - 3
            # frame.byte_size = self.__read_unicode_string(offset + )
            pass

        return frame


    def __read_apic_frame(self, offset: int, header: ID3FrameHeader) -> ID3APICFrame:
        '''
        Read an APIC (Attached PICture) frame

        @param {int}
        '''


#=======================================================
#                   Data classes
#=======================================================
@dataclass
class ID3Header:
    '''
    This class modelize an ID3v2.3 header

    All flags are represented as an int (boolean are C-coded 0 = False, 1 = True)

    Size: 10 bytes
    '''
    version: int = 0x0300
    tag_size: int = 0x00 # The size (in bytes) of the ID3 tag (excluding the header)
    unsynchronisation: int = 0x00
    extended_header: int = 0x00
    experimental: int = 0x00

    header_size: int = 10
    '''
    The size in bytes of the header

    SHOULD NOT BE MODIFIED
    '''


@dataclass
class ID3FrameHeader:
    '''
    Represent the header of an ID3v2.3 frame

    Size: 10 bytes
    '''
    frame_id: int = 0x00
    '''
    A 4-bytes integer representing the identifier of the frame (ASCII)
    '''

    size: int = 0x00
    '''
    The size of the frame excluding the header
    '''

    flag_tag_alter_preservation: int = 0x00
    '''
    Should the frame be preserved if it is unknown and the tag is altered
    '''

    flag_file_alter_preservation: int = 0x00
    '''
    Should the frame be preserved if it is unknown and the file is altered
    '''

    flag_read_only: int = 0x00
    '''
    Is the frame read only ?
    '''

    flag_compression: int = 0x00
    '''
    Is the frame compressed ?
    '''

    flag_encryption: int = 0x00
    '''
    Is the frame encrypted ?
    '''

    flag_grouping_identity: int = 0x00
    '''
    Does the frame belongs to a group of frames ?
    '''

    header_size: int = 10
    '''
    The size in bytes of the header

    SHOULD NOT BE MODIFIED
    '''


@dataclass
class ID3Frame:
    '''
    Represent a complete frame of an ID3v2.3 tag.
    Can be overrided to provide more specific tag information.
    This class aims to be a base for all other frame types

    Size: at least 11 bytes (header + 1 byte of content)
    '''
    header: ID3FrameHeader
    '''
    The header of the frame
    '''

    offset: int
    '''
    The position of the first byte of the frame in the tag
    '''


@dataclass
class ID3TextFrame(ID3Frame):
    '''
    Represent a ID3v2.3 text frame (all frame with id starting with `T` (0x54))

    Some properties might be undefined depending on the type of encoding of the string
    '''

    text_encoding: int = 0x00
    '''
    Represent the encoding used by the string value
    0x00 = ISO-8859-1
    0x01 = Unicode
    '''

    byte_order: str | None = None
    '''
    Indicate the orders of the bytes for a Unicode string
    Has no signification for a ISO-8859-1 encoded string

    Possible value :
        - 'BE': Big endian encoding (Unicode BOM 0xFEFF)
        - 'LE': Little endian encoding (Unicode BOM 0xFFFE)
    '''

    length: int = 0
    '''
    The length of the string (in character)
    Should be the same as `byte_size` if ISO-8859-1 encoded
    '''

    byte_size: int = 0
    '''
    The size of the string value in bytes
    '''

    value: str = ''
    '''
    The value of the string
    '''


@dataclass
class ID3USLTFrame(ID3TextFrame):
    '''
    Represent an unsynchronised lyrics frame

    Based on a text frame
    '''

    language: str = ''
    '''
    The language the lyrics are written in
    '''

    content_descriptor: str = ''
    '''
    A content descriptor string representing the content of the lyrics

    Usually not set
    '''

    content_descriptor_size: int = 1
    '''
    The size in bytes of the content descriptor string
    '''

    content_descriptor_length: int = 0
    '''
    The length of the content descriptor string
    '''


@dataclass
class ID3APICFrame(ID3Frame):
    '''
    Represent an associated picture frame
    '''
    text_encoding: int = 0x00
    '''
    Represent the encoding used by the description field
    0x00 = ISO-8859-1
    0x01 = Unicode
    '''

    mime_type: str = ''
    '''
    The MIME type of the image
    '''

    picture_type: int = 0x00
    '''
    The type of picture this frame is holding

    Refer to https://id3.org/id3v2.3.0 chapter 4.15 to see the list of possible values
    '''

    description: str = ''
    '''
    The text description of the image
    Has a maximum length of 64 characters
    '''

    picture_data: int = 0x00
    '''
    The binary data of the picture
    '''
