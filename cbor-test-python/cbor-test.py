import os
import json

import cbor
import cbor2


with open('test.json') as json_file:
    json_data = json.load(json_file)

json_file_size = os.stat('test.json').st_size

with open('test.cbor', 'rb') as cbor_file:
    cbor_data = cbor_file.read()

cbor_file_size = os.stat('test.cbor').st_size


def test_cbor_pack():
    cbor.dumps(json_data)


def test_cbor_unpack():
    cbor.loads(cbor_data)


def test_cbor2_pack():
    cbor2.dumps(json_data)


def test_cbor2_unpack():
    cbor2.loads(cbor_data)


if __name__ == '__main__':
    import timeit

    print('CBOR упаковка')
    tm = timeit.timeit('test_cbor_pack()', number=10, setup='from __main__ import test_cbor_pack')
    print(json_file_size / tm)

    print('CBOR распаковка')
    tm = timeit.timeit('test_cbor_unpack()', number=10, setup='from __main__ import test_cbor_unpack')
    print(cbor_file_size / tm)

    print('CBOR2 упаковка')
    tm = timeit.timeit('test_cbor2_pack()', number=10, setup='from __main__ import test_cbor2_pack')
    print(json_file_size / tm)

    print('CBOR2 распаковка')
    tm = timeit.timeit('test_cbor2_unpack()', number=10, setup='from __main__ import test_cbor2_unpack')
    print(cbor_file_size / tm)

