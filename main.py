import kivy 

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
from datetime import date, datetime, timedelta
import mysql.connector
from plyer import notification
import smtplib, ssl
import re


WindowSize = Window.size
Window.clearcolor = (33/255, 33/255, 33/255, 1)

Config.set('graphics', 'width', '360')
Config.set('kivy','window_icon','FoodTruckfinderLogo.png')
Config.write()

Builder.load_file('FoodTruckFinderApp.kv')

robotoSlab = 'RobotoSlab-Medium.ttf'


port = 465
emailPassword = "Kenyadog!"
smtp_server = "smtp.gmail.com"
senderEmail = "alexandertesting06@gmail.com"

htmlMSG = """Subject: Thanks For Creating a FoodTruckFinderMI Account!
            

            We hope you enjoy our new app!!
        """

# The ScreenManager controls movin0 between screens
screen_manager = ScreenManager()

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


cnx = mysql.connector.connect(
    user='app',
    password='Cian62016!',
    host='216.137.179.68',
    database="test"
)

cursor = cnx.cursor()

class MainApp(App):
    
    
    def build(self):
        
        return screen_manager

    

    def on_start(self):
        cursor.execute("SHOW TABLES")
        print(cursor.fetchall())
        print('start')



appInst = MainApp()


class StartScreen(Screen):
    pass

class LoginScreen(Screen):
    def login(self):
        emailValue = self.ids['email'].text
        passwordValue = self.ids['password'].text
        
        cursor.execute(f"SELECT email from users WHERE email='{email}' AND password = '{password}';")

        cur.execute(statement)
        if not cur.fetchone():  # An empty result evaluates to False.
            print("Login failed")
        else:
            screen_manager.transition.direction = 'left'
            screen_manager.current = 'user_screen'









    def back(self):
        screen_manager.transition.direction = 'right'
        screen_manager.current = "start_screen"
        

class CreateAccountScreen(Screen):
    def back(self):
        screen_manager.transition.direction = 'right'
        screen_manager.current = "start_screen"

    def createAccount(self):
        emailValue = str(self.ids['email'].text)
        usernameValue = str(self.ids['username'].text)
        passwordValue = str(self.ids['password'].text)

        if(re.fullmatch(regex, emailValue)):
            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'FoodTruckFinderMI Account'
            msg['From'] = senderEmail
            msg['To'] = emailValue


            emailbody = MIMEText(htmlMSG, 'plain')
            msg.attach(emailbody)
            cursor.execute(f"INSERT INTO users (email, username, password) VALUES ('{emailValue}', '{usernameValue}', '{passwordValue}')")
            cnx.commit()
            context = ssl.create_default_context()

            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(senderEmail, emailPassword)
                server.sendmail(senderEmail, emailValue, htmlMSG)
            
            screen_manager.transition.direction = 'left'
            screen_manager.current = 'user_screen'
        else:
            label = Label(text='Invalid Email Address', font=robotoSlab, color=(1, 0, 0, 1), padding=(0, 20))
            self.add_widget(label)
            
 
        
            


    

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
cnx.close()