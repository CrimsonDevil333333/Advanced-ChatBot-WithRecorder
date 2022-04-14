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
from exceptions.AliasNotFoundException import AliasNotFoundException
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
        self.allias = self.getUserAliasForDisplay()
        no_of_allias = len(self.allias)
    

        self.add_widget(Label(text='Your all Alias',font_size='40sp' ,color = "white",size_hint=(.45, .1), pos_hint={'x': .25, 'y': .87}))

        if no_of_allias %2 == 0:
            rows_required = no_of_allias/2
        else:
            rows_required = no_of_allias/2 +1

        max_y = .79
        min_y = .5
        
        MaxDiff = (max_y - min_y)/ rows_required
        y_pos = max_y
        
        bottom_line1 = Screen()
        for r in range(no_of_allias):
            if r==0:
                x_pos = .25
                y_pos = y_pos
            elif r % 2 == 0:
                x_pos = .25
                y_pos = y_pos - MaxDiff
            else:
                x_pos = .57
            bottom_line1.add_widget(Label(text= self.allias[r] ,
            color = "red", size_hint=(.15, .04), pos_hint={'x': x_pos, 'y': y_pos} ))

        self.add_widget(bottom_line1)

        self.ali = TextInput(multiline=False, size_hint=(.5, .05), pos_hint={'x': .25, 'y': .42})
        self.add_widget(self.ali)
        
        self.back_btn = Button(text='Back', size_hint=(.3, .1), pos_hint={'center_x': .24, 'y': 0.2})
        self.add_widget(self.back_btn)
        # self.back_btn.bind(on_press=self.back_btn_fn)
        
        self.load_and_go_btn = Button(text='Load', size_hint=(.3, .1), pos_hint={'center_x': .68, 'y': 0.2})
        self.add_widget(self.load_and_go_btn)
        self.load_and_go_btn.bind(on_press=self.load_data_btn)

    def load_data_btn(self, _):
        flag = 0
        for r in self.allias:
            if r == self.ali.text:
                flag = 1
        if(flag):
            du = DatabaseUtils()
            try:
                paths = du.getFilesPathOnBaseOfAlias(self.ali.text)

                # TODO 
                print(paths)

            except AliasNotFoundException:
                print("Alias not found in fileStructure Database")
        else:
            print("You have no such alias saved in your DataBase")
            self.ali.text = ""

    def getUserAliasForDisplay(self):
        loggedUserName = "vai"
        ud = UserDataBase()
        ud.refreshDataBase
        allias_list = ud.getUserAlias(loggedUserName)
        allias_list = allias_list[:-1]
        return allias_list.split(",")

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