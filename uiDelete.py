from turtle import color
import kivy, os, sys
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from matplotlib.pyplot import text

from modules.recorder.InternalVoiceRecoder import InternalVoiceRecorder
from modules.converter.VoiceToTextConverter import VoiceToTextConverter
from databaseHandler.databaseUtils import DatabaseUtils

kivy.require("1.10.1")

class RecordMeetingPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
# alias, filepath, mp3, mvc, txt

        self.add_widget(Label(text='File Path', color = "white",size_hint=(.45, .1), pos_hint={'x': .25, 'y': .87}))

        self.filepath = TextInput(multiline=False,text = r"database\audiofiles", size_hint=(.5, .05), pos_hint={'x': .25, 'y': .82})
        self.add_widget(self.filepath)

        
        self.add_widget(Label(text='Meeting Time (Seconds)', size_hint=(.45, .1), pos_hint={'x': .05, 'y': .65}))
        
        self.mtime = TextInput(multiline=False,text = "10", size_hint=(.2, .05), pos_hint={'x': .5, 'y': .675})
        self.add_widget(self.mtime)
        
        self.add_widget(Label(text='File Name', size_hint=(.45, .1), pos_hint={'x': .05, 'y': .55}))
        
        self.fname = TextInput(multiline=False,text= "output.mp3", size_hint=(.2, .05), pos_hint={'x': .5, 'y': .575})
        self.add_widget(self.fname)

        self.add_widget(Label(text='Audio Frequency', size_hint=(.45, .1), pos_hint={'x': .05, 'y': .45}))
        
        self.fre = TextInput(multiline=False, readonly = True, text = "44100", size_hint=(.2, .05), pos_hint={'x': .5, 'y': .475})
        self.add_widget(self.fre)
        # self.fre.text = "44100"

        self.add_widget(Label(text='Alias', size_hint=(.45, .1), pos_hint={'x': .05, 'y': .35}))
        
        self.alias = TextInput(multiline=False,text = "default", size_hint=(.2, .05), pos_hint={'x': .5, 'y': .375})
        self.add_widget(self.alias)
        
        self.start_rec = Button(text='Start Recording', size_hint=(.3, .1), pos_hint={'center_x': .24, 'y': 0.2})
        self.add_widget(self.start_rec)
        self.start_rec.bind(on_press=self.after_start_rec_fn)
    

        self.save_and_go_btn = Button(text='Back', size_hint=(.3, .1), pos_hint={'center_x': .68, 'y': 0.2})
        self.add_widget(self.save_and_go_btn)
        self.save_and_go_btn.bind(on_press=self.after_rec_text_converter)

    def after_start_rec_fn(self, _):
        self.seconds = int(self.mtime.text)
        self.fs = int(self.fre.text)
        self.mp3_path_with_fileName = f"{self.filepath.text}\{self.fname.text}"
        ivr = InternalVoiceRecorder(seconds=self.seconds, fs=self.fs)
        ivr.recorder(filePath= self.mp3_path_with_fileName)

    def after_rec_text_converter(self, _):
        try:
            vttc = VoiceToTextConverter()
            self.wav_path_with_fileName = f"{self.filepath.text}\{self.alias.text}.wav"
            self.txt_path_with_fileName = f"{self.filepath.text}\{self.alias.text}.txt"

            print("Started audio COnversion")
            vttc.audioFormatConverter(inputPath=self.mp3_path_with_fileName, outputPath=self.wav_path_with_fileName)
            print("Started text conversion")
            vttc.voiceToTextConverter(inputPath=self.wav_path_with_fileName, outputPath=self.txt_path_with_fileName)
            print("Finish")

            dbu = DatabaseUtils()
            dbu.updateFileNamesAndPaths(alias=self.alias.text, mp3FileName=self.mp3_path_with_fileName, 
            txtFileName=self.txt_path_with_fileName, wavFileName=self.wav_path_with_fileName)
            dbu.updateDatabase()
        except:
            print("Go BAck")

class MainApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.main_page = RecordMeetingPage()
        screen = Screen(name= "MainScreen")
        screen.add_widget(self.main_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


if __name__ == "__main__":
    o_s = MainApp()
    o_s.run()