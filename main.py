from tkinter import Tk, BOTH, Canvas
import time

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas: Canvas, fill_color="black"):
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2)

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title("My Window")
        self.__root.geometry(f"{self.width}x{self.height}")
        self.__canvas = Canvas(self.__root, bg="white", width=self.width, height=self.height)
        self.__canvas.pack(fill=BOTH, expand=True)
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__running = False

    def draw_line(self, line: Line, fill_color="black"):
        line.draw(self.__canvas, fill_color)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False

class Cell:
    def __init__(self, win: Window):
        self.__win = win
        self.__x1 = -1
        self.__y1 = -1
        self.__x2 = -1
        self.__y2 = -1
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True

    def draw(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        if self.__win is None: return
        if self.has_left_wall:
            self.__win.draw_line(Line(Point(x1, y1), Point(x1, y2)))
        if self.has_right_wall:
            self.__win.draw_line(Line(Point(x2, y1), Point(x2, y2)))
        if self.has_top_wall:
            self.__win.draw_line(Line(Point(x1, y1), Point(x2, y1)))
        if self.has_bottom_wall:
            self.__win.draw_line(Line(Point(x1, y2), Point(x2, y2)))

    def draw_move(self, to_cell, undo=False):
        fill_color = "gray" if undo else "red"

        if self.__win is None: return

        x_center = (self.__x1 + self.__x2) // 2
        y_center = (self.__y1 + self.__y2) // 2

        to_x_center = (to_cell.__x1 + to_cell.__x2) // 2
        to_y_center = (to_cell.__y1 + to_cell.__y2) // 2

        line = Line(Point(x_center, y_center), Point(to_x_center, to_y_center))
        self.__win.draw_line(line, fill_color)

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
    ):
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__cells = []
        self.__create_cells()

    def __create_cells(self):
        for i in range(self.__num_cols):
            col = []
            for j in range(self.__num_rows):
                col.append(Cell(self.__win))
            self.__cells.append(col)

        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__draw_cell(i, j)


     
    def __draw_cell(self, i, j):
        if i < 0 or i >= self.__num_cols or j < 0 or j >= self.__num_rows:
            return
        if self.__win is None:
            return
        x1 = self.__x1 + i * self.__cell_size_x
        y1 = self.__y1 + j * self.__cell_size_y
        x2 = x1 + self.__cell_size_x
        y2 = y1 + self.__cell_size_y
        self.__cells[i][j].draw(x1, y1, x2, y2)

        self.__animate()
        print(f"Drawn cell ({i}, {j})")
    
    def __animate(self):
        if self.__win is None:
            return
        self.__win.redraw()
        time.sleep(0.05)



def main():
    num_rows = 12
    num_cols = 16
    margin = 50
    screen_x = 800
    screen_y = 600

    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows

    win = Window(screen_x, screen_y)
    Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win)
    win.wait_for_close()

if __name__ == "__main__":
    main()