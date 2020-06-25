from voice_catcher import VoiceCatcher
from voice_recorder import Recorder
from threading import Thread


if __name__ == '__main__':
    t1 = Thread(target = Recorder, args=(8220,))
    t2 = Thread(target = VoiceCatcher, args=(8220, 44100))
    t1.start()
    t2.start()