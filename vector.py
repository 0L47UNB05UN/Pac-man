from math import sqrt


class Vector2D:

    def __init__(self, x_axis = 0, y_axis = 0):
        try:
            if len(x_axis) == 2 and not ( type(x_axis[0]) == str or type(x_axis[1]) == str ):
                self.x = x_axis[0]
                self.y = x_axis[1]
            else:
                raise SyntaxError("Iterable must be len 2 and type int")
        except TypeError:
            if type(x_axis) == str or type(y_axis) == str:
                raise TypeError(f"Type must be int x_axis: {type(x_axis)}, y_axis: {type(y_axis)}")
            self.x = x_axis
            self.y = y_axis

    @staticmethod
    def UP():
        return Vector2D(0, -1)
    @staticmethod
    def DOWN():
        return Vector2D( 0, 1 )

    @staticmethod
    def RIGHT():
        return Vector2D( 1, 0 )

    @staticmethod
    def LEFT():
        return Vector2D( -1, 0 )

    @staticmethod
    def ZERO():
        return Vector2D()

    def length(self):
        return sqrt( ( (self.x**2) + (self.y**2) ) )

    def normalized(self):
        m = self.length()
        return Vector2D( self.x / m, self.y / m ) if m > 0 else Vector2D()

    def distance_to(self, point):
        x = abs(self.x - point.x)
        y = abs(self.y - point.y)
        return sqrt(x**2 + y**2)

    def mult(self, val):
        return Vector2D(self.x * val, self.y * val)

    def add( self, vector ):
        return Vector2D( self.x + vector.x, self.y + vector.y )

    def direction_to(self, point):
        x, y = 0, 0
        if point.x > self.x:
            x = 1
        elif point.x < self.x:
            x = -1
        elif point.y > self.y:
            y = 1
        elif point.y < self.y:
            y = -1            
        return Vector2D( x, y ).normalized()

    def direction( self ):
        return Vector2D ( self.x // abs(self.x) if self.x else 0, self.y // abs(self.y) if self.y else 0 )

    def is_equal(self, vector):
        if self.x != vector.x or self.y != vector.y:
            return False
        return True

    def coord_direction(self):
        if not self.x and not self.y:
            return "normal"
        else:
            if self.x:
                return "right" if self.x > 0 else "left"
            elif self.y:
                return "down" if self.y > 0 else "up"
            



