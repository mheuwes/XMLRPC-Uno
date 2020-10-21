class Player:
    def __init__(self, name):
        self.name = name
        self.events = []
        self.handKarten = []

    def finished(self):
        return len(self.handKarten) == 0

    def karteGelegt(self, karte):
        try:
            self.handKarten.remove(karte)
        except ValueError:
            raise ValueError("Diese Karte besitze ich nicht")

    def karteGezogen(self, karte):
        self.handKarten.append(karte)
