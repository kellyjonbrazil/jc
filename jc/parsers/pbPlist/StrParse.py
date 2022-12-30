# Copyright (c) 2016, Samantha Marshall (http://pewpewthespells.com)
# All rights reserved.
#
# https://github.com/samdmarshall/pbPlist
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
#
# 3. Neither the name of Samantha Marshall nor the names of its contributors may
# be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
import string

if sys.version_info >= (3, 0):
    def unichr(character): # pylint: disable=redefined-builtin
        return chr(character)

def ConvertNEXTSTEPToUnicode(hex_digits):
    # taken from http://ftp.unicode.org/Public/MAPPINGS/VENDORS/NEXT/NEXTSTEP.TXT
    conversion = {
        "80":	"a0",	# NO-BREAK SPACE
        "81":	"c0",	# LATIN CAPITAL LETTER A WITH GRAVE
        "82":	"c1",	# LATIN CAPITAL LETTER A WITH ACUTE
        "83":	"c2",	# LATIN CAPITAL LETTER A WITH CIRCUMFLEX
        "84":	"c3",	# LATIN CAPITAL LETTER A WITH TILDE
        "85":	"c4",	# LATIN CAPITAL LETTER A WITH DIAERESIS
        "86":	"c5",	# LATIN CAPITAL LETTER A WITH RING
        "87":	"c7",	# LATIN CAPITAL LETTER C WITH CEDILLA
        "88":	"c8",	# LATIN CAPITAL LETTER E WITH GRAVE
        "89":	"c9",	# LATIN CAPITAL LETTER E WITH ACUTE
        "8a":	"ca",	# LATIN CAPITAL LETTER E WITH CIRCUMFLEX
        "8b":	"cb",	# LATIN CAPITAL LETTER E WITH DIAERESIS
        "8c":	"cc",	# LATIN CAPITAL LETTER I WITH GRAVE
        "8d":	"cd",	# LATIN CAPITAL LETTER I WITH ACUTE
        "8e":	"ce",	# LATIN CAPITAL LETTER I WITH CIRCUMFLEX
        "8f":	"cf",	# LATIN CAPITAL LETTER I WITH DIAERESIS
        "90":	"d0",	# LATIN CAPITAL LETTER ETH
        "91":	"d1",	# LATIN CAPITAL LETTER N WITH TILDE
        "92":	"d2",	# LATIN CAPITAL LETTER O WITH GRAVE
        "93":	"d3",	# LATIN CAPITAL LETTER O WITH ACUTE
        "94":	"d4",	# LATIN CAPITAL LETTER O WITH CIRCUMFLEX
        "95":	"d5",	# LATIN CAPITAL LETTER O WITH TILDE
        "96":	"d6",	# LATIN CAPITAL LETTER O WITH DIAERESIS
        "97":	"d9",	# LATIN CAPITAL LETTER U WITH GRAVE
        "98":	"da",	# LATIN CAPITAL LETTER U WITH ACUTE
        "99":	"db",	# LATIN CAPITAL LETTER U WITH CIRCUMFLEX
        "9a":	"dc",	# LATIN CAPITAL LETTER U WITH DIAERESIS
        "9b":	"dd",	# LATIN CAPITAL LETTER Y WITH ACUTE
        "9c":	"de",	# LATIN CAPITAL LETTER THORN
        "9d":	"b5",	# MICRO SIGN
        "9e":	"d7",	# MULTIPLICATION SIGN
        "9f":	"f7",	# DIVISION SIGN
        "a0":	"a9",	# COPYRIGHT SIGN
        "a1":	"a1",	# INVERTED EXCLAMATION MARK
        "a2":	"a2",	# CENT SIGN
        "a3":	"a3",	# POUND SIGN
        "a4":	"44",	# FRACTION SLASH
        "a5":	"a5",	# YEN SIGN
        "a6":	"92",	# LATIN SMALL LETTER F WITH HOOK
        "a7":	"a7",	# SECTION SIGN
        "a8":	"a4",	# CURRENCY SIGN
        "a9":	"19",	# RIGHT SINGLE QUOTATION MARK
        "aa":	"1c",	# LEFT DOUBLE QUOTATION MARK
        "ab":	"ab",	# LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
        "ac":	"39",	# SINGLE LEFT-POINTING ANGLE QUOTATION MARK
        "ad":	"3a",	# SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
        "ae":	"01",	# LATIN SMALL LIGATURE FI
        "af":	"02",	# LATIN SMALL LIGATURE FL
        "b0":	"ae",	# REGISTERED SIGN
        "b1":	"13",	# EN DASH
        "b2":	"20",	# DAGGER
        "b3":	"21",	# DOUBLE DAGGER
        "b4":	"b7",	# MIDDLE DOT
        "b5":	"a6",	# BROKEN BAR
        "b6":	"b6",	# PILCROW SIGN
        "b7":	"22",	# BULLET
        "b8":	"1a",	# SINGLE LOW-9 QUOTATION MARK
        "b9":	"1e",	# DOUBLE LOW-9 QUOTATION MARK
        "ba":	"1d",	# RIGHT DOUBLE QUOTATION MARK
        "bb":	"bb",	# RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
        "bc":	"26",	# HORIZONTAL ELLIPSIS
        "bd":	"30",	# PER MILLE SIGN
        "be":	"ac",	# NOT SIGN
        "bf":	"bf",	# INVERTED QUESTION MARK
        "c0":	"b9",	# SUPERSCRIPT ONE
        "c1":	"cb",	# MODIFIER LETTER GRAVE ACCENT
        "c2":	"b4",	# ACUTE ACCENT
        "c3":	"c6",	# MODIFIER LETTER CIRCUMFLEX ACCENT
        "c4":	"dc",	# SMALL TILDE
        "c5":	"af",	# MACRON
        "c6":	"d8",	# BREVE
        "c7":	"d9",	# DOT ABOVE
        "c8":	"a8",	# DIAERESIS
        "c9":	"b2",	# SUPERSCRIPT TWO
        "ca":	"da",	# RING ABOVE
        "cb":	"b8",	# CEDILLA
        "cc":	"b3",	# SUPERSCRIPT THREE
        "cd":	"dd",	# DOUBLE ACUTE ACCENT
        "ce":	"db",	# OGONEK
        "cf":	"c7",	# CARON
        "d0":	"14",	# EM DASH
        "d1":	"b1",	# PLUS-MINUS SIGN
        "d2":	"bc",	# VULGAR FRACTION ONE QUARTER
        "d3":	"bd",	# VULGAR FRACTION ONE HALF
        "d4":	"be",	# VULGAR FRACTION THREE QUARTERS
        "d5":	"e0",	# LATIN SMALL LETTER A WITH GRAVE
        "d6":	"e1",	# LATIN SMALL LETTER A WITH ACUTE
        "d7":	"e2",	# LATIN SMALL LETTER A WITH CIRCUMFLEX
        "d8":	"e3",	# LATIN SMALL LETTER A WITH TILDE
        "d9":	"e4",	# LATIN SMALL LETTER A WITH DIAERESIS
        "da":	"e5",	# LATIN SMALL LETTER A WITH RING ABOVE
        "db":	"e7",	# LATIN SMALL LETTER C WITH CEDILLA
        "dc":	"e8",	# LATIN SMALL LETTER E WITH GRAVE
        "dd":	"e9",	# LATIN SMALL LETTER E WITH ACUTE
        "de":	"ea",	# LATIN SMALL LETTER E WITH CIRCUMFLEX
        "df":	"eb",	# LATIN SMALL LETTER E WITH DIAERESIS
        "e0":	"ec",	# LATIN SMALL LETTER I WITH GRAVE
        "e1":	"c6",	# LATIN CAPITAL LETTER AE
        "e2":	"ed",	# LATIN SMALL LETTER I WITH ACUTE
        "e3":	"aa",	# FEMININE ORDINAL INDICATOR
        "e4":	"ee",	# LATIN SMALL LETTER I WITH CIRCUMFLEX
        "e5":	"ef",	# LATIN SMALL LETTER I WITH DIAERESIS
        "e6":	"f0",	# LATIN SMALL LETTER ETH
        "e7":	"f1",	# LATIN SMALL LETTER N WITH TILDE
        "e8":	"41",	# LATIN CAPITAL LETTER L WITH STROKE
        "e9":	"d8",	# LATIN CAPITAL LETTER O WITH STROKE
        "ea":	"52",	# LATIN CAPITAL LIGATURE OE
        "eb":	"ba",	# MASCULINE ORDINAL INDICATOR
        "ec":	"f2",	# LATIN SMALL LETTER O WITH GRAVE
        "ed":	"f3",	# LATIN SMALL LETTER O WITH ACUTE
        "ee":	"f4",	# LATIN SMALL LETTER O WITH CIRCUMFLEX
        "ef":	"f5",	# LATIN SMALL LETTER O WITH TILDE
        "f0":	"f6",	# LATIN SMALL LETTER O WITH DIAERESIS
        "f1":	"e6",	# LATIN SMALL LETTER AE
        "f2":	"f9",	# LATIN SMALL LETTER U WITH GRAVE
        "f3":	"fa",	# LATIN SMALL LETTER U WITH ACUTE
        "f4":	"fb",	# LATIN SMALL LETTER U WITH CIRCUMFLEX
        "f5":	"31",	# LATIN SMALL LETTER DOTLESS I
        "f6":	"fc",	# LATIN SMALL LETTER U WITH DIAERESIS
        "f7":	"fd",	# LATIN SMALL LETTER Y WITH ACUTE
        "f8":	"42",	# LATIN SMALL LETTER L WITH STROKE
        "f9":	"f8",	# LATIN SMALL LETTER O WITH STROKE
        "fa":	"53",	# LATIN SMALL LIGATURE OE
        "fb":	"df",	# LATIN SMALL LETTER SHARP S
        "fc":	"fe",	# LATIN SMALL LETTER THORN
        "fd":	"ff",	# LATIN SMALL LETTER Y WITH DIAERESIS
        "fe":	"fd",	# .notdef, REPLACEMENT CHARACTER
        "ff":	"fd",	# .notdef, REPLACEMENT CHARACTER
    }
    return conversion[hex_digits]

def IsOctalNumber(character):
    oct_digits = set(string.octdigits)
    return set(character).issubset(oct_digits)

def IsHexNumber(character):
    hex_digits = set(string.hexdigits)
    return set(character).issubset(hex_digits)

def SanitizeCharacter(character):
    char = character
    escaped_characters = {
        '\a': '\\a',
        '\b': '\\b',
        '\f': '\\f',
        '\n': '\\n',
        '\r': '\\r',
        '\t': '\\t',
        '\v': '\\v',
        '\"': '\\"',
    }
    if character in escaped_characters.keys():
        char = escaped_characters[character]
    return char

# http://www.opensource.apple.com/source/CF/CF-744.19/CFOldStylePList.c See `getSlashedChar()`
def UnQuotifyString(string_data, start_index, end_index): # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    formatted_string = ''
    extracted_string = string_data[start_index:end_index]
    string_length = len(extracted_string)
    all_cases = ['0', '1', '2', '3', '4', '5', '6', '7', 'a', 'b', 'f', 'n', 'r', 't', 'v', '\"', '\n', 'U']
    index = 0
    while index < string_length: # pylint: disable=too-many-nested-blocks
        current_char = extracted_string[index]
        if current_char == '\\':
            next_char = extracted_string[index+1]
            if next_char in all_cases:
                index += 1
                if next_char == 'a':
                    formatted_string += '\a'
                if next_char == 'b':
                    formatted_string += '\b'
                if next_char == 'f':
                    formatted_string += '\f'
                if next_char == 'n':
                    formatted_string += '\n'
                if next_char == 'r':
                    formatted_string += '\r'
                if next_char == 't':
                    formatted_string += '\t'
                if next_char == 'v':
                    formatted_string += '\v'
                if next_char == '"':
                    formatted_string += '\"'
                if next_char == '\n':
                    formatted_string += '\n'
                if next_char == 'U':
                    starting_index = index + 1
                    ending_index = starting_index + 4
                    unicode_numbers = extracted_string[starting_index:ending_index]
                    for number in unicode_numbers:
                        index += 1
                        if IsHexNumber(number) is False: # pragma: no cover
                            message = 'Invalid unicode sequence on line '+str(LineNumberForIndex(string_data, start_index+index))
                            raise Exception(message)
                    formatted_string += unichr(int(unicode_numbers, 16))
                if IsOctalNumber(next_char) is True: # https://twitter.com/Catfish_Man/status/658014170055507968
                    starting_index = index
                    ending_index = starting_index + 1
                    for oct_index in range(3):
                        test_index = starting_index + oct_index
                        test_oct = extracted_string[test_index]
                        if IsOctalNumber(test_oct) is True:
                            ending_index += 1
                    octal_numbers = extracted_string[starting_index:ending_index]
                    hex_number = int(octal_numbers, 8)
                    hex_str = format(hex_number, 'x')
                    if hex_number >= 0x80:
                        hex_str = ConvertNEXTSTEPToUnicode(hex_str)
                    formatted_string += unichr(int('00'+hex_str, 16))
            else:
                formatted_string += current_char
                index += 1
                formatted_string += next_char
        else:
            formatted_string += current_char
        index += 1
    return formatted_string

def LineNumberForIndex(string_data, current_index):
    line_number = 1
    index = 0
    string_length = len(string_data)
    while (index < current_index) and (index < string_length):
        current_char = string_data[index]
        if IsNewline(current_char) is True:
            line_number += 1
        index += 1
    return line_number

def IsValidUnquotedStringCharacter(character):
    if len(character) == 1:
        valid_characters = set(string.ascii_letters+string.digits+'_$/:.-')
        return set(character).issubset(valid_characters)
    else: # pragma: no cover
        message = 'The function "IsValidUnquotedStringCharacter()" can only take single characters!'
        raise ValueError(message)

def IsSpecialWhitespace(character):
    value = ord(character)
    result = (value >= 9 and value <= 13) # tab, newline, vt, form feed, carriage return
    return result

def IsUnicodeSeparator(character):
    value = ord(character)
    result = (value == 8232 or value == 8233)
    return result

def IsRegularWhitespace(character):
    value = ord(character)
    result = (value == 32 or IsUnicodeSeparator(character)) # space and Unicode line sep, para sep
    return result

def IsDataFormattingWhitespace(character):
    value = ord(character)
    result = (IsNewline(character) or IsRegularWhitespace(character) or value == 9)
    return result

def IsNewline(character):
    value = ord(character)
    result = (value == 13 or value == 10)
    return result

def IsEndOfLine(character):
    result = (IsNewline(character) or IsUnicodeSeparator(character))
    return result

def IndexOfNextNonSpace(string_data, current_index): # pylint: disable=too-many-branches,too-many-statements
    successful = False
    found_index = current_index
    string_length = len(string_data)
    annotation_string = ''
    while found_index < string_length: # pylint: disable=too-many-nested-blocks
        current_char = string_data[found_index]
        if IsSpecialWhitespace(current_char) is True:
            found_index += 1
            continue
        if IsRegularWhitespace(current_char) is True:
            found_index += 1
            continue
        if current_char == '/':
            next_index = found_index + 1
            if next_index >= string_length:
                successful = True
                break
            else:
                next_character = string_data[next_index]
                if next_character == '/': # found a line comment "//"
                    found_index += 1
                    next_index = found_index
                    first_pass = True
                    while next_index < string_length:
                        test_char = string_data[next_index]
                        if IsEndOfLine(test_char) is True:
                            break
                        else:
                            if first_pass is False:
                                annotation_string += test_char
                            else:
                                first_pass = False
                        next_index += 1
                    found_index = next_index
                elif next_character == '*': # found a block comment "/* ... */"
                    found_index += 1
                    next_index = found_index
                    first_pass = True
                    while next_index < string_length:
                        test_char = string_data[next_index]
                        if test_char == '*' and (next_index+1 < string_length) and string_data[next_index+1] == '/':
                            next_index += 2
                            break
                        else:
                            if first_pass != True:
                                annotation_string += test_char
                            else:
                                first_pass = False
                        next_index += 1
                    found_index = next_index
                else:
                    successful = True
                    break
        else:
            successful = True
            break
    result = (successful, found_index, annotation_string)
    return result
