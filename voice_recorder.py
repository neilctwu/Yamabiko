import wave
import struct
import math
from scipy.signal import butter, lfilter
import socket
import sys
import time


def get_rms(block):
    count = len(block) / 2
    format = "%dh" % (count)
    shorts = struct.unpack(format, block)
    sum_squares = 0.0
    for sample in shorts:
        n = sample * (1.0 / 32768.0)
        sum_squares += n * n
    return math.sqrt(sum_squares / count)


class VoiceRecorder:
    def __init__(self, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_server(('localhost', port))

        print("Listening for client . . .")
        conn, address = self.server_socket.accept()
        print("Connected to client at ", address)
        # pick a large output buffer size because i dont necessarily know how big the incoming packet is
        sentence_start = False
        sentence = []
        while True:
            output = conn.recv(2048)
            if 'Sample Rate:' in output.decode():
                sample_rate = int(output.decode().split(':')[-1])
                continue

            if not sentence_start:
                if self.check_fraction(output):
                    sentence_start = True
                    sentence = []
                    continue
            else:
                if not self.check_fraction(output):
                    sentence_start = False
                    self.save_sentence(sentence, sample_rate)
                    continue
                sentence.append(output)

    #TODO:
    def check_fraction(self, output):
        return

    #TODO:
    def save_sentence(self, wavs, sample_rate):
        if not wavs:
            return
        wav = b''.join(wavs)
        bp_wav = self.butter_bandpass(wav, 300, 3600, sample_rate, order=5)


    def set_server(self, address):
        self.server_socket.bind(address)
        self.server_socket.listen()

    @staticmethod
    def butter_bandpass(lowcut, highcut, fs, order=5):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def butter_bandpass_filter(self, data, lowcut, highcut, fs, order=5):
        b, a = self.butter_bandpass(lowcut, highcut, fs, order=order)
        y = lfilter(b, a, data)
        return y


if __name__=='__main__':
    VoiceRecorder(8220)