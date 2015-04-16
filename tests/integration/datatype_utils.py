# Copyright 2013-2015 DataStax, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from decimal import Decimal
from datetime import datetime, date, time
from uuid import uuid1, uuid4

try:
    from blist import sortedset
except ImportError:
    sortedset = set  # noqa

from cassandra.util import OrderedMap

from tests.integration import get_server_versions


PRIMITIVE_DATATYPES = [
    'ascii',
    'bigint',
    'blob',
    'boolean',
    'decimal',
    'double',
    'float',
    'inet',
    'int',
    'text',
    'timestamp',
    'timeuuid',
    'uuid',
    'varchar',
    'varint',
]

COLLECTION_TYPES = [
    'list',
    'set',
    'map',
]


def update_datatypes():
    _cass_version, _cql_version = get_server_versions()

    if _cass_version >= (2, 1, 0):
        COLLECTION_TYPES.append('tuple')

    if _cass_version >= (2, 1, 5):
        PRIMITIVE_DATATYPES.append('date')
        PRIMITIVE_DATATYPES.append('time')


def get_sample_data():
    sample_data = {}

    for datatype in PRIMITIVE_DATATYPES:
        if datatype == 'ascii':
            sample_data[datatype] = 'ascii'

        elif datatype == 'bigint':
            sample_data[datatype] = 2 ** 63 - 1

        elif datatype == 'blob':
            sample_data[datatype] = bytearray(b'hello world')

        elif datatype == 'boolean':
            sample_data[datatype] = True

        elif datatype == 'decimal':
            sample_data[datatype] = Decimal('12.3E+7')

        elif datatype == 'double':
            sample_data[datatype] = 1.23E+8

        elif datatype == 'float':
            sample_data[datatype] = 3.4028234663852886e+38

        elif datatype == 'inet':
            sample_data[datatype] = '123.123.123.123'

        elif datatype == 'int':
            sample_data[datatype] = 2147483647

        elif datatype == 'text':
            sample_data[datatype] = 'text'

        elif datatype == 'timestamp':
            sample_data[datatype] = datetime(2013, 12, 31, 23, 59, 59, 999000)

        elif datatype == 'timeuuid':
            sample_data[datatype] = uuid1()

        elif datatype == 'uuid':
            sample_data[datatype] = uuid4()

        elif datatype == 'varchar':
            sample_data[datatype] = 'varchar'

        elif datatype == 'varint':
            sample_data[datatype] = int(str(2147483647) + '000')

        elif datatype == 'date':
            sample_data[datatype] = date(2015, 1, 15)

        elif datatype == 'time':
            sample_data[datatype] = time(16, 47, 25, 7)

        else:
            raise Exception("Missing handling of {0}".format(datatype))

    return sample_data

SAMPLE_DATA = get_sample_data()


def get_sample(datatype):
    """
    Helper method to access created sample data for primitive types
    """

    return SAMPLE_DATA[datatype]


def get_collection_sample(collection_type, datatype):
    """
    Helper method to access created sample data for collection types
    """

    if collection_type == 'list':
        return [get_sample(datatype), get_sample(datatype)]
    elif collection_type == 'set':
        return sortedset([get_sample(datatype)])
    elif collection_type == 'map':
        return OrderedMap([(get_sample(datatype), get_sample(datatype))])
    elif collection_type == 'tuple':
        return (get_sample(datatype),)
    else:
        raise Exception('Missing handling of non-primitive type {0}.'.format(collection_type))
