import kivy 
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.pagelayout import PageLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex
from kivy.uix.stacklayout import StackLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import (ScreenManager, Screen, NoTransition,
SlideTransition, CardTransition, SwapTransition,
FadeTransition, WipeTransition, FallOutTransition, RiseInTransition) 
from kivy.lang import Builder

from plyer import notification

WindowSize = Window.size
Window.clearcolor = (33/255, 33/255, 33/255, 1)

Config.set('graphics', 'width', '360')
Config.set('kivy','window_icon','FoodTruckfinderLogo.png')
Config.write()

Builder.load_file('FoodTruckFinderApp.kv')

robotoSlab = 'RobotoSlab-Medium.ttf'


# The ScreenManager controls moving between screens
screen_manager = ScreenManager()


class MainApp(App):
    
    
    def build(self):
        
        return screen_manager

    

    def on_start(self):
        print('start')



appInst = MainApp()


class StartScreen(Screen):
    pass

class LoginScreen(Screen):
    def login(self):
        text = self.ids['newtext'].text
        print(text)
        screen_manager.current = 'user_screen'
        

class CreateAccountScreen(Screen):
    def back(self):
        screen_manager.transition.direction = 'right'
        screen_manager.current = "start_screen"
    
   
class UserScreen(Screen):
    def load_Trucks(self):
        box = Button()
        buttonText = self.ids['LayoutForTrucks'].add_widget(box)
        


screen_manager.add_widget(StartScreen(name ="start_screen"))
screen_manager.add_widget(LoginScreen(name ="login_screen"))
screen_manager.add_widget(CreateAccountScreen(name="create_account_screen"))
screen_manager.add_widget(UserScreen(name ="user_screen"))




  
# run the app 

appInst.run()