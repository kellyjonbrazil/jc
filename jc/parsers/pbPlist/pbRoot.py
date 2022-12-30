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

from functools import cmp_to_key
import collections
from .         import pbItem

def StringCmp(obj1, obj2):
    result = -1
    if obj1 > obj2:
        result = 1
    elif obj1 == obj2:
        result = 0
    return result

def KeySorter(obj1, obj2):
    result = 0
    if str(obj1) == 'isa':
        result = -1
    elif str(obj2) == 'isa':
        result = 1
    else:
        result = StringCmp(str(obj1), str(obj2))
    return result

class pbRoot(collections.MutableMapping):

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.key_storage = list()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __internalKeyCheck(self, key): # pylint: disable=no-self-use
        safe_key = key
        if isinstance(safe_key, str):
            safe_key = pbItem.pbItemResolver(safe_key, 'qstring')
        return safe_key

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        if key not in self.key_storage:
            self.key_storage.append(self.__internalKeyCheck(key))
        self.store[key] = value

    def __delitem__(self, key):
        if key in self.key_storage:
            self.key_storage.remove(key)
        del self.store[key]

    def __iter__(self):
        return self.key_storage.__iter__()

    def __len__(self):
        return self.key_storage.__len__()

    def __str__(self):
        return self.store.__str__()

    def __contains__(self, item):
        return item in self.key_storage

    def __getattr__(self, attrib):
        return getattr(self.store, attrib)

    def __keytransform__(self, key): # pylint: disable=no-self-use
        result = key
        if isinstance(key, pbItem.pbItem):
            result = key.value
        return result

    def sortedKeys(self):
        unsorted_keys = self.key_storage
        sorted_keys = sorted(unsorted_keys, key=cmp_to_key(KeySorter))
        can_sort = False
        if len(sorted_keys) > 0:
            all_dictionaries = all((isinstance(self[key].value, dict) or isinstance(self[key].value, pbRoot)) for key in unsorted_keys)
            if all_dictionaries:
                can_sort = all(self[key].get('isa', None) is not None for key in unsorted_keys)
                if can_sort:
                    sorted_keys = sorted(unsorted_keys, key=lambda k: str(self[k]['isa']))
        return (can_sort, sorted_keys)
