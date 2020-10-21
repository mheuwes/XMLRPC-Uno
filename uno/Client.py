import xmlrpc.client
import time
import readline
import os, sys, select

readline.parse_and_bind("")

import shutil

def get_terminal_columns():
    return shutil.get_terminal_size().columns

from .Card import Card

class Player:
    def __init__(self, adresse, name):
        self.connection = xmlrpc.client.Server(adresse)

        self.idx = self.connection.connect(name)

        self.cards = []
        self.enemies = {}
        self.topCard = None
        self.active = -1
        self.play()

    def zieheKarte(self):
        c = self.connection.zieheKarte(self.idx)
        self.cards.append(Card(c[0], c[1]))

    def drawField(self, active):
        os.system('clear')
        print('-' * get_terminal_columns())
        if active != -1:
            if not self.topCard is None:
                print('TopCard: %s' % self.topCard)
            else:
                print("TopCard: x")

            print()
        print("Spieler:")
        for pidx, (pkarten, pname) in self.enemies.items():
            print("{0:30s}".format(f" {pname} ({pidx}) {pkarten}") + ("  <----" if pidx == active else ""))

        if active != -1:
            print("Handkarten:")
            for x in self.cards:
                print(x, end=" ")
            print()
        else:
            print("Press ANY key to start:")

    def play(self):
        started = False
        while(True):
            events = self.connection.getEvents(self.idx)
            player = -1
            for (name, value) in events:
                if name == "start":
                    started = True
                    pl = value["players"]
                    for pid, plname in pl:
                        self.enemies[pid] = [6, plname] #Am Anfang 6 karten auf der Hand
                    cs = value["cards"]
                    for (color, val) in cs:
                        self.cards.append(Card(color,val))
                elif name == "spieler":
                    for pid, plname in value:
                        self.enemies[pid] = [6, plname] #Am Anfang 6 karten auf der Hand
                    self.drawField(-1)
                elif name == "gelegteKarte":
                    (pid, (color, val)) = value
                    self.topCard = Card(color,val)
                    self.enemies[pid][0] -= 1
                elif name == "gezogeneKarte":
                    self.enemies[value][0] += 1
                elif name == "aktiverSpieler":
                    player = value
                    self.drawField(value)
                elif name == "ende":
                    #spiel zuende
                    print("Spiel ist zuende:")
                    for (rank, pid) in value:
                        print("{}. Platz: {} ({})".format(rank + 1, self.enemies[pid][1], pid))
                    return
                else:
                    print(f"Unbekanntes Event: {name}")


            if player == self.idx:
                #bin selbst dran
                self.playCard()

            if not started:
                i, o, e = select.select([sys.stdin], [], [], 0.5)
                if i:
                    self.connection.start()
            else:
                time.sleep(0.5) #1 Sekunde warten


    def compatibleCardsOnHand(self):
        if not self.topCard:
            return True
        for x in self.cards:
            if self.topCard.compatible(x):
                return True
        return False



    def playCard(self):
        #todo karte checken
        if self.compatibleCardsOnHand():
            try:
                color = input("Farbe? ")
                value = input("Value? ")
                self.connection.legeKarte(self.idx,color, value)
                self.cards.remove(Card(color, value))
            except xmlrpc.client.Fault:
                self.playCard()
        else:
            print("Du kannst wohl nicht legen. Karte wird gezogen.")
            self.zieheKarte()
