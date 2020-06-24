import pyaudio
import socket


class VoiceCatcher:
    def __init__(self, port, sample_rate, sec_per_frame=1.0):
        self.cli_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cache = int(sample_rate*sec_per_frame)
        self.format = pyaudio.paInt16
        self.channels = 1
        self.sample_rate = sample_rate
        self.set_socket(port)

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.format,
                                  channels=self.channels,
                                  rate=self.sample_rate,
                                  input=True,
                                  frames_per_buffer=self.cache)
        self.cli_socket.send(f'Sample Rate:{self.sample_rate}'.encode())
        print("* recording")
        while True:
            data = self.stream.read(self.cache)
            self.cli_socket.send(data)

    def set_socket(self, port):
        self.cli_socket.connect(("localhost", port))


if __name__=='__main__':
    VoiceCatcher(8220, 44100)