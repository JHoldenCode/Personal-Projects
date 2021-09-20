import random


class Grid:
    def __init__(self):
        boxes = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        added = 0
        while added < 2:
            a = int(random.random() * 4)
            b = int(random.random() * 4)
            if boxes[a][b] == 0:
                added += 1
                chance = random.random()
                if chance <= .1:
                    boxes[a][b] = 4
                else:
                    boxes[a][b] = 2
        self.boxes = boxes

    def print_grid(self):
        for x in range(4):
            row = ""
            for y in range(4):
                if self.boxes[x][y] != 0:
                    row += str(self.boxes[x][y])
                else:
                    row += "."
                row += "   "
            print(row)

    def add_number(self):
        open_boxes = 0
        for x in range(4):
            for y in range(4):
                if self.boxes[x][y] == 0:
                    open_boxes += 1
        box_to_be_added = int(random.random() * open_boxes)
        open_boxes = 0
        for x in range(4):
            for y in range(4):
                if open_boxes == box_to_be_added and self.boxes[x][y] == 0:
                    chance = random.random()
                    if chance <= .1:
                        self.boxes[x][y] = 4
                    else:
                        self.boxes[x][y] = 2
                    open_boxes += 1
                if self.boxes[x][y] == 0:
                    open_boxes += 1

    def sum_up(self):
        change = 0
        x = 0
        x2 = 1
        for y in range(4):
            while x < 4 and x2 < 4:
                while x < 4 and self.boxes[x][y] == 0:
                    x += 1
                    x2 = x + 1
                while x2 < 4 and self.boxes[x2][y] == 0:
                    x2 += 1
                if x < 4 and x2 < 4 and self.boxes[x][y] == self.boxes[x2][y]:
                    self.boxes[x2][y] = self.boxes[x][y] + self.boxes[x2][y]
                    change += self.boxes[x2][y]
                    self.boxes[x][y] = 0
                    x = x2 + 1
                    x2 = x + 1
                else:
                    x = x2
                    x2 += 1
            x = 0
            x2 = 1
        return change

    def sum_left(self):
        change = 0
        y = 0
        y2 = 1
        for x in range(4):
            while y < 4 and y2 < 4:
                while y < 4 and self.boxes[x][y] == 0:
                    y += 1
                    y2 = y + 1
                while y2 < 4 and self.boxes[x][y2] == 0:
                    y2 += 1
                if y < 4 and y2 < 4 and self.boxes[x][y] == self.boxes[x][y2]:
                    self.boxes[x][y2] = self.boxes[x][y] + self.boxes[x][y2]
                    change += self.boxes[x][y2]
                    self.boxes[x][y] = 0
                    y = y2 + 1
                    y2 = y + 1
                else:
                    y = y2
                    y2 += 1
            y = 0
            y2 = 1
        return change

    def sum_down(self):
        change = 0
        x = 3
        x2 = 2
        for y in range(4):
            while x >= 0 and x2 >= 0:
                while x >= 0 and self.boxes[x][y] == 0:
                    x -= 1
                    x2 = x - 1
                while x2 >= 0 and self.boxes[x2][y] == 0:
                    x2 -= 1
                if x >= 0 and x2 >= 0 and self.boxes[x][y] == self.boxes[x2][y]:
                    self.boxes[x2][y] = self.boxes[x][y] + self.boxes[x2][y]
                    change += self.boxes[x2][y]
                    self.boxes[x][y] = 0
                    x = x2 - 1
                    x2 = x - 1
                else:
                    x = x2
                    x2 -= 1
            x = 3
            x2 = 2
        return change

    def sum_right(self):
        change = 0
        y = 3
        y2 = 2
        for x in range(4):
            while y >= 0 and y2 >= 0:
                while y >= 0 and self.boxes[x][y] == 0:
                    y -= 1
                    y2 = y - 1
                while y2 >= 0 and self.boxes[x][y2] == 0:
                    y2 -= 1
                if y >= 0 and y2 >= 0 and self.boxes[x][y] == self.boxes[x][y2]:
                    self.boxes[x][y2] = self.boxes[x][y] + self.boxes[x][y2]
                    change += self.boxes[x][y2]
                    self.boxes[x][y] = 0
                    y = y2 - 1
                    y2 = y - 1
                else:
                    y = y2
                    y2 -= 1
            y = 3
            y2 = 2
        return change

    def move_up(self):
        something_moved = False
        for y in range(4):
            x = 0
            new_col = [0, 0, 0, 0]
            size = 0
            while x < 4:
                if self.boxes[x][y] != 0:
                    new_col[size] = self.boxes[x][y]
                    size += 1
                x += 1
            for x in range(4):
                if self.boxes[x][y] != new_col[x]:
                    something_moved = True
                self.boxes[x][y] = new_col[x]
        if something_moved:
            self.add_number()

    def move_left(self):
        something_moved = False
        for x in range(4):
            y = 0
            new_col = [0, 0, 0, 0]
            size = 0
            while y < 4:
                if self.boxes[x][y] != 0:
                    new_col[size] = self.boxes[x][y]
                    size += 1
                y += 1
            for y in range(4):
                if self.boxes[x][y] != new_col[y]:
                    something_moved = True
                self.boxes[x][y] = new_col[y]
        if something_moved:
            self.add_number()

    def move_down(self):
        something_moved = False
        for y in range(4):
            x = 3
            new_col = [0, 0, 0, 0]
            size = 3
            while x >= 0:
                if self.boxes[x][y] != 0:
                    new_col[size] = self.boxes[x][y]
                    size -= 1
                x -= 1
            for x in range(4):
                if self.boxes[3 - x][y] != new_col[3 - x]:
                    something_moved = True
                self.boxes[3 - x][y] = new_col[3 - x]
        if something_moved:
            self.add_number()

    def move_right(self):
        something_moved = False
        for x in range(4):
            y = 3
            new_col = [0, 0, 0, 0]
            size = 3
            while y >= 0:
                if self.boxes[x][y] != 0:
                    new_col[size] = self.boxes[x][y]
                    size -= 1
                y -= 1
            for y in range(4):
                if self.boxes[x][3 - y] != new_col[3 - y]:
                    something_moved = True
                self.boxes[x][3 - y] = new_col[3 - y]
        if something_moved:
            self.add_number()

    def up_press(self):
        change = self.sum_up()
        self.move_up()
        return change

    def left_press(self):
        change = self.sum_left()
        self.move_left()
        return change

    def down_press(self):
        change = self.sum_down()
        self.move_down()
        return change

    def right_press(self):
        change = self.sum_right()
        self.move_right()
        return change

    def grid_is_full(self):
        for x in range(4):
            for y in range(4):
                if self.boxes[x][y] == 0:
                    return False
        return True

    def grid_is_summable(self):
        for x in range(4):
            for y in range(3):
                if self.boxes[x][y] == self.boxes[x][y + 1]:
                    return True
        for y in range(4):
            for x in range(3):
                if self.boxes[x][y] == self.boxes[x + 1][y]:
                    return True
        return False

    def game_over(self):
        if not self.grid_is_full() or self.grid_is_summable():
            return False
        return True




