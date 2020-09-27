class Rectangle(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __repr__(self):
        return f"{self.__class__.__name__}(width={self.width}, height={self.height})"

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def get_area(self):
        return self.width * self.height

    def get_perimeter(self):
        return 2 * (self.width + self.height)

    def get_diagonal(self):
        return (self.width ** 2 + self.height ** 2) ** .5

    def get_picture(self):
        if self.width > 50 or self.height > 50:
            return "Too big for picture."
        return self.height * (self.width * "*" + "\n")

    def get_amount_inside(self, shape):
        return int(self.width / shape.width) * int(self.height / shape.height)


class Square(Rectangle):
    def __init__(self, side):
        super(Square, self).__init__(side, side)

    def __repr__(self):
        return f"{self.__class__.__name__}(side={self.width})"

    def set_side(self, side):
        self.width = self.height = side

    def set_width(self, width):
        self.set_side(width)

    def set_height(self, height):
        self.set_side(height)
