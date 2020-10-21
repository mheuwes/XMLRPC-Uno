class Card:
    def __init__(self, color, value):
        self._color = color
        self._value = value

    def _color_getter(self):
        return self._color

    def _value_getter(self):
        return self._value

    color = property(_color_getter)
    value = property(_value_getter)

    def compatible(self, other):
        return (self.value == other.value) or (self.color == other.color)

    def serialize(self):
        return self.color, self.value

    @classmethod
    def deserialize(cls, x) -> 'Card':
        return cls(x[0], x[1])

    def __str__(self):
        return "(%s %s)" % (self.color, self.value)

    def __repr__(self):
        return "<Karte: %s, %s>" % (self.color, self.value)

    def __eq__(self, other):
        return self.color == other.color and self.value == other.value
