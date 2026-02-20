import random
import time

from cell import Cell


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
        seed=None,
    ):
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self._cells = []
        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)
        self.__reset_cells_visited()

        if seed:
            random.seed(seed)

    def __create_cells(self):
        for i in range(self.__num_cols):
            col = []
            for j in range(self.__num_rows):
                col.append(Cell(self.__win))
            self._cells.append(col)

        if self.__win is None:
            return

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
        self._cells[i][j].draw(x1, y1, x2, y2)

        self.__animate()
        print(f"Drawn cell ({i}, {j})")

    def __animate(self):
        if self.__win is None:
            return
        self.__win.redraw()
        time.sleep(0.05)

    def __break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self.__draw_cell(0, 0)
        self._cells[self.__num_cols - 1][self.__num_rows - 1].has_bottom_wall = False
        self.__draw_cell(self.__num_cols - 1, self.__num_rows - 1)

    def __break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            next_index_list = []

            if i > 0 and not self._cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))

            if i < self.__num_cols - 1 and not self._cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))

            if j > 0 and not self._cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))

            if j < self.__num_rows - 1 and not self._cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))

            if len(next_index_list) == 0:
                self.__draw_cell(i, j)
                return

            direction_index = random.randrange(len(next_index_list))
            next_index = next_index_list[direction_index]

            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False

            if next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False

            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False

            if next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False

            self.__break_walls_r(next_index[0], next_index[1])

    def __reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        return self.__solve_r(0, 0)

    def __solve_r(self, i, j):
        self.__animate()
        self._cells[i][j].visited = True

        if i == self.__num_cols - 1 and j == self.__num_rows - 1:
            return True

        if (
            i > 0
            and not self._cells[i - 1][j].visited
            and not self._cells[i][j].has_left_wall
        ):
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self.__solve_r(i - 1, j):
                return True
            self._cells[i][j].draw_move(self._cells[i - 1][j], undo=True)

        if (
            i < self.__num_cols - 1
            and not self._cells[i + 1][j].visited
            and not self._cells[i][j].has_right_wall
        ):
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self.__solve_r(i + 1, j):
                return True
            self._cells[i][j].draw_move(self._cells[i + 1][j], undo=True)

        if (
            j > 0
            and not self._cells[i][j - 1].visited
            and not self._cells[i][j].has_top_wall
        ):
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self.__solve_r(i, j - 1):
                return True
            self._cells[i][j].draw_move(self._cells[i][j - 1], undo=True)

        if (
            j < self.__num_rows - 1
            and not self._cells[i][j + 1].visited
            and not self._cells[i][j].has_bottom_wall
        ):
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self.__solve_r(i, j + 1):
                return True
            self._cells[i][j].draw_move(self._cells[i][j + 1], undo=True)

        return False
