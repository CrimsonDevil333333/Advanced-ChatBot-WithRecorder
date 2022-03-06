import sounddevice as sd
from scipy.io.wavfile import write
import os
import speech_recognition as sr
import win32com.client as wincl

class InternalVoiceRecorder:
    def __init__(self, seconds = 10, fs = 44100) -> None:
        self.spk = wincl.Dispatch("SAPI.SpVoice").Speak
        self.fs = fs  # this is the frequency sampling; also: 4999, 64000
        self.seconds = seconds  # Duration of recording

    def recorder(self, filePath = None):
        if filePath == None:
            filePath = r"database\audiofiles\output.mp3"
        myrecording = sd.rec(int(self.seconds * self.fs), samplerate=self.fs, channels=2)
        self.spk("Recording Started.")
        sd.wait()  # Wait until recording is finished
        write(filePath, self.fs, myrecording)  # Save as WAV file
        os.startfile(filePath)
        self.spk("Recording Completed.")

if __name__ == "__main__":
    InternalVoiceRecorder().recorder()