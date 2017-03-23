import os
import time
import json

import umsgpack
import bson
import ubjson
import cbor

import pylab
from matplotlib.ticker import FormatStrFormatter

json_files_sizes = []

msgpack_files_sizes = []
msgpack_compression = []
msgpack_pack_time = []
msgpack_unpack_time = []

bson_files_sizes = []
bson_compression = []
bson_pack_time = []
bson_unpack_time = []

ubjson_files_sizes = []
ubjson_compression = []
ubjson_pack_time = []
ubjson_unpack_time = []

cbor_files_sizes = []
cbor_compression = []
cbor_pack_time = []
cbor_unpack_time = []


for i in range(1, 6):
    json_file_name = 'test-{}.json'
    with open(json_file_name.format(i)) as json_file:
        json_data = json.load(json_file)

    json_file_size = os.stat(json_file_name.format(i)).st_size
    json_files_sizes += [json_file_size]

    # Testing MsgPack library.
    bin_file_name = 'test-{}.packers-test.bin'
    with open(bin_file_name.format(i), 'wb') as bin_file:
        start = time.time()
        umsg = umsgpack.packb(json_data)
        end = time.time()
        msgpack_pack_time += [end - start]
        bin_file.write(umsg)

    msgpack_file_size = os.stat(bin_file_name.format(i)).st_size
    msgpack_files_sizes += [msgpack_file_size]


    with open(bin_file_name.format(i), 'rb') as bin_file:
        umsg = bin_file.read()
        start = time.time()
        umsgpack.unpackb(umsg)
        end = time.time()
        msgpack_unpack_time += [end - start]

    msgpack_compression += [msgpack_file_size / json_file_size]

    # Testing BSON library.
    bin_file_name = 'test-{}.bson.bin'
    with open(bin_file_name.format(i), 'wb') as bin_file:
        start = time.time()
        bs = bson.dumps(json_data)
        end = time.time()
        bson_pack_time += [end - start]
        bin_file.write(bs)

    bson_file_size = os.stat(bin_file_name.format(i)).st_size
    bson_files_sizes += [bson_file_size]


    with open(bin_file_name.format(i), 'rb') as bin_file:
        bs = bin_file.read()
        start = time.time()
        bson.loads(bs)
        end = time.time()
        bson_unpack_time += [end - start]

    bson_compression += [bson_file_size / json_file_size]

    # Testing ubjson library.
    bin_file_name = 'test-{}.ubjson.bin'
    with open(bin_file_name.format(i), 'wb') as bin_file:
        start = time.time()
        ubs = ubjson.dumpb(json_data)
        end = time.time()
        ubjson_pack_time += [end - start]
        bin_file.write(ubs)

    ubjson_file_size = os.stat(bin_file_name.format(i)).st_size
    ubjson_files_sizes += [ubjson_file_size]

    with open(bin_file_name.format(i), 'rb') as bin_file:
        ubs = bin_file.read()
        start = time.time()
        ubjson.loadb(ubs)
        end = time.time()
        ubjson_unpack_time += [end - start]

    ubjson_compression += [ubjson_file_size / json_file_size]

    # Testing cbor library.
    bin_file_name = 'test-{}.cbor.bin'
    with open(bin_file_name.format(i), 'wb') as bin_file:
        start = time.time()
        cb = cbor.dumps(json_data)
        end = time.time()
        cbor_pack_time += [end - start]
        bin_file.write(cb)

    cbor_file_size = os.stat(bin_file_name.format(i)).st_size
    cbor_files_sizes += [cbor_file_size]

    with open(bin_file_name.format(i), 'rb') as bin_file:
        cb = bin_file.read()
        start = time.time()
        cbor.loads(cb)
        end = time.time()
        cbor_unpack_time += [end - start]

    cbor_compression += [cbor_file_size / json_file_size]


# Зависимость степени сжатия от исходного объема файла JSON.
# pylab.plot(json_files_sizes, msgpack_compression, '-', label='msgpack')
# pylab.plot(json_files_sizes, bson_compression, '-', label='BSON')
# pylab.plot(json_files_sizes, ubjson_compression, '-', label='ubjson')
# pylab.plot(json_files_sizes, cbor_compression, '-', label='CBOR')
#
# legend = pylab.legend(fancybox=True, loc='upper left', ncol=4)
# legend.get_frame().set_alpha(1)
#
# pylab.xscale('log')
#
# pylab.ylim(0.63, 0.83)
# pylab.xlim(0, 10**7)
#
# pylab.yticks(rotation=90)
#
# ax = pylab.gca()
# ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
# ax.yaxis.grid(b=True, which='major', color='grey', linestyle='-')
# ax.yaxis.grid(b=True, which='minor', color='lightgrey', linestyle='--')
# ax.xaxis.grid(b=True, which='major', color='grey', linestyle='-')
# ax.xaxis.grid(b=True, which='minor', color='lightgrey', linestyle='--')
#
# pylab.ylabel('Compression ratio')
# pylab.xlabel('JSON size, bytes')
#
# pylab.grid(True)
# pylab.minorticks_on()
#
# pylab.show()

# Зависимость времени сжатия от исходного объема файла JSON.
pylab.plot(json_files_sizes, msgpack_pack_time, '-', label='msgpack')
pylab.plot(json_files_sizes, bson_pack_time, '-', label='BSON')
pylab.plot(json_files_sizes, ubjson_pack_time, '-', label='ubjson')
pylab.plot(json_files_sizes, cbor_pack_time, '-', label='CBOR')

legend = pylab.legend(fancybox=True, loc='upper left', ncol=4)
legend.get_frame().set_alpha(1)

pylab.ylim(0, 3)
pylab.xlim(0, 15000000)

pylab.yticks(rotation=90)

ax = pylab.gca()
ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
ax.yaxis.grid(b=True, which='major', color='grey', linestyle='-')
ax.yaxis.grid(b=True, which='minor', color='lightgrey', linestyle='--')
ax.xaxis.grid(b=True, which='major', color='grey', linestyle='-')
ax.xaxis.grid(b=True, which='minor', color='lightgrey', linestyle='--')

pylab.ylabel('Packing time, s')
pylab.xlabel('JSON size, bytes')

pylab.grid(True)
pylab.minorticks_on()

pylab.show()

# Зависимость времени распаковки от исходного объема файла JSON.
# pylab.plot(json_files_sizes, msgpack_unpack_time, '-', label='msgpack')
# pylab.plot(json_files_sizes, bson_unpack_time, '-', label='BSON')
# pylab.plot(json_files_sizes, ubjson_unpack_time, '-', label='ubjson')
# pylab.plot(json_files_sizes, cbor_unpack_time, '-', label='CBOR')
#
# legend = pylab.legend(fancybox=True, loc='upper left', ncol=4)
# legend.get_frame().set_alpha(1)
#
# pylab.ylim(0, 2.5)
# pylab.xlim(0, 15000000)
#
# pylab.yticks(rotation=90)
#
# ax = pylab.gca()
# ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
# ax.yaxis.grid(b=True, which='major', color='grey', linestyle='-')
# ax.yaxis.grid(b=True, which='minor', color='lightgrey', linestyle='--')
# ax.xaxis.grid(b=True, which='major', color='grey', linestyle='-')
# ax.xaxis.grid(b=True, which='minor', color='lightgrey', linestyle='--')
#
# pylab.ylabel('Unpacking time, s')
# pylab.xlabel('JSON size, bytes')
#
# pylab.grid(True)
# pylab.minorticks_on()
#
# pylab.show()