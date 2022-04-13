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
from exceptions.AliasAllreadyAvailableException import AliasAllreadyAvailableException
from exceptions.UserNotFoundException import UserNotFoundException

from modules.recorder.InternalVoiceRecoder import InternalVoiceRecorder
from modules.converter.VoiceToTextConverter import VoiceToTextConverter
from databaseHandler.databaseUtils import DatabaseUtils

from databaseHandler.userDataBase import UserDataBase

kivy.require("1.10.1")

class SaveAliasPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
# alias, filepath, mp3, mvc, txt

        self.add_widget(Label(text='File Path', color = "white",size_hint=(.45, .1), pos_hint={'x': .25, 'y': .87}))

        self.filepath = TextInput(multiline=False, size_hint=(.5, .05), pos_hint={'x': .25, 'y': .82})
        self.add_widget(self.filepath)

        
        self.add_widget(Label(text='Mp3 File Name', size_hint=(.45, .1), pos_hint={'x': .05, 'y': .65}))
        
        self.mp3 = TextInput(multiline=False, size_hint=(.2, .05), pos_hint={'x': .5, 'y': .675})
        self.add_widget(self.mp3)
        
        self.add_widget(Label(text='WAV File Name', size_hint=(.45, .1), pos_hint={'x': .05, 'y': .55}))
        
        self.wav = TextInput(multiline=False, size_hint=(.2, .05), pos_hint={'x': .5, 'y': .575})
        self.add_widget(self.wav)

        self.add_widget(Label(text='TEXT File Name', size_hint=(.45, .1), pos_hint={'x': .05, 'y': .45}))
        
        self.txt = TextInput(multiline=False, size_hint=(.2, .05), pos_hint={'x': .5, 'y': .475})
        self.add_widget(self.txt)

        self.add_widget(Label(text='Alias', size_hint=(.45, .1), pos_hint={'x': .05, 'y': .35}))
        
        self.alias = TextInput(multiline=False, size_hint=(.2, .05), pos_hint={'x': .5, 'y': .375})
        self.add_widget(self.alias)
        
        self.back_btn = Button(text='Back', size_hint=(.3, .1), pos_hint={'center_x': .24, 'y': 0.2})
        self.add_widget(self.back_btn)
        # self.back_btn.bind(on_press=self.back_btn_fn)
        
        self.save_and_go_btn = Button(text='Save', size_hint=(.3, .1), pos_hint={'center_x': .68, 'y': 0.2})
        self.add_widget(self.save_and_go_btn)
        self.save_and_go_btn.bind(on_press=self.save_data_in_db_fn)

    def save_data_in_db_fn(self, _):
        self.mp3_path = fr"{self.filepath.text}\{self.mp3.text}"
        self.wav_path = fr"{self.filepath.text}\{self.wav.text}"
        self.txt_path = fr"{self.filepath.text}\{self.txt.text}"
        if self.mp3.text == "":
            print("It cant be blank ")
            # TODO -> break loop here dont proceed further
    
        loggedUserName = "admin"

        ud = UserDataBase()
        ud.refreshDataBase()
        try:
            allias_list = ud.getUserAlias(loggedUserName)
            print(allias_list.split(","))
            ud.updateAliasField(self.alias.text)
            allias_list = ud.getUserAlias(loggedUserName)
            print(allias_list.split(","))
            ud.refreshDataBase()

            du = DatabaseUtils()
            du.updateFileNamesAndPaths(alias=self.alias.text, mp3FileName=self.mp3_path, txtFileName=self.txt_path, wavFileName=self.wav_path)
            du.updateDatabase()
            
        except UserNotFoundException:
            print("User Not Found")
        except AliasAllreadyAvailableException:
            print("Select new alias")

class MainApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.main_page = SaveAliasPage()
        screen = Screen(name= "MainScreen")
        screen.add_widget(self.main_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


if __name__ == "__main__":
    o_s = MainApp()
    o_s.run()