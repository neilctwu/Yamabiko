import pyaudio


class Audio:
    def __init__(self, io, sample_rate, sec_per_frame=1.0):
        self.p = pyaudio.PyAudio()
        self.format  = pyaudio.paInt16
        kwargs = {'format':self.format,
                  'channels':1,
                  'rate':sample_rate,
                  'frames_per_buffer':int(sample_rate*sec_per_frame),
                  'input': True if io == 'input' else False,
                  'output': True if io == 'output' else False}
        self.stream = self.p.open(**kwargs)
