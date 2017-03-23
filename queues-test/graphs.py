import pylab
import numpy as np
from scipy.interpolate import spline
from matplotlib.ticker import FormatStrFormatter

message_sizes = np.array([1, 10, 100, 1000, 10000, 100000, 1000000])

ZeroMQ_PUBSUB = np.array([5700240, 53317760, 408329600, 3436128000, 4398000000, 7956800000, 5816000000])
ZeroMQ_PAIR = np.array([7173072, 61572560, 509158400, 3380408000, 4543920000, 10848000000, 7408000000])
nanomsg_PUBSUB = np.array([1712960, 17276640, 167488800, 1042752000, 5820000000, 9694400000, 6712000000])
nanomsg_BUS = np.array([1644720, 16656960, 160844000, 1227320000, 5412240000, 8252000000, 5608000000])
RabbitMQ_PUBSUB = np.array([46232, 423280, 3968800, 42160000, 164240000, 568000000, 968000000])
ActiveMQ_PUBSUB = np.array([33296, 332800, 3381600, 30672000, 294080000, 816000000, 816000000])


pylab.plot(message_sizes, ZeroMQ_PUBSUB, '-', label='ZeroMQ PUBSUB')
pylab.plot(message_sizes, ZeroMQ_PAIR, '-', label='ZeroMQ PAIR')
pylab.plot(message_sizes, nanomsg_PUBSUB, '-', label='nanomsg PUBSUB')
pylab.plot(message_sizes, nanomsg_BUS, '-', label='nanomsg BUS')
pylab.plot(message_sizes, RabbitMQ_PUBSUB, '-', label='RabbitMQ PUBSUB')
pylab.plot(message_sizes, ActiveMQ_PUBSUB, '-', label='ActiveMQ_PUBSUB')

legend = pylab.legend(fancybox=True, loc='best', ncol=2)
legend.get_frame().set_alpha(1)

# pylab.ylim(0, 3)
# pylab.xlim(0, 15000000)

# pylab.yticks(rotation=90)

ax = pylab.gca()
ax.set_xscale('log')
ax.set_yscale('log')
# ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
ax.yaxis.grid(b=True, which='major', color='grey', linestyle='-')
ax.yaxis.grid(b=True, which='minor', color='lightgrey', linestyle='--')
ax.xaxis.grid(b=True, which='major', color='grey', linestyle='-')
ax.xaxis.grid(b=True, which='minor', color='lightgrey', linestyle='--')

pylab.ylabel('Bandwidth, bit/s')
pylab.xlabel('Message size, bytes')

pylab.grid(True)
pylab.minorticks_on()

pylab.show()