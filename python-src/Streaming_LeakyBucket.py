# -------------------------------------------------------------------------------------------------------
# NEURONRAIN ASFER - Software for Mining Large Datasets
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------------------------------------------
# K.Srinivasan
# NeuronRain Documentation and Licensing: http://neuronrain-documentation.readthedocs.io/en/latest/
# Personal website(research): https://sites.google.com/site/kuja27/
# --------------------------------------------------------------------------------------------------------

import sys
import math
import random
from collections import defaultdict
from Streaming_AbstractGenerator import StreamAbsGen
import threading
import queue


class LeakyBucket(object):
    def __init__(self, data_storage, data_source, buffer_size=100):
        self.buffer_incoming_stream = StreamAbsGen(
            data_storage, data_source)
        self.buffer = queue.deque()
        self.buffer_size = buffer_size
        self.overflow = 0
        self.buffer_lock=threading.Lock()
        self.buffer_outgoing_stream = threading.Thread(
            target=self.outgoing_stream_thread, args=())
        self.buffer_outgoing_stream.start()

    def outgoing_stream_thread(self):
        print("outgoing_stream_thread():")
        while True:
            if self.buf_count == 0:
                continue
            if len(self.buffer) > 0:
                popped = self.buffer.pop()
                print(("Buffer Outgoing:", popped))

    def leaky_bucket_timeseries_analyzer(self):
        self.buf_count = 0
        for element in self.buffer_incoming_stream:
            if self.buf_count < self.buffer_size:
                self.buffer_lock.acquire()
                self.buffer.insert(0,element)
                self.buf_count += 1
                self.buffer_lock.release()
            else:
                self.buffer_lock.acquire()
                self.overflow += 1
                print("Buffer overflow:",self.overflow," - element: ",element)
                self.buf_count = 0
                self.buffer_lock.release()


if __name__ == "__main__":
    lb = LeakyBucket("file", "Dictionary.txt", 10)
    lb.leaky_bucket_timeseries_analyzer()
