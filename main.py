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
from kivy.graphics import Color, Rectangle, Canvas
from kivy.lang import Builder
from datetime import date, datetime, timedelta
import mysql.connector
from plyer import notification
import smtplib, ssl
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import partial
from kivy_garden.mapview import MapView


WindowSize = Window.size
Window.clearcolor = (33/255, 33/255, 33/255, 1)

Config.set('graphics', 'width', '360')
Config.set('kivy','window_icon','FoodTruckfinderLogo.png')
Config.write()

Builder.load_file('FoodTruckFinderApp.kv')

robotoSlab = 'Azonix.otf'


port = 465
emailPassword = "Kenyadog!"
smtp_server = "smtp.gmail.com"
senderEmail = "alexandertesting06@gmail.com"

htmlMSG = """Subject: Thanks For Creating a FoodTruckFinderMI Account!
            

            We hope you enjoy our new app!!
        """
truckMSG = """Subject: Thanks For Registering Your Truck ON FoodTruckFinderMI


            Thanks, we hope you enjoy the new app"""

# The ScreenManager controls movin0 between screens
screen_manager = ScreenManager()

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


truckPageName = ''
truckPageFood = ''
truckPageOpen = False

truckTitleLabel = None
selectedTruck = []


#SSH command ssh root@216.137.179.68 -p7822


cnx = mysql.connector.connect(
    user='app',
    password='Cian62016!',
    host='216.137.179.68',
    database="test"
)

cursor = cnx.cursor()


color = (200, 200, 200, .5)


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
        
        cursor.execute(f"SELECT email from users WHERE email='{emailValue}' AND password = '{passwordValue}';")

        
        if not cursor.fetchone():  # An empty result evaluates to False.
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

            try:
                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(senderEmail, emailPassword)
                    server.sendmail(senderEmail, emailValue, htmlMSG)
                
                
            except:
                screen_manager.transition.direction = 'left'
                screen_manager.current = 'user_screen'
                
        else:
            label = Label(text='Invalid Email Address', font=robotoSlab, color=(1, 0, 0, 1), padding=(0, 20))
            self.add_widget(label)
            
class TruckStartScreen(Screen):
    def back(self):
        screen_manager.transition.direction = 'up'
        screen_manager.current = "start_screen"
        
class CreateTruckScreen(Screen):
    def back(self):
        screen_manager.transition.direction = 'right'
        screen_manager.current = "truck_start_screen"

    def createAccount(self):
        emailValue = str(self.ids['email'].text)
        truckNameValue = str(self.ids['truck_name'].text)
        foodTypeValue = str(self.ids['food_type'].text)
        passwordValue = str(self.ids['password'].text)

        if(re.fullmatch(regex, emailValue)):
            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'FoodTruckFinderMI Account'
            msg['From'] = senderEmail
            msg['To'] = emailValue
                

            emailbody = MIMEText(truckMSG, 'plain')
            msg.attach(emailbody)
            cursor.execute(f"INSERT INTO trucks (email, truckname, password, foodtype, isopen) VALUES ('{emailValue}', '{truckNameValue}', '{passwordValue}', '{foodTypeValue}', {False})")
            cnx.commit()
            context = ssl.create_default_context()

            try:
                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(senderEmail, emailPassword)
                    server.sendmail(senderEmail, emailValue, htmlMSG)
                
                
            except:

                screen_manager.transition.direction = 'left'
                screen_manager.current = 'truck_screen'
                
            else:
                label = Label(text='Invalid Email Address', font_name=robotoSlab, color=(1, 0, 0, 1), padding=(0, 20))
                self.add_widget(label)






class TruckLoginScreen(Screen):
    def login(self):
        emailValue = self.ids['email'].text
        passwordValue = self.ids['password'].text
        truckNameValue = self.ids["truck_name"].text

        
        cursor.execute(f"SELECT email from trucks WHERE email='{emailValue}' AND truckname='{truckNameValue}' AND password='{passwordValue}';")

        
        if not cursor.fetchone():  # An empty result evaluates to False.clause
            print("Login failed")
        else:
            screen_manager.transition.direction = 'left'
            screen_manager.current = 'truck_screen'



    def back(self):
        screen_manager.transition.direction = 'right'
        screen_manager.current = "truck_start_screen"


    

    


class UserScreen(Screen):
    def load_Trucks(self):
        global truckPageName
        global truckPageFood
        global truckPageOpen
        global cnx
        
        self.ids['LayoutForTrucks'].clear_widgets()

        cnx.close()
        cnx = mysql.connector.connect(
            user='app',
            password='Cian62016!',
            host='216.137.179.68',
            database="test"
        )

        cursor = cnx.cursor()
        
        foodtypeOffset = 0
        isopenOffset = 0

        cursor.execute("SELECT truckname FROM trucks")
        trucknames = cursor.fetchall()

        cursor.execute("SELECT foodtype FROM trucks")
        truckfoodtypes = cursor.fetchall()

        cursor.execute("SELECT isopen FROM trucks")
        truckisopen = cursor.fetchall()

        for x in trucknames:
            print(x[0])
            print(truckfoodtypes[foodtypeOffset][0])
            print(truckisopen[isopenOffset][0])



            nameLabel = Label(text='Truck Name: ', font_name=robotoSlab)
            truckNameLabel = Label(text=str(x[0]), font_name=robotoSlab)
            foodLabel = Label(text="Food Type: ", font_name=robotoSlab)
            foodTypeLabel = Label(text=str(truckfoodtypes[foodtypeOffset][0]), font_name=robotoSlab)
            openLabel = Label(text="Currently Open: ", font_name=robotoSlab)
            if truckisopen[isopenOffset][0] == 0:
                isOpenLabel = Label(text="Closed", font_name=robotoSlab)
            elif truckisopen[isopenOffset][0] == 1:
                isOpenLabel = Label(text="Open", font_name=robotoSlab)
            box = BoxLayout(orientation='vertical')
            layout = GridLayout(cols = 2, padding=(0, 0, 0, 20))


            #initPage(self, x[0], truckfoodtypes[foodtypeOffset][0], truckisopen[isopenOffset][0])
            openPageButton = Button(text='Open Page', size_hint_y=.4)
            openPageButton.bind(on_press=partial(self.select_Truck, x[0], truckfoodtypes[foodtypeOffset][0], truckisopen[isopenOffset][0]))
            
            
            

            layout.add_widget(nameLabel)
            layout.add_widget(truckNameLabel)
            layout.add_widget(foodLabel)
            layout.add_widget(foodTypeLabel)
            layout.add_widget(openLabel)
            layout.add_widget(isOpenLabel)
            box.add_widget(layout)
            box.add_widget(openPageButton)
            


            buttonText = self.ids['LayoutForTrucks'].add_widget(box)



            foodtypeOffset += 1
            isopenOffset += 1
        


    def select_Truck(self, name, food, isOpen, button):
        truckInfoMenu = button.parent.parent.parent.parent.parent.parent.children[1].children[2].children[0].children[2]

        #Setup Selected Truck Panel, add new widgets including mapview, truck name, is open, and food type. and a refresh button.

        box = BoxLayout(orientation='vertical')
        titleBox = BoxLayout(orientation='horizontal', size_hint_y=.1, padding=(0, 20, 0, 0))
        layout = GridLayout(cols=2, size_hint_y=.2)
        placeholderBox = BoxLayout(orientation='vertical')
        mapbox = BoxLayout(orientation='vertical')

        truckTitle = Label(text=name, font_name=robotoSlab, font_size=20)
        currentlyOpenDesc = Label(text='Status:')
        if isOpen == 0:
            currentlyOpen = Label(text="Closed", font_name=robotoSlab, color=(1, 0, 0, 1))
        elif isOpen == 1:
            currentlyOpen = Label(text="Open", font_name=robotoSlab, color=(0, 1, 0, 1))


        foodTypeDesc = Label(text='Food:', font_name=robotoSlab)
        foodType = Label(text=food, font_name=robotoSlab)

        truckMap = MapView(zoom=11, lat=-33.867, lon=151.206)


        layout.add_widget(foodTypeDesc)
        layout.add_widget(foodType)
        layout.add_widget(currentlyOpenDesc)
        layout.add_widget(currentlyOpen)

        titleBox.add_widget(truckTitle)
        
        mapbox.add_widget(truckMap)

        box.add_widget(titleBox)
        box.add_widget(layout)
        box.add_widget(mapbox)
        

        truckInfoMenu.add_widget(box)







    def print_childs(self):
        print(self.children[0].children[0].children[0].children[0].children[0].children[0].children)
    



class TruckScreen(Screen):
    def change_status(self): 
        if self.ids['statusLabel'].text == 'Closed':
            self.ids['statusLabel'].text = 'Open'
            self.ids['statusLabel'].color = (0, 1, 0, 1)
            cursor.execute("""UPDATE trucks SET isopen = 1 WHERE isopen = 0""")
            cnx.commit()


        elif self.ids['statusLabel'].text == 'Open':
            self.ids['statusLabel'].text = 'Closed'
            self.ids['statusLabel'].color = (1, 0, 0, 1)
            cursor.execute("""UPDATE trucks SET isopen = 0 WHERE isopen = 1""")
            cnx.commit()



screen_manager.add_widget(StartScreen(name ="start_screen"))
screen_manager.add_widget(LoginScreen(name ="login_screen"))
screen_manager.add_widget(CreateAccountScreen(name="create_account_screen"))
screen_manager.add_widget(TruckStartScreen(name="truck_start_screen"))
screen_manager.add_widget(CreateTruckScreen(name='create_truck_screen'))
screen_manager.add_widget(TruckLoginScreen(name='truck_login_screen'))
screen_manager.add_widget(UserScreen(name ="user_screen"))
screen_manager.add_widget(TruckScreen(name='truck_screen'))


  
# run the app 

appInst.run()
cnx.close()