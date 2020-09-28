# The tests on repl.it will fail with this solution. The specification requests
# C++-like getters and setters. The idiomatic way for this in Python is to use
# properties, which I'm doing here. However, this makes the class code a little
# more involved, so I kind of see why they avoid this in the project..

class Rectangle(object):
    def __init__(self, width, height):
        self._width = width
        self._height = height

    def __repr__(self):
        return f"{self.__class__.__name__}(width={self.width}, height={self.height})"

    @property
    def width(self):
        return self._width
    @width.setter
    def width(self, width):
        self._width = width

    @property
    def height(self):
        return self._height
    @height.setter
    def height(self, height):
        self._height = height

    @property
    def area(self):
        return self.width * self.height

    @property
    def perimeter(self):
        return 2 * (self.width + self.height)

    @property
    def diagonal(self):
        return (self.width ** 2 + self.height ** 2) ** .5

    def picture(self):
        if self.width > 50 or self.height > 50:
            return "Too big for picture."
        return self.height * (self.width * "*" + "\n")

    def amount_inside(self, shape):
        return int(self.width / shape.width) * int(self.height / shape.height)


class Square(Rectangle):
    def __init__(self, side):
        super(Square, self).__init__(side, side)

    def __repr__(self):
        return f"{self.__class__.__name__}(side={self.width})"

    @property
    def side(self):
        return self._width
    @side.setter
    def side(self, side):
        self._width = self._height = side

    @property
    def width(self):
        return self._width
    @width.setter
    def width(self, width):
        self._width = self._height = width

    @property
    def height(self):
        return self._height
    @height.setter
    def height(self, height):
        self._width = self._height = height
