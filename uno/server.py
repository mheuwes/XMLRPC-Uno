from xmlrpc.server import SimpleXMLRPCServer
from threading import Thread

from .Card import Card
from .DeckUNO import DeckUNO
from .Player import Player
from .exceptions import *

STATE_LOBBY = 1
STATE_PLAYING = 2
STATE_FINISHED = 3

class ServerThread(Thread):
    def __init__(self, x: SimpleXMLRPCServer):
        Thread.__init__(self)
        self.server = x

    def run(self):
        self.server.serve_forever()

class Server:
    def __init__(self):
        self._deck = DeckUNO()
        self._playedCards: list[Card] = []
        self._players: list[Player] = []
        self._activeIdx = -1
        self._state = STATE_LOBBY
        self._finished = {}

    def _event(self, evt_name, evt_val):
        for (xid, xpl) in enumerate(self._players):
            xpl.events.append((evt_name, evt_val))

    def _finish(self, reason_talon: bool):
        self._state = STATE_FINISHED
        if not reason_talon:
            for xid in range(len(self._players)):
                if xid not in self._finished:
                    self._finished[xid] = len(self._finished)

        self._event("ende", [(x[1], x[0]) for x in self._finished.items()])
        print("Ende!", self._finished)

    def connect(self, name: str) -> int:
        if self._state != STATE_LOBBY:
            raise ValueError("Current State is not lobby!")

        if name in [pl.name for pl in self._players]:
            raise ValueError("Invalid player name")

        pl = Player(name)
        self._players.append(pl)
        plidx = self._players.index(pl)
        print("New player joined: %s (%s)" % (name, plidx))
        self._event('spieler', [(xid, xpl.name) for (xid, xpl) in enumerate(self._players)])
        return plidx

    def legeKarte(self, idx, color, value):
        if self._state != STATE_PLAYING:
            raise ValueError("Current state is not playing!")
        if idx != self._activeIdx:
            raise ValueError("You are not the active player!")
        pl = self._players[idx]

        karte = Card.deserialize((color, value))

        print("%s will %s legen" % (idx, karte))
       # print("er hat %s" % pl.handKarten)
        if self._playedCards:
            if not karte.compatible(self._playedCards[-1]):
                raise ValueError("This card is not playable.")


        pl.karteGelegt(karte) # checks if card is present

        self._playedCards.append(karte)
        self._event("gelegteKarte", (idx, (color, value)))

        for (xid, xpl) in enumerate(self._players):
            if xpl.finished() and xid not in self._finished:
                self._finished[xid] = len(self._finished)

        if len(self._finished) >= len(self._players) - 1:
            self._finish(False)
            return

        self._activeIdx = (self._activeIdx + 1) % len(self._players)

        self._event("aktiverSpieler", self._activeIdx)
        print("Player %s (%s) hat %s gelegt! Neuer Spieler: %s" % (pl.name, idx, karte, self._activeIdx))
        return

    def zieheKarte(self, idx):
        if self._state != STATE_PLAYING:
            raise ValueError("Current state is not playing!")
        if idx != self._activeIdx:
            raise ValueError("You are not the active player!")
        pl = self._players[idx]

        if len(self._deck) == 0:
            self._finish(True)
            return

        card = self._deck.pop()
        pl.karteGezogen(card)
        self._event('gezogeneKarte', idx)

        self._activeIdx = (self._activeIdx + 1) % len(self._players)

        self._event("aktiverSpieler", self._activeIdx)
        print("Spieler %s (%s) hat Karte gezogen." % (pl.name, idx))
        return card.serialize()

    def getEvents(self, idx):
        pl = self._players[idx]
        evts = pl.events
        pl.events = []
        return evts

    def start(self):
        if self._state != STATE_LOBBY:
            raise ValueError("Not startable!")

        if len(self._players) < 2:
            raise ValueError("Not enough players!")

        print("Spiel wird gestartet...")
        players = [(xid, xpl.name) for (xid, xpl) in enumerate(self._players)]
        for (xid, xpl) in enumerate(self._players):
            for _ in range(6):
                card = self._deck.pop(0)
                xpl.karteGezogen(card)

            xpl.events.append(("start", {
                "cards": [x.serialize() for x in xpl.handKarten],
                "players": players,
            }))

        self._activeIdx = 0
        self._event("aktiverSpieler", self._activeIdx)
        self._state = STATE_PLAYING

        return

    def debug(self):
        return [(xid, xpl.name, [x.serialize() for x in xpl.handKarten]) for xid, xpl in enumerate(self._players)]

def get_server(host, port):
    x = Server()
    server = SimpleXMLRPCServer((host, port), allow_none=True, logRequests=False)
    server.register_instance(x)
    server.register_introspection_functions()
    return (x, server)

def start_server(host='localhost', port=8080):
    server, rpcserver = get_server(host, port)
    thread = ServerThread(rpcserver)
    thread.start()
    print("after serve forever")
    return server

def start_server_foreground(host, port):
    server, rpcserver = get_server(host, port)
    rpcserver.serve_forever()
