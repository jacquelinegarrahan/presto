import pyaudio
import numpy as np
from presto.channels.channel import Channel
import struct

pa = pyaudio.PyAudio()

DEFAULT_INFO = pa.get_default_host_api_info()


class MicrophoneAudio(Channel):
    def __init__(
        self,
        frames_per_buffer=1024,
        input_device_index=DEFAULT_INFO["defaultInputDevice"],
        rate=48000,
        data_queue=None,
    ):
        super().__init__()
        self._rate = rate
        self._frames_per_buffer = frames_per_buffer
        self._data_queue = data_queue
        self._input_device_index = input_device_index
        self._stream = None

    def run(self):
        # read input stream
        self._stream = pa.open(
            rate=self._rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            input_device_index=self._input_device_index,
            frames_per_buffer=self._frames_per_buffer,
        )

        while True:
            data = self._stream.read(self._rate)
            samps = np.fromstring(data, dtype=np.int16)
            if self._data_queue is not None:
                self._data_queue.put(samps)

    def shutdown(self):
        if self._stream is not None:
            self._stream.stop_stream()
            self._stream.close()


if __name__ == "__main__":
    listener = MicrophoneAudio()
    listener.start()
