from graphics import Line, Point


class Cell:
    def __init__(self, win=None):
        self.__win = win
        self.__x1 = -1
        self.__y1 = -1
        self.__x2 = -1
        self.__y2 = -1
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        if self.__win is None:
            return
        if self.has_left_wall:
            self.__win.draw_line(Line(Point(x1, y1), Point(x1, y2)), "black")
        else:
            self.__win.draw_line(Line(Point(x1, y1), Point(x1, y2)), "white")
        if self.has_right_wall:
            self.__win.draw_line(Line(Point(x2, y1), Point(x2, y2)), "black")
        else:
            self.__win.draw_line(Line(Point(x2, y1), Point(x2, y2)), "white")
        if self.has_top_wall:
            self.__win.draw_line(Line(Point(x1, y1), Point(x2, y1)), "black")
        else:
            self.__win.draw_line(Line(Point(x1, y1), Point(x2, y1)), "white")
        if self.has_bottom_wall:
            self.__win.draw_line(Line(Point(x1, y2), Point(x2, y2)), "black")
        else:
            self.__win.draw_line(Line(Point(x1, y2), Point(x2, y2)), "white")

    def draw_move(self, to_cell, undo=False):
        fill_color = "gray" if undo else "red"

        if self.__win is None:
            return

        x_center = (self.__x1 + self.__x2) // 2
        y_center = (self.__y1 + self.__y2) // 2

        to_x_center = (to_cell.__x1 + to_cell.__x2) // 2
        to_y_center = (to_cell.__y1 + to_cell.__y2) // 2

        line = Line(Point(x_center, y_center), Point(to_x_center, to_y_center))
        self.__win.draw_line(line, fill_color)
