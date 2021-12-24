from presto.channels.channel import Channel
from presto.screen import Screen
from presto.channels import MicrophoneAudio
from multiprocessing.managers import BaseManager
from time import sleep
from queue import LifoQueue


# create manager that knows how to create and manage LifoQueues
class MyManager(BaseManager):
    pass


MyManager.register("LifoQueue", LifoQueue)


class PrestoViz:
    def __init__(self, animation, rate=48000):
        self._animation = animation
        self.manager = MyManager()
        self.manager.start()

        self._data_queue = self.manager.LifoQueue()
        self._screen = Screen(self._animation, self._data_queue)
        self._channel = MicrophoneAudio(data_queue=self._data_queue, rate=48000)

    def start(self):
        self._channel.start()
        self._screen.start()

        self._channel.shutdown()


if __name__ == "__main__":
    from presto.animations import Mesh

    mesh = Mesh(48000)

    viz = PrestoViz(mesh)
    viz.start()
