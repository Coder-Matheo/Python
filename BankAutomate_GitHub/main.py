#python -m pip install https://github.com/kivy/kivy/archive/master.zip  kivy installtion
#python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew;
#python -m pip install https://github.com/kivy/kivy/archive/master.zip  kivy installtion
#pip install matplotlib==3.0.0
#for kivy figurue, you should use python 3.7

#alle the libriry would install

import kivy
import numpy as np
from kivy.app import App
from kivy.core import window
from kivy.graphics import Color
from kivy.graphics import Canvas
from kivy.graphics import Ellipse
from kivy.graphics import Rectangle
from kivy.graphics import RoundedRectangle
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.core.image import Image
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.config import Config
from kivy.factory import Factory
from kivy.utils import get_color_from_hex
from kivy.properties import ObjectProperty, StringProperty
import csv
import time
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import re
import socket

Window.size = (400,680)
Config.set('graphics', 'resizable', True)
kivy.require('1.9.0')


HEADER = 64
PORT = 5050 #port yahoo masanger
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "127.0.0.1" #depends which client(ipv4) to be connecting
ADDR = (SERVER,PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length =str(msg_length).encode(FORMAT)#ensure our message, how much big.
    send_length += b' '*(HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))
"""
send(DISCONNECT_MESSAGE)#for to again connecting
"""



class VerwalteterGeldbetrag:
    def __init__(self, anfangsbetrag):
        self.Betrag = anfangsbetrag

    def einzahlenMoeglich(self, betrag):
        return True

    def auszahlenMoeglich(self, betrag):
        return True

    def einzahlen(self, betrag):
        if betrag < 0 or not self.einzahlenMoeglich(betrag):
            return False
        else:
            self.Betrag += betrag
            return True

    def auszahlen(self, betrag):
        if betrag < 0 or not self.auszahlenMoeglich(betrag):
            return False
        else:
            self.Betrag -= betrag
            return True

    def zeige(self):
        print("Betrag : {:.2f}".format(self.Betrag))


class AllgemeinesKonto(VerwalteterGeldbetrag):
    def __init__(self, kundendaten, kontostand):
        # kontostand Value von hier zu VerwalteterGeldbetrag function(__init__) abgegeben.
        super().__init__(kontostand)
        self.Kundendaten = kundendaten

    def geldtransfer(self, ziel, betrag):
        # für geldtransfer schickt(Verwalt..), dann überprüft.wenn ist True function erweitert.
        if self.auszahlenMoeglich(betrag) and ziel.einzahlenMoeglich(betrag):
            self.auszahlen(betrag)
            self.einzahlen(betrag)
            return True
        else:
            return False

    def zeige(self):
        self.Kundendaten.zeige()
        VerwalteterGeldbetrag.zeige(self)


class AllgemeinesKontoMitTagesumsatz(AllgemeinesKonto):
    def __init__(self, kundendaten, kontostand, max_tagesumsatz=1500):
        # initialisieren Parameter die function AllgemeinesKonto
        super().__init__(kundendaten, kontostand)
        self.MaxTagesumsatz = max_tagesumsatz
        self.UmsatzHeute = 0.0

    def transferMoeglich(self, betrag):
        return (self.UmsatzHeute + betrag <= self.MaxTagesumsatz)

    def auszahlenMoeglich(self, betrag):
        return self.transferMoeglich(betrag)

    def einzahlenMoeglich(self, betrag):
        return self.transferMoeglich(betrag)

    def einzahlen(self, betrag):
        if AllgemeinesKonto.einzahlen(self, betrag):
            self.UmsatzHeute += betrag
            return True
        else:
            return False

    def auszahlen(self, betrag):
        if AllgemeinesKonto.auszahlen(self, betrag):
            self.UmsatzHeute += betrag
            return True
        else:
            return False

    def zeige(self):
        AllgemeinesKonto.zeige(self)
        print("Heute schon {:.2f} von {:.2f} Euro umgesetzt".format(
            self.UmsatzHeute, self.MaxTagesumsatz))





class GirokontoKundendaten:
    def __init__(self, inhaber, kontonummer):
        self.Inhaber = inhaber
        self.Kontonummer = kontonummer

    def zeige(self):
        print("Inhaber: ", self.Inhaber)
        print("kontonummer: ", self.Kontonummer)


class GirokontoMitTagesumsatz(AllgemeinesKontoMitTagesumsatz):
    def __init__(self, inhaber, kontonummer, kontostand, max_tagesumsatz=1500):
        kundendaten = GirokontoKundendaten(inhaber, kontonummer)
        super().__init__(kundendaten, kontostand, max_tagesumsatz)


class VerwalteterBargeldbetrag(VerwalteterGeldbetrag):
    def __init__(self, bargeldbetrag):
        if bargeldbetrag < 0:
            bargeldbetrag = 0
        super().__init__(bargeldbetrag)

    def auszahlenMoeglich(self, betrag):
        return (self.Betrag >= betrag)


class Geldboerse(VerwalteterBargeldbetrag):
    # TODO: Spezielle Methode fuer eine Geldboerse
    pass


class Tresor(VerwalteterBargeldbetrag):
    # TODO: Spezielle Methode fuer eine Tresor
    pass


class Girokonto(AllgemeinesKonto):
    def __init__(self, inhaber, kontonummer, kontostand):
        kundendaten = GirokontoKundendaten(inhaber, kontonummer)
        super().__init__(kundendaten, kontostand)


class NummernkontoKundendaten:
    def __init__(self, identifikationsnummer):
        self.Identifikationsnummer = identifikationsnummer
    def zeige(self):
        print("Identifikationsnummer:", self.Identifikationsnummer)


class Nummernkonto(AllgemeinesKonto):
    def __init__(self, identifikationsnummer, kontostand):
        kundendaten = NummernkontoKundendaten(identifikationsnummer)
        super().__init__(kundendaten, kontostand)


class NummernkontoMitTagesumsatz(AllgemeinesKontoMitTagesumsatz):
    def __init__(self, kontonummer, kontostand, max_tagesumsatz):
        kundendaten = NummernkontoKundendaten(kontonummer)
        super().__init__(kundendaten, kontostand, max_tagesumsatz)




Builder.load_file("Inh_menu.kv")
kv_menu = Builder.load_file("Dis_menu.kv")

date_and_time = time.localtime()
dater = time.strftime("%m/%d/%Y", date_and_time)
timer = time.strftime("%H/%M/%S", date_and_time)

tracfile = open('tracInfo.csv ', 'a', newline='')
fieldhead = ['TranNr','Transaction','Konto','Value','date','time']

writertrac = csv.DictWriter(tracfile, fieldnames=fieldhead)
#writertrac.writeheader()



class mainApp(App):
    kntShowKv = StringProperty('')
    knteinShowKv = StringProperty('')
    kntausShowKv = StringProperty('')
    tracNr = 1


    def popup(self, name):
        self._popups[name].open()

    def build(self):
        self._popups = {
            'einzahl': Factory.Einzal(),
            'auszahl': Factory.Auszahl(),
            'konto':Factory.Konto(),
            'passwordVergess':Factory.PassVergess()
        }
        return kv_menu

    def entryInfo(self,nameInfo,emailInfo,passwortInfo):
        self.nameInfo = nameInfo
        self.emailInfo = emailInfo
        self.passwortInfo = passwortInfo

        filterEmail = re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$",emailInfo)


        if (nameInfo != "" and filterEmail and passwortInfo != ""):

            try:
                self.conn = sqlite3.connect('cus_dBank.db')
                self.c = self.conn.cursor()

                """c.execute('''CREATE TABLE customer(
                                        id INTEGER PRIMARY KEY,
                                        name TEXT NOT NULL,
                                        email TEXT NOT NULL,
                                        pass TEXT NOT NULL,
                                        kontonum INTEGER,
                                        kontostand INTEGER)''')"""

                """c.execute("INSERT INTO customer VALUES(1, 'Matheo', 'ali.dinarvand1370@gmail.com', 'Matheo1370',11111111, 3500)")"""


                try:
                    self.c.execute("SELECT pass FROM customer WHERE name=? AND email=? AND pass=?",
                                   (self.nameInfo, self.emailInfo, self.passwortInfo,))
                    passKunIndb = self.c.fetchone()[0]
                    if self.passwortInfo == passKunIndb:
                        print("password is right")
                except:
                    print("your Info is wrong")
                    quit(0)
                    self.c.close()

                self.c.execute("SELECT * FROM customer WHERE name=? AND email=? AND pass=?", (self.nameInfo, self.emailInfo, self.passwortInfo,))

                if (self.c.fetchone()):
                    self.c.execute("SELECT * FROM customer WHERE name=? AND email=? AND pass=?", (self.nameInfo, self.emailInfo, self.passwortInfo,))
                    print(self.c.fetchone())

                else:
                    pass
                    #registeren

                    """if (self.newKontoNrIn.text != "" and self.newBetragIn.text != ""):
                        self.c.execute("INSERT INTO customer(name,email,pass,kontonum,kontostand) VALUES(?,?,?,?,?)",
                                  (self.nameInfo, self.emailInfo, self.passwortInfo.text, self.newKontoNrIn.text , self.newBetragIn.text))
                        print("New user created")
                    else:
                        print("Please enter your account number and your money")"""

                self.conn.commit()
                #conn.close()

            except sqlite3.Error as error:
                print("Error while creating a sqlite table", error)
                self.conn.close()
            finally:
                if (self.conn):
                    #conn.close()
                    print("sqlite connection is closed")




    def forgeinPass(self,nameFor,emailFor):
        self.conn = sqlite3.connect('cus_dBank.db')
        self.c = self.conn.cursor()
        self.c.execute("SELECT pass FROM customer WHERE name=? AND email=? ",
                       (nameFor, emailFor,))
        print(self.c.fetchone())
        print("forgein password",nameFor,emailFor)
        self.c.close()


    def kontoStand(self,kontoNrInTo):
        self.c.execute("SELECT kontonum FROM customer WHERE name=? AND email=? AND pass=?",
                       (self.nameInfo, self.emailInfo, self.passwortInfo,))
        self.kontoNrInto = self.c.fetchone()[0]
        self.kontoNrInTo = int(kontoNrInTo)

        if(self.kontoNrInto == self.kontoNrInTo):
            self.c.execute("SELECT kontostand FROM customer WHERE name=? AND email=? AND pass=?",
                           (self.nameInfo, self.emailInfo, self.passwortInfo,))
            self.kstand = self.c.fetchone()[0]
            print("Sie haben : ",self.kstand," in Ihre Konto")
            self.kntShowKv = str(self.kstand)
            msg = str("Ihre konto stand ist: " + str(self.kntShowKv))
            send(msg)
        else:
            print("Don't find")
    def einzahl(self,kontonrEinIn,betragEinIn):
        self.kontonrEinIn = int(kontonrEinIn)
        self.betragEinIn = int(betragEinIn)
        #(2, 'ali', 'ali.dinarvand1370@gmail.com', 'Matheo1370', 123456789, 5033)
        #(1, 'Matheo', 'ali.dinarvand1370@gmail.com', 'Matheo1370', 11111111, 3500)

        self.c.execute("SELECT kontostand,kontonum FROM customer WHERE name=? AND email=? AND pass=?",
                       (self.nameInfo, self.emailInfo, self.passwortInfo,))
        self.kstandein = self.c.fetchone()[0]

        self.c.execute("SELECT kontonum FROM customer WHERE name=? AND email=? AND pass=?",
                       (self.nameInfo, self.emailInfo, self.passwortInfo,))
        self.kontoNr = self.c.fetchone()[0]


        if(self.kontonrEinIn != "" and self.betragEinIn != ""):
            if(self.kontonrEinIn == self.kontoNr):

                self.nk4 = NummernkontoMitTagesumsatz(self.kontonrEinIn, self.kstandein, 8000)
                print("nk2.einzahlen(1500): ", self.nk4.einzahlen(int(self.betragEinIn)))

                newkontostand = int(self.betragEinIn) + int(self.kstandein)

                self.c.execute("Update customer set kontostand=? WHERE name=? AND email=? AND pass=?",(newkontostand, self.nameInfo, self.emailInfo, self.passwortInfo,))

                self.knteinShowKv = str(newkontostand)

                msg = str("Sie haben " + str(self.betragEinIn) + " eingezahlt, ihre konto ist: " + str(self.knteinShowKv))
                send(msg)
                self.conn.commit()
                self.nk4.zeige()
                self.tracNr += 1
                writertrac.writerow({'TranNr': self.tracNr, 'Transaction': 'Einzahlung','Konto':str(newkontostand), 'Value': str(self.betragEinIn), 'date': str(dater), 'time': str(timer)})
            else:
                print("Bitte geben richtige account nummer ein.")
        else:
            print("Bitte geben Ihre Antrag Geld ein.")



    def auszahl(self,kontonrAusIn,betragAusIn):
        self.kontonrAusIn = int(kontonrAusIn)
        self.betragAusIn = int(betragAusIn)

        self.c.execute("SELECT kontostand FROM customer WHERE name=? AND email=? AND pass=?",
                       (self.nameInfo, self.emailInfo, self.passwortInfo,))
        self.kstandaus = self.c.fetchone()[0]

        self.c.execute("SELECT kontonum FROM customer WHERE name=? AND email=? AND pass=?",
                       (self.nameInfo, self.emailInfo, self.passwortInfo,))
        self.kontoNrauszahl = self.c.fetchone()[0]

        if(self.kontonrAusIn != "" and self.betragAusIn != ""):
            if(int(self.kontoNrauszahl) == int(self.kontonrAusIn)):

                nk1 = NummernkontoMitTagesumsatz(self.kontonrAusIn, self.kstandaus, 8000)
                nk1.auszahlen(int(self.betragAusIn))
                newkontostand = int(self.kstandaus) - self.betragAusIn

                self.c.execute("Update customer set kontostand=? WHERE name=? AND email=? AND pass=?",
                               (newkontostand, self.nameInfo, self.emailInfo, self.passwortInfo,))

                self.kntausShowKv = str(newkontostand)

                msg = str("Sie haben " + str(self.betragAusIn) + " ausgezahlt, Ihre konto ist : " + str(self.kntausShowKv))
                send(msg)
                self.conn.commit()
                nk1.zeige()
                self.tracNr += 1
                writertrac.writerow({'TranNr': self.tracNr, 'Transaction': 'Auszahlung','Konto':str(newkontostand), 'Value': str(self.betragAusIn), 'date': str(dater), 'time': str(timer)})

            else:
                print("Bitte geben richtige account nummer ab.")
        else:
            print("Bitte gebe Ihre Antrag ein.")



    def diagramKonto(self):

        lsttracY = []
        lsttracX = []

        with open('tracInfo.csv', 'r') as tracToDiag:
            readertrac = csv.DictReader(tracToDiag)
            for trac in readertrac:
                lsttracY.append(int(trac['Value']))
                lsttracX.append(int(trac['TranNr']))

        import seaborn as sns

        with plt.style.context('dark_background'):
            #plt.stem(lsttracX, lsttracY)
            sns.lineplot(x=lsttracX, y=lsttracY)
        plt.ylabel('some numbers')

        data = pd.read_csv('tracInfo.csv')
        #data[data['Transaction']=='Einzahlung']['Value']
        #data[data['Transaction']=='Auszahlung']['Value']

        self.layout = GridLayout(cols=1, padding=10)
        self.uberInh = GridLayout(cols=1)
        self.uberMenu = GridLayout(cols=1)


        self.uberMenu.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        self.closeButton = Button(text="Close ", size_hint=(.1, .1))

        self.uberInh.add_widget(self.uberMenu)

        self.layout.add_widget(self.uberInh)
        self.layout.add_widget(self.closeButton)

        popup = Popup(title='Konto diagramm',
                      content=self.layout)
        popup.open()

        self.closeButton.bind(on_press=popup.dismiss)


# Run the app


class MyMainApp(App):
    def build(self):

        return mainApp()


if __name__ == '__main__':
    mainApp().run()
    tracfile.close()


