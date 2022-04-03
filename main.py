from doctest import OutputChecker
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
from pyspark import *
from tables import Cols

from pages.TransitionPage import TransitionPage
from Utils.functions import *
from backend_main import BackendMain
from controller.MainController import MainController

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

        self.new_message = TextInput(width = Window.size[0]*0.6, size_hint_max_x=None,multiline=False)
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


        bottom_line1 = GridLayout(cols=2)
        bottom_line1.add_widget(self.new_message)
        bottom_line1.add_widget(self.send)
        self.add_widget(bottom_line1)
        
        bottom_line2 = GridLayout(cols=5)
        bottom_line2.add_widget(self.logout_btn)
        bottom_line2.add_widget(self.save_alias)
        bottom_line2.add_widget(self.voice_input_btn)
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

    def save_alias_fn(self, _):
        self.new_message.text = "Save alias"
    def load_alias_fn(self, _):
        self.new_message.text = "Load alias"






















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
    

if __name__ == "__main__":
    o_s = MainApp()
    o_s.run()