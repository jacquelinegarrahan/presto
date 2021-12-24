import pyaudio
import wave
from presto.channels.channel import Channel


pa = pyaudio.PyAudio()

DEFAULT_INFO = pa.get_default_host_api_info()


class FileAudio(Channel):

    def __init__(self, file, rate=48000, data_queue=None):
        self._rate = rate
        self._frames_per_buffer = frames_per_buffer

        wf = wave.open(sys.argv[1], 'rb')

        self._stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)


    def run(self):
        # read input stream
        data = wf.readframes(CHUNK)

        while data != '':
            stream.write(data)
            data = wf.readframes(CHUNK)


    def stop(self):
        self._stream.stop_stream()
        self._stream.close()


if __name__ == "__main__":
    listener = Microphone()
    listener.start()





data = wf.readframes(CHUNK)

while data != '':
    stream.write(data)
    data = wf.readframes(CHUNK)
