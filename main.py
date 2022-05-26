from doctest import OutputChecker
from logging import exception
import os, sys
from xml.dom import ValidationErr
from xmlrpc.client import FastMarshaller
import bottle_websocket
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
from pydantic import FilePath
from pyspark import *
from tables import Cols
from exceptions.AliasAllreadyAvailableException import AliasAllreadyAvailableException
from exceptions.AliasNotFoundException import AliasNotFoundException
from exceptions.DummyException import DummyException

from pages.TransitionPage import TransitionPage
from Utils.functions import *
from backend_main import BackendMain
from controller.MainController import MainController
from modules.recorder.InternalVoiceRecoder import InternalVoiceRecorder
from modules.converter.VoiceToTextConverter import VoiceToTextConverter
from databaseHandler.databaseUtils import DatabaseUtils

global loggedUserName

global bot
global Input
global Output

global vi

Input = False
Output = False
loggedUserName = ""

def BotMainInstance():
    global bot
    global Input
    global Output
    bot = BackendMain(Input=Input, Output=Output)

def VoiceInputInstance():
    global vi
    vi = MainController()

BotMainInstance()
VoiceInputInstance()

kivy.require("1.10.1")

# Main page of application -> MainPage
class MainPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.login_btn = Button(text='Log In', size_hint=(.5, .1), pos_hint={'center_x': .5, 'y': .7})
        self.add_widget(self.login_btn)
        self.login_btn.bind(on_press=self.login_fn)

        self.signup_btn = Button(text='Sign Up', size_hint=(.5, .1), pos_hint={'center_x': .5, 'y': .5})
        self.add_widget(self.signup_btn)
        self.signup_btn.bind(on_press=self.sign_up_fn)

        self.quit_btn = Button(text='Exit', size_hint=(.5, .1), pos_hint={'center_x': .5, 'y': 0.3})
        self.add_widget(self.quit_btn)
        self.quit_btn.bind(on_press=self.exit_app_fn )

    def login_fn(self, _):
        transitionInfo = f"Login Page ..."
        o_s.transition_page.update_info(transitionInfo)
        o_s.screen_manager.current = "TransitionScreen"
        Clock.schedule_once(self.redirect_login_page, 0.6)
    def redirect_login_page(self, _):
        try:
            o_s.login_page()
        except:
            print("Login Page instance already available")
        o_s.screen_manager.current = "LoginScreen"

    def sign_up_fn(self, _):
        transitionInfo = f"Sign Up Page ..."
        o_s.transition_page.update_info(transitionInfo)
        o_s.screen_manager.current = "TransitionScreen"
        Clock.schedule_once(self.redirect_signup_page, 0.6)
    def redirect_signup_page(self, _):
        try:
            o_s.signup_page()
        except:
            print("SignUp page Instance already available")
        o_s.screen_manager.current = "SignupScreen"

    def exit_app_fn(self, _):
        transitionInfo = f"Thanks For using our application"
        o_s.transition_page.update_info(transitionInfo)
        o_s.screen_manager.current = "TransitionScreen"
        Clock.schedule_once(self.exits, 0.6)
    def exits(self, _):
        sys.exit()

class SignUpPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_widget(Label(text='Username', size_hint=(.45, .1), pos_hint={'x': .05, 'y': .7}))
        
        self.username = TextInput(multiline=False, size_hint=(.45, .1), pos_hint={'x': .5, 'y': .7})
        self.add_widget(self.username)
        
        self.add_widget(Label(text='E-mail', size_hint=(.45, .1), pos_hint={'x': .05, 'y': .3}))
        
        self.email = TextInput(multiline=False, size_hint=(.45, .1), pos_hint={'x': .5, 'y': .3})
        self.add_widget(self.email)

        self.add_widget(Label(text='Password', size_hint=(.45, .1), pos_hint={'x': .05, 'y': .5}))
        
        self.password = TextInput(multiline=False, password=True, size_hint=(.45, .1), pos_hint={'x': .5, 'y': .5})
        self.add_widget(self.password)
        
        self.back_btn = Button(text='Back', size_hint=(.3, .1), pos_hint={'center_x': .24, 'y': 0.08})
        self.add_widget(self.back_btn)
        self.back_btn.bind(on_press=self.back_btn_fn)
        
        self.login_btn = Button(text='Log In', size_hint=(.3, .1), pos_hint={'center_x': .68, 'y': 0.08})
        self.add_widget(self.login_btn)
        self.login_btn.bind(on_press=self.login_fn_after_validation)

    def back_btn_fn(self, _):
        self.email.text = ""
        self.username.text = ""
        self.password.text = ""
        transitionInfo = f"Going back ..."
        o_s.transition_page.update_info(transitionInfo)
        o_s.screen_manager.current = "TransitionScreen"
        Clock.schedule_once(self.back_b, 1)
    def back_b(self, _):
        o_s.screen_manager.current = "MainScreen"

    def login_fn_after_validation(self, _):
        try:
            valid = saveUserInDB(userEmail = self.email.text, userName = self.username.text, userPassword = self.password.text)
            if valid:
                self.reset_vals()
                transitionInfo = "Account Created\nGoing back to Main Page"
                o_s.transition_page.update_info(transitionInfo)
                o_s.screen_manager.current = "TransitionScreen"
                Clock.schedule_once(self.validation_true, .6)  
            else:
                transitionInfo = "Please Enter all Details"
                o_s.transition_page.update_info(transitionInfo)
                o_s.screen_manager.current = "TransitionScreen"
                Clock.schedule_once(self.validation_false, .6)    
        except UserAlreadyAvailableException:
            self.username.text = ""
            transitionInfo = "UserName is Taken"
            o_s.transition_page.update_info(transitionInfo)
            o_s.screen_manager.current = "TransitionScreen"
            Clock.schedule_once(self.validation_false, .6)    
    def reset_vals(self):
        self.username.text = ""
        self.password.text = ""
        self.email.text = ""
    def validation_true(self, _):
        o_s.screen_manager.current = "MainScreen"
    def validation_false(self, _):
        o_s.screen_manager.current = "SignupScreen"

class LoginPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_widget(Label(text='Username', size_hint=(.45, .1), pos_hint={'x': .05, 'y': .65}))
        
        self.username = TextInput(multiline=False, size_hint=(.45, .1), pos_hint={'x': .5, 'y': .65})
        self.add_widget(self.username)

        self.add_widget(Label(text='Password', size_hint=(.45, .1), pos_hint={'x': .05, 'y': .5}))
        
        self.password = TextInput(multiline=False, password=True, size_hint=(.45, .1), pos_hint={'x': .5, 'y': .5})
        self.add_widget(self.password)
        
        self.back_btn = Button(text='Back', size_hint=(.3, .1), pos_hint={'center_x': .24, 'y': 0.08})
        self.add_widget(self.back_btn)
        self.back_btn.bind(on_press=self.back_btn_fn)
        
        self.login_btn = Button(text='Log In', size_hint=(.3, .1), pos_hint={'center_x': .68, 'y': 0.08})
        self.add_widget(self.login_btn)
        self.login_btn.bind(on_press=self.login_fn_after_validation)

    def back_btn_fn(self, isinstance):
        self.username.text = ""
        self.password.text = ""
        transitionInfo = f"Going back ..."
        o_s.transition_page.update_info(transitionInfo)
        o_s.screen_manager.current = "TransitionScreen"
        Clock.schedule_once(self.back_b, 1)
    def back_b(self, _):
        o_s.screen_manager.current = "MainScreen"

    def login_fn_after_validation(self, _):
        try:
            valid = checkUserFromDB( userName = self.username.text, userPassword= self.password.text)
            if valid:
                global loggedUserName
                loggedUserName = self.username.text
                self.username.text = ""
                self.password.text = ""
                transitionInfo = "Chat Page"
                o_s.transition_page.update_info(transitionInfo)
                o_s.screen_manager.current = "TransitionScreen"
                Clock.schedule_once(self.chatpage_fn, .6) 
            else:
                transitionInfo = "Please Enter a Username"
                o_s.transition_page.update_info(transitionInfo)
                o_s.screen_manager.current = "TransitionScreen"
                Clock.schedule_once(self.validation_false, .6)
        except UserNotFoundException:
            self.username.text = ""
            self.password.text = ""
            transitionInfo = "UserName Is wrong"
            o_s.transition_page.update_info(transitionInfo)
            o_s.screen_manager.current = "TransitionScreen"
            Clock.schedule_once(self.validation_false, .6)
        except WrongPasswordException:
            self.password.text = ""
            transitionInfo = "Password Is Wrong"
            o_s.transition_page.update_info(transitionInfo)
            o_s.screen_manager.current = "TransitionScreen"
            Clock.schedule_once(self.validation_false, .6)
        
    def validation_false(self, _):
        o_s.screen_manager.current = "LoginScreen"
    def chatpage_fn(self, _):
        try:
            print("In Try")
            o_s.chat_page()
        except:
            print("In Except")
            print("Chat Page Instance already avalaible")  
        o_s.screen_manager.current = "ChatScreen"

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
        transitionInfo = f"Recording Started..."
        o_s.transition_page.update_info(transitionInfo)
        o_s.screen_manager.current = "TransitionScreen"
        Clock.schedule_once(self.after_start_rec_fn2, 0.6)

    def after_start_rec_fn2(self, _):
        self.seconds = int(self.mtime.text)
        self.fs = int(self.fre.text)
        self.mp3_path_with_fileName = f"{self.filepath.text}\{self.fname.text}"
        ivr = InternalVoiceRecorder(seconds=self.seconds, fs=self.fs)
        ivr.recorder(filePath= self.mp3_path_with_fileName)

        transitionInfo = f"Recording Finish..."
        o_s.transition_page.update_info(transitionInfo)
        o_s.screen_manager.current = "TransitionScreen"
        Clock.schedule_once(self.rec_finish_fn, 0.6)
    def rec_finish_fn(self,_):
        try:
            o_s.record_meeting_page()
        except:
            print("record meeting page Instance allready available")
        o_s.screen_manager.current = "RecordMeetingScreen"
    

    def after_rec_text_converter(self, _):
        try:
            print(self.mp3_path_with_fileName)
            self.vttc = VoiceToTextConverter()
            self.wav_path_with_fileName = f"{self.filepath.text}\{self.alias.text}.wav"
            self.txt_path_with_fileName = f"{self.filepath.text}\{self.alias.text}.txt"

            transitionInfo = f"Starting Audio Conversion"
            o_s.transition_page.update_info(transitionInfo)
            o_s.screen_manager.current = "TransitionScreen"
            Clock.schedule_once(self.audio_format_convertor, 0.6)

        except:
            transitionInfo = f"Going Back..."
            o_s.transition_page.update_info(transitionInfo)
            o_s.screen_manager.current = "TransitionScreen"
            Clock.schedule_once(self.go_back, 0.6)
    def audio_format_convertor(self, _):
        try:
            self.vttc.audioFormatConverter(inputPath=self.mp3_path_with_fileName, outputPath=self.wav_path_with_fileName)
            transitionInfo = f"Starting Text Conversion"
            o_s.transition_page.update_info(transitionInfo)
            o_s.screen_manager.current = "TransitionScreen"
            Clock.schedule_once(self.text_convertor, 0.6)
        except:
            transitionInfo = f"Going Back..."
            o_s.transition_page.update_info(transitionInfo)
            o_s.screen_manager.current = "TransitionScreen"
            Clock.schedule_once(self.go_back, 0.6)
        
    def text_convertor(self,_):
        try:
            self.vttc.voiceToTextConverter(inputPath=self.wav_path_with_fileName, outputPath=self.txt_path_with_fileName)    
            transitionInfo = f"Saving In DataBase"
            o_s.transition_page.update_info(transitionInfo)
            o_s.screen_manager.current = "TransitionScreen"
            Clock.schedule_once(self.saving_in_database, 0.6)
        except:
            transitionInfo = f"Going Back..."
            o_s.transition_page.update_info(transitionInfo)
            o_s.screen_manager.current = "TransitionScreen"
            Clock.schedule_once(self.go_back, 0.6)
            
    def saving_in_database(self, _):
        dbu = DatabaseUtils()
        dbu.updateFileNamesAndPaths(alias=self.alias.text, mp3FileName=self.mp3_path_with_fileName, 
        txtFileName=self.txt_path_with_fileName, wavFileName=self.wav_path_with_fileName)
        dbu.updateDatabase()
        transitionInfo = f"Going Back"
        o_s.transition_page.update_info(transitionInfo)
        o_s.screen_manager.current = "TransitionScreen"
        Clock.schedule_once(self.go_back, 0.6)


    def go_back(self, _):
        try:
            o_s.chat_page()
        except:
            print("chat page Instance allready available")
        o_s.screen_manager.current = "ChatScreen"









class SaveAliasPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
        self.back_btn.bind(on_press=self.back_btn_fn)
        
        self.save_and_go_btn = Button(text='Save', size_hint=(.3, .1), pos_hint={'center_x': .68, 'y': 0.2})
        self.add_widget(self.save_and_go_btn)
        self.save_and_go_btn.bind(on_press=self.save_data_in_db_fn)

    def back_btn_fn(self, _):
        transitionInfo = "Going Back"
        o_s.transition_page.update_info(transitionInfo)
        o_s.screen_manager.current = "TransitionScreen"
        Clock.schedule_once(self.back_btn_fn1, .6)

    def back_btn_fn1(self,_):
        try:
            o_s.chat_page()
        except:
            print("ChatPage Instance allready there")
        o_s.screen_manager.current = "ChatScreen"

    def refresh_page_fn(self, _):
        try:
            o_s.save_alias_page()
        except:
            print("Save allias page instance allready available")
        o_s.screen_manager.current = "SaveAliasScreen"

    def save_data_in_db_fn(self, _):
        self.mp3_path = fr"{self.filepath.text}\{self.mp3.text}"
        self.wav_path = fr"{self.filepath.text}\{self.wav.text}"
        self.txt_path = fr"{self.filepath.text}\{self.txt.text}"
        if self.mp3.text == "":
            transitionInfo = "Mp3 File Name can't be blank"
            o_s.transition_page.update_info(transitionInfo)
            o_s.screen_manager.current = "TransitionScreen"
            Clock.schedule_once(self.refresh_page_fn, .6)
        elif self.alias.text == "":
            transitionInfo = "Alias can't be blank"
            o_s.transition_page.update_info(transitionInfo)
            o_s.screen_manager.current = "TransitionScreen"
            Clock.schedule_once(self.refresh_page_fn, .6)
        
        global loggedUserName

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
            
            transitionInfo = "Saved Data Now Going Back"
            o_s.transition_page.update_info(transitionInfo)
            o_s.screen_manager.current = "TransitionScreen"
            Clock.schedule_once(self.back_btn_fn1, .6)

        except UserNotFoundException:
            print("User Not Found")
        except AliasAllreadyAvailableException:
            transitionInfo = f"Select new Alias {self.alias.text} is allready there in database"
            o_s.transition_page.update_info(transitionInfo)
            o_s.screen_manager.current = "TransitionScreen"
            Clock.schedule_once(self.refresh_page_fn, .6)


class LoadAliasPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
        self.back_btn.bind(on_press=self.back_btn_fn)
        
        self.load_and_go_btn = Button(text='Load', size_hint=(.3, .1), pos_hint={'center_x': .68, 'y': 0.2})
        self.add_widget(self.load_and_go_btn)
        self.load_and_go_btn.bind(on_press=self.load_data_btn)

    def back_btn_fn(self, _):
        try:
            o_s.chat_page()
        except:
            print("Instance allready available")
        o_s.screen_manager.current = "ChatScreen"

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
                print(paths["txtFileName"])
                global bot
                # bot = BackendMain(Filepath=paths["txtFileName"])
                try:
                    dumppp = BackendMain(Filepath=paths["txtFileName"])
                    bot = dumppp
                except:
                    print("Data Not found")
                    transitionInfo = f"Txt File seems to be missing from Actual Path "
                    o_s.transition_page.update_info(transitionInfo)
                    o_s.screen_manager.current = "TransitionScreen"
                    Clock.schedule_once(self.getOnSamePage, 45)
                self.ali.text = ""
                transitionInfo = f"Files loaded now going back..."
                o_s.transition_page.update_info(transitionInfo)
                o_s.screen_manager.current = "TransitionScreen"
                Clock.schedule_once(self.back_btn_fn, 1)

            except AliasNotFoundException:
                transitionInfo = f"Alias not found in fileStructure Database"
                o_s.transition_page.update_info(transitionInfo)
                o_s.screen_manager.current = "TransitionScreen"
                Clock.schedule_once(self.getOnSamePage, 1)
        else:
            self.ali.text = ""
            transitionInfo = f"You have no such alias saved in your DataBase"
            o_s.transition_page.update_info(transitionInfo)
            o_s.screen_manager.current = "TransitionScreen"
            Clock.schedule_once(self.getOnSamePage, 1)

    def getOnSamePage(self,_):
        try:
            o_s.load_alias_page()
        except:
            print("Load allias page Instance allready available")
        o_s.screen_manager.current = "LoadAliasScreen"

    def getUserAliasForDisplay(self):
        global loggedUserName
        ud = UserDataBase()
        ud.refreshDataBase
        allias_list = ud.getUserAlias(loggedUserName)
        allias_list = allias_list[:-1]
        return allias_list.split(",")







class ScrollableLabel(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols = 1, size_hint_y=None)
        self.add_widget(self.layout)

        self.chat_history = Label(size_hint_y=None ,markup = True)
        self.scroll_to_point = Label()

        self.layout.add_widget(self.chat_history)
        self.layout.add_widget(self.scroll_to_point)
    
    def update_chat_history(self,message):
        self.chat_history.text += "\n" + message

        self.layout.height = self.chat_history.texture_size[1] + 15
        self.chat_history.height =self.chat_history.texture_size[1]
        self.chat_history.text_size = (self.chat_history.width*0.68, None)

        self.scroll_to(self.scroll_to_point)

    def update_chat_history_layout(self, _=None):
        self.layout.height = self.chat_history.texture_size[1] + 15
        self.chat_history.height =self.chat_history.texture_size[1]
        self.chat_history.text_size = (self.chat_history.width*0.68, None)




class ChatPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 3

        self.history = ScrollableLabel(height= Window.size[1]*0.6,size_hint_y=None)
        self.add_widget(self.history)

        self.new_message = TextInput(multiline=False)
        self.send = Button(text="Send")
        self.send.bind(on_press= self.send_message)

        self.logout_btn = Button(text='Logout')
        self.logout_btn.bind(on_press=self.logout_btn_fn)
        
        self.voice_input_btn = Button(text='Voice Input')
        self.voice_input_btn.bind(on_press=self.voice_input_fn)

        self.quit_btn = Button(text='Exit')
        self.quit_btn.bind(on_press=self.exit_app_fn)

        self.save_alias = Button(text='Add Recording')
        self.save_alias.bind(on_press=self.save_alias_fn)

        self.load_alias = Button(text='Load Recording')
        self.load_alias.bind(on_press=self.load_alias_fn)

        self.record_meeting = Button(text='Record Meeting')
        self.record_meeting.bind(on_press=self.rec_meeting_fn)

        bottom_line1 = GridLayout(cols=3)
        bottom_line1.add_widget(self.voice_input_btn)
        bottom_line1.add_widget(self.new_message)
        bottom_line1.add_widget(self.send)
        self.add_widget(bottom_line1)
        
        bottom_line2 = GridLayout(cols=5)
        bottom_line2.add_widget(self.logout_btn)
        bottom_line2.add_widget(self.save_alias)
        bottom_line2.add_widget(self.record_meeting)
        bottom_line2.add_widget(self.load_alias)
        bottom_line2.add_widget(self.quit_btn)
        self.add_widget(bottom_line2)

        # bottom_line3 = GridLayout(Cols=2)
        # bottom_line3.add_widget(self.save_alias)
        # bottom_line3.add_widget(self.load_alias)
        # self.add_widget(bottom_line3)

        Window.bind(on_key_down=self.on_key_down)

        Clock.schedule_once(self.focus_text_input,1)
        self.bind(size=self.adjust_fields)

    def adjust_fields(self, *_):
        if Window.size[1]*0.1<50:
            new_hight = Window.size[1]-50
        else:
            new_hight = Window.size[1]*0.6
        self.history.height = new_hight

        if Window.size[0]*0.2<150:
            new_width = Window.size[0]-160
        else:
            new_width = Window.size[0]*0.8
        self.new_message.width=new_width

        Clock.schedule_once(self.history.update_chat_history_layout,0.01)

    def on_key_down(self,isinstance,keyboard,keycode,text,modifiers):
        if keycode == 40:
            self.send_message(None)
    
    def send_message(self, _):
        global bot
        global loggedUserName
        message= self.new_message.text
        self.new_message.text = ""

        if message:
            self.history.update_chat_history(f"[color=dd2020]{loggedUserName}[/color] > {message}")
            # fun to save msg
            botmsg = bot.getBotResponse(userInput = message)
            self.history.update_chat_history(f"[color=20dd20]Bot[/color] > {botmsg}")

        Clock.schedule_once(self.focus_text_input,0.1)

    def focus_text_input(self, _):
        self.new_message.focus = True

    def voice_input_fn(self, _):
        global vi
        try:
            input = vi.convertVoiceToText()
            self.new_message.text = input
        except:
            self.new_message.text = "Try Typing VI not available"

    def logout_btn_fn(self, _):
        transitionInfo = f"Looging out ..."
        o_s.transition_page.update_info(transitionInfo)
        o_s.screen_manager.current = "TransitionScreen"
        Clock.schedule_once(self.back_b, 1)
    def back_b(self, _):
        o_s.screen_manager.current = "MainScreen"

    def exit_app_fn(self, _):
        transitionInfo = f"Thanks For using our application"
        o_s.transition_page.update_info(transitionInfo)
        o_s.screen_manager.current = "TransitionScreen"
        Clock.schedule_once(self.exits, 0.6)
    def exits(self, _):
        sys.exit()

    def save_alias_fn(self,_):
        transitionInfo = f"Going to Add Recording Session"
        o_s.transition_page.update_info(transitionInfo)
        o_s.screen_manager.current = "TransitionScreen"
        Clock.schedule_once(self.save_alias_fn1, 0.6)
    def save_alias_fn1(self, _):
        self.new_message.text = "Save alias"
        try:
            o_s.save_alias_page()
        except:
            print("Save alias instance allready created")
        o_s.screen_manager.current = "SaveAliasScreen"

    def load_alias_fn(self, _):
        transitionInfo = f"Going to Load Recording Session"
        o_s.transition_page.update_info(transitionInfo)
        o_s.screen_manager.current = "TransitionScreen"
        Clock.schedule_once(self.load_alias_fn2, 0.6)

    def load_alias_fn(self, _):
        try:
            o_s.load_alias_page()
        except:
            print("Load alias instance allready created")
        o_s.screen_manager.current = "LoadAliasScreen"

    def rec_meeting_fn(self, _):
        transitionInfo = f"Going to Recording"
        o_s.transition_page.update_info(transitionInfo)
        o_s.screen_manager.current = "TransitionScreen"
        Clock.schedule_once(self.rec_meeting_logic, 0.6)
    def rec_meeting_logic(self, _):
        try:
            o_s.record_meeting_page()
        except:
            print("rec meeting instance already created")
        o_s.screen_manager.current = "RecordMeetingScreen"
























class MainApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.main_page = MainPage()
        screen = Screen(name= "MainScreen")
        screen.add_widget(self.main_page)
        self.screen_manager.add_widget(screen)
        
        self.transition_page = TransitionPage()
        screen = Screen(name ="TransitionScreen")
        screen.add_widget(self.transition_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

    def signup_page(self):
        self.signup_page = SignUpPage()
        screen = Screen(name= "SignupScreen")
        screen.add_widget(self.signup_page)
        self.screen_manager.add_widget(screen)
        return self.screen_manager

    def login_page(self):
        self.login_page = LoginPage()
        screen = Screen(name= "LoginScreen")
        screen.add_widget(self.login_page)
        self.screen_manager.add_widget(screen)
        return self.screen_manager

    def chat_page(self):
        self.chat_page = ChatPage()
        screen = Screen(name= "ChatScreen")
        screen.add_widget(self.chat_page)
        self.screen_manager.add_widget(screen) 

    def save_alias_page(self):
        self.save_alias_page = SaveAliasPage()
        screen = Screen(name= "SaveAliasScreen")
        screen.add_widget(self.save_alias_page)
        self.screen_manager.add_widget(screen) 

    def record_meeting_page(self):
        self.record_meeting_page = RecordMeetingPage()
        screen = Screen(name= "RecordMeetingScreen")
        screen.add_widget(self.record_meeting_page)
        self.screen_manager.add_widget(screen) 
        
    def load_alias_page(self):
        self.load_alias_page = LoadAliasPage()
        screen = Screen(name= "LoadAliasScreen")
        screen.add_widget(self.load_alias_page)
        self.screen_manager.add_widget(screen) 
        
    

if __name__ == "__main__":
    o_s = MainApp()
    o_s.run()