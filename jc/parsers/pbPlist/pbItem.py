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

from . import StrParse

def PushIndent(indent_level):
    return indent_level + 1

def PopIndent(indent_level):
    return indent_level - 1

def WriteIndent(level=0):
    output = ''
    for _index in range(level):
        output += '\t'
    return output

def WriteNewline(level=0, indent=True):
    output = '\n'
    if indent:
        output += WriteIndent(level)
    return output

class pbItem(object):
    def __init__(self, value=None, type_name=None, annotation=None):
        if value != None and type_name != None:
            self.value = value
            if type_name not in KnownTypes.keys(): # pragma: no cover
                message = 'Unknown type "'+type_name+'" passed to '+self.__class__.__name__+' initializer!'
                raise TypeError(message)
            self.type_name = type_name
            self.annotation = annotation
        else: # pragma: no cover
            message = 'The class "'+self.__class__.__name__+'" must be initialized with a non-None value'
            raise ValueError(message)

    def __eq__(self, other):
        is_equal = False
        if isinstance(other, pbItem):
            other = other.value
        if type(other) is type(self.value):
            is_equal = self.value.__eq__(other)
        return is_equal

    def __hash__(self):
        return self.value.__hash__()

    def __repr__(self):
        return self.value.__repr__()

    def __iter__(self):
        return self.value.__iter__()

    def __getattr__(self, attrib):
        return self.value.__getattr__(attrib)

    def __str__(self):
        return self.writeStringRep(0, False)[0]

    def __getitem__(self, key):
        return self.value.__getitem__(key)

    def __setitem__(self, key, value):
        self.value.__setitem__(key, value)

    def __len__(self):
        return self.value.__len__()

    def __contains__(self, item):
        return self.value.__contains__(item)

    def __get__(self, obj, objtype):
        return self.value.__get__(obj, objtype)

    def writeStringRep(self, indent_level=0, pretty=True):
        return self.writeString(indent_level, pretty)

    def writeString(self, indent_level=0, pretty=True): # pylint: disable=no-self-use,unused-variable,unused-argument ; # pragma: no cover
        message = 'This is a base class, it cannot write!'
        raise Exception(message)

    def nativeType(self):
        return self.value

    def writeAnnotation(self):
        output_string = ''
        if self.annotation != None and len(self.annotation) > 0:
            output_string += ' '
            output_string += '/*'
            output_string += self.annotation
            output_string += '*/'
        return output_string

class pbString(pbItem):
    def writeString(self, indent_level=0, pretty=True):
        string_string = ''
        string_string += self.value
        if pretty is True:
            string_string += self.writeAnnotation()
        return (string_string, indent_level)

class pbQString(pbItem):
    def writeStringRep(self, indent_level=0, pretty=True):
        qstring_string = ''
        for character in self.value:
            qstring_string += StrParse.SanitizeCharacter(character)
        return (qstring_string, indent_level)

    def writeString(self, indent_level=0, pretty=True):
        qstring_string = ''
        qstring_string += '"'
        string_rep, indent_level = self.writeStringRep(indent_level, pretty)
        qstring_string += string_rep
        qstring_string += '"'
        if pretty is True:
            qstring_string += self.writeAnnotation()
        return (qstring_string, indent_level)

class pbData(pbItem):
    def writeString(self, indent_level=0, pretty=True):
        data_string = ''
        indent_level = PushIndent(indent_level)
        data_string += '<'
        grouping_byte_counter = 0
        grouping_line_counter = 0
        for hex_byte in map(ord, self.value.decode()):
            data_string += format(hex_byte, 'x')
            grouping_byte_counter += 1
            # write a space every 4th byte
            if grouping_byte_counter == 4:
                data_string += ' '
                grouping_byte_counter = 0
                grouping_line_counter += 1
            # write a newline every 4th grouping of bytes
            if grouping_line_counter == 4:
                data_string += WriteNewline(indent_level)
                data_string += ' ' # indent an additional space to make the byte groupings line up
                grouping_line_counter = 0
        data_string += '>'
        if pretty is True:
            data_string += self.writeAnnotation()
        indent_level = PopIndent(indent_level)
        return (data_string, indent_level)

class pbDictionary(pbItem):
    def nativeType(self):
        new_value = dict()
        for key in self.keys():
            value = self[key]
            new_value[str(key)] = value.nativeType()
        return new_value
    def writeString(self, indent_level=0, pretty=True):
        dictionary_string = ''
        dictionary_string += '{'
        has_sorted_keys, keys_array = self.value.sortedKeys()
        dictionary_string += WriteNewline(indent_level, not has_sorted_keys)
        indent_level = PushIndent(indent_level)
        previous_value_type = None
        if len(keys_array) == 0:
            indent_level = PopIndent(indent_level)
        else:
            if not has_sorted_keys:
                dictionary_string += '\t'
            for key in keys_array:
                if has_sorted_keys:
                    current_value_type = str(self.value[key]['isa'])
                    if previous_value_type != current_value_type:
                        if previous_value_type != None:
                            dictionary_string += '/* End '+previous_value_type+' section */'
                            dictionary_string += WriteNewline(indent_level, False)
                        previous_value_type = current_value_type
                        dictionary_string += '\n/* Begin '+current_value_type+' section */'
                        dictionary_string += WriteNewline(indent_level)
                    else:
                        dictionary_string += WriteIndent(indent_level)
                write_string, indent_level = key.writeString(indent_level, pretty)
                dictionary_string += write_string
                dictionary_string += ' = '
                write_string, indent_level = self.value[key].writeString(indent_level, pretty)
                dictionary_string += write_string
                dictionary_string += ';'
                should_indent = True
                is_last_key = (key == keys_array[-1])
                if is_last_key:
                    if has_sorted_keys:
                        dictionary_string += WriteNewline(indent_level, False)
                        dictionary_string += '/* End '+previous_value_type+' section */'
                    indent_level = PopIndent(indent_level)
                else:
                    if has_sorted_keys:
                        should_indent = False
                dictionary_string += WriteNewline(indent_level, should_indent)
        dictionary_string += '}'
        return (dictionary_string, indent_level)

class pbArray(pbItem):
    def nativeType(self):
        new_value = [item.nativeType() for item in self.value]
        return new_value
    def writeString(self, indent_level=0, pretty=True):
        array_string = ''
        array_string += '('
        array_string += WriteNewline(indent_level)
        indent_level = PushIndent(indent_level)
        values_array = list(self.value)
        if len(values_array) == 0:
            indent_level = PopIndent(indent_level)
        else:
            array_string += '\t'
            for value in values_array:
                write_string, indent_level = value.writeString(indent_level, pretty)
                array_string += write_string
                if value != values_array[-1]:
                    array_string += ','
                else:
                    indent_level = PopIndent(indent_level)
                array_string += WriteNewline(indent_level)
        array_string += ')'
        return (array_string, indent_level)

KnownTypes = {
    'string': pbString,
    'qstring': pbQString,
    'data': pbData,
    'dictionary': pbDictionary,
    'array': pbArray,
}

def pbItemResolver(obj, type_name):
    initializer = KnownTypes[type_name]
    if initializer:
        return initializer(obj, type_name)
    else: # pragma: no cover
        message = 'Unknown type "'+type_name+'" passed to pbItemResolver!'
        raise TypeError(message)
