from tkinter import *
from tkinter.messagebox import *
import random
from PIL import Image, ImageTk
import os
# ---------------------------------------------random start
def random_board_create():
    global all_ship_coord
    all_ship_coord = []
    all_dead_ship_coord = []
    temp_lis = []  # for every single list in 2D matrix
    coord_list = []  # 2D matrix
    for i in range(10):
        for j in range(10):
            temp_lis.append((i, j))  # creating every single list and appending to 2D coor_list

        coord_list.append(temp_lis)
        temp_lis = []

    def ship(ship_size):
        ship_coord = []
        k = 0
        # n == 1 all possible ways to put boat on board
        if (ship_size == 1):
            for i in range(10):
                for j in range(10):
                    ship_coord.append([(i, j)])
                    k += 1
        # n == 2  all possible ways to put boat on board
        elif (ship_size == 2):
            for i in range(10):
                for j in range(10):
                    if (j + 1 < 5):
                        ship_coord.append([(i, j), (i, j + 1)])
                        k += 1
                    if (i + 1 < 5):
                        ship_coord.append([(i, j), (i + 1, j)])
                        k += 1
        # n == 3 all possible ways to put boat on board
        elif (ship_size == 3):
            for i in range(10):
                for j in range(10):
                    if (j + 2 < 5):
                        ship_coord.append([(i, j), (i, j + 1), (i, j + 2)])
                        k += 1
                    if (i + 2 < 5):
                        ship_coord.append([(i, j), (i + 1, j), (i + 2, j)])
                        k += 1
        # n == 4 all possible ways to put boat on board
        elif (ship_size == 4):
            for i in range(10):
                for j in range(10):
                    if (j + 3 < 5):
                        ship_coord.append([(i, j), (i, j + 1), (i, j + 2), (i, j + 3)])
                        k += 1
                    if (i + 3 < 5):
                        ship_coord.append([(i, j), (i + 1, j), (i + 2, j), (i + 3, j)])
                        k += 1
        return ship_coord

    def rand_boat(ship_coords):
        ran_numb_boat = random.randint(0, len(ship_coords) - 1)
        return ran_numb_boat

    def shape(ship_coord_unique):
        def shape_cord(tup):
            lis1 = []
            x = tup[0]
            y = tup[1]
            for i in range(-1, 2):
                for j in range(-1, 2):
                    lis1.append((x + i, y + j))
            return lis1

        dead_shape_list = []
        for i in range(len(ship_coord_unique)):
            dead_shape_list.extend(shape_cord(ship_coord_unique[i]))

        return list(set(dead_shape_list))

    def combined_coord(all_dead_ship_coord, all_ship_coord, x):
        rand_number = rand_boat(ship_coords)
        q = 0
        for i in range(len(ship_coords[rand_number])):
            if ship_coords[rand_number][i] not in all_dead_ship_coord:
                q += 1
            if q == len(ship_coords[rand_number]):
                all_ship_coord.append(ship_coords[rand_number])
                all_dead_ship_coord.extend(shape(ship_coords[rand_number]))
                x += 1

        return [list(set(all_dead_ship_coord)), all_ship_coord, x]

    for i in range(4, 0, -1):
        ship_coords = ship(i)
        counter = 0
        x = 0
        while x < (5 - i):
            all_dead_ship_coord, all_ship_coord, x = combined_coord(all_dead_ship_coord, all_ship_coord, x)
            counter += 1

    temp_lis1 = []
    ship_cord_1d = []
    for i in range(len(all_ship_coord)):
        for j in range(len(all_ship_coord[i])):
            ship_cord_1d.append(all_ship_coord[i][j])

    coord_list1 = []
    for i in range(10):
        for j in range(10):
            if (i, j) in ship_cord_1d:
                temp_lis1.append("X")
            else:
                temp_lis1.append("O")  # creating every single list and appending to 2D coor_list
        coord_list1.append(temp_lis1)
        temp_lis1 = []
    return coord_list1, all_ship_coord
# ---------------------------------------------------------------random end

# ---------------------------------------------------------------computer hit start

shape_of_x = []
shape_of_x_values = []

def fire(player_board, shape_of_x, shape_of_x_values, all_ship_coord, count):
    def rand_coord(n):
        ran_numb_boat = random.randint(0, n - 1)
        return ran_numb_boat

    def rand_fire_shape_of_x(player_board, shape_of_x, shape_of_x_values, count):
        x0, y0 = shape_of_x[-1]
        bol = True
        while bol:
            remove_shape_of_x = []
            n = len(shape_of_x)
            if len(shape_of_x) > 2:
                q = random.randint(0, n - 2)
            else:
                q = 0
            x, y = shape_of_x[q]
            shape_of_x.pop(q)
            if player_board[x][y] == "O":
                player_board[x][y] = "-"
                bol = False

            elif player_board[x][y] == "X":
                bol = False
                count += 1
                shape_of_x_values.remove("X")
                player_board[x][y] = "+"
                if x == x0:
                    if abs(y0 - y) == 1:
                        Y = 2 * y - y0
                        if Y != -1 and Y != 10:
                            shape_of_x.insert(0, (x, Y))
                            if player_board[x][Y] == "X":
                                shape_of_x_values.append("X")
                    elif abs(y0 - y) == 2:
                        Y = (3 * y - y0) // 2
                        if Y != -1 and Y != 10:
                            shape_of_x.insert(0, (x, Y))
                            if player_board[x][Y] == "X":
                                shape_of_x_values.append("X")

                    for i in range(len(shape_of_x)):
                        if shape_of_x[i][0] != x:
                            remove_shape_of_x.append(shape_of_x[i])
                elif y == y0:
                    if abs(x0 - x) == 1:
                        X = 2 * x - x0
                        if X != -1 and X != 10:
                            shape_of_x.insert(0, (X, y))
                            if player_board[X][y] == "X":
                                shape_of_x_values.append("X")
                    elif abs(x0 - x) == 2:
                        X = (3 * x - x0) // 2
                        if X != -1 and X != 10:
                            shape_of_x.insert(0, (X, y))
                            if player_board[X][y] == "X":
                                shape_of_x_values.append("X")

                    for i in range(len(shape_of_x)):
                        if shape_of_x[i][1] != y:
                            remove_shape_of_x.append(shape_of_x[i])
                for i in range(len(remove_shape_of_x)):
                    shape_of_x.remove(remove_shape_of_x[i])
        return shape_of_x, count

    def rand_fire(player_board, shape_of_x, shape_of_x_values, count):
        bol = True
        while bol:
            x = rand_coord(len(player_board))
            y = rand_coord(len(player_board))
            if player_board[x][y] == "O":
                player_board[x][y] = "-"
                bol = False
            elif player_board[x][y] == "X":
                count += 1
                player_board[x][y] = "+"
                bol = False
                if (x - 1) != -1 and player_board[x - 1][y] != "-" and player_board[x - 1][y] != "+":
                    shape_of_x_values.append(player_board[x - 1][y])
                    shape_of_x.append((x - 1, y))
                if (x + 1) != 10 and player_board[x + 1][y] != "-" and player_board[x + 1][y] != "+":
                    shape_of_x_values.append(player_board[x + 1][y])
                    shape_of_x.append((x + 1, y))
                if (y + 1) != 10 and player_board[x][y + 1] != "-" and player_board[x][y + 1] != "+":
                    shape_of_x_values.append(player_board[x][y + 1])
                    shape_of_x.append((x, y + 1))
                if (y - 1) != -1 and player_board[x][y - 1] != "-" and player_board[x][y - 1] != "+":
                    shape_of_x_values.append(player_board[x][y - 1])
                    shape_of_x.append((x, y - 1))
                    shape_of_x.append((x, y))

        return shape_of_x_values, shape_of_x, count

    def dead_ship_shape(ship_coord_unique, player_board):
        dead_shape_list = []

        for i in range(len(ship_coord_unique)):
            dead_shape_list.extend(dead_ship_shape_cord(ship_coord_unique[i]))
        dead_shape_list = list(set(dead_shape_list))
        for i in range(len(ship_coord_unique)):
            dead_shape_list.remove(ship_coord_unique[i])
        for i in range(len(dead_shape_list)):
            x, y = dead_shape_list[i]
            player_board[x][y] = "-"

    if "X" not in shape_of_x_values:

        shape_of_x_values, shape_of_x, count = rand_fire(player_board, shape_of_x, shape_of_x_values, count)

    else:
        shape_of_x, count = rand_fire_shape_of_x(player_board, shape_of_x, shape_of_x_values, count)

    def playerboard_filter(player_bord, all_ship_coord):
        lis = [["+", "+", "+", "+"], ["+", "+", "+"], ["+", "+"], ["+"]]
        all_ship_coord_plus = []
        for i in range(len(all_ship_coord)):
            for j in range(len(all_ship_coord[i])):
                x, y = all_ship_coord[i][j]
                all_ship_coord_plus.append(player_board[x][y])
            if all_ship_coord_plus in lis:
                dead_ship_shape(all_ship_coord[i], player_board)

            all_ship_coord_plus = []

    def dead_ship_shape_cord(tup):
        lis1 = []
        x = tup[0]
        y = tup[1]
        if x == 0:
            for i in range(0, 2):
                if y == 0:
                    for j in range(0, 2):
                        lis1.append((x + i, y + j))
                elif y == 9:
                    for j in range(-1, 1):
                        lis1.append((x + i, y + j))
                else:
                    for j in range(-1, 2):
                        lis1.append((x + i, y + j))
        elif x == 9:
            for i in range(-1, 1):
                if y == 0:
                    for j in range(0, 2):
                        lis1.append((x + i, y + j))
                elif y == 9:
                    for j in range(-1, 1):
                        lis1.append((x + i, y + j))
                else:
                    for j in range(-1, 2):
                        lis1.append((x + i, y + j))
        else:
            for i in range(-1, 2):
                if y == 0:
                    for j in range(0, 2):
                        lis1.append((x + i, y + j))
                elif y == 9:
                    for j in range(-1, 1):
                        lis1.append((x + i, y + j))
                else:
                    for j in range(-1, 2):
                        lis1.append((x + i, y + j))
        return lis1

    playerboard_filter(player_board, all_ship_coord)

    def player_win(player_board, all_ship_coord, count):
        a = 0
        for i in range(len(all_ship_coord)):
            for j in range(len(all_ship_coord[i])):
                x, y = all_ship_coord[i][j]
                if player_board[x][y] == "X":
                    a += 1
        if a == 0:
            count = 0
            #print("You ara a winner!!!!!!")
        return count

    count = player_win(player_board, all_ship_coord, count)

    if count > 1:
        player_board = fire(player_board, shape_of_x, shape_of_x_values, all_ship_coord, count - 1)
    print("\n")
    return player_board


# ---------------------------------------------------------------computer hit end
class Game(Frame):
    # display width
    width = 800
    # display height
    height = 500
    # canvas color
    bg = "white"
    # indent between cells
    indent = 2
    # cells size
    gauge = 32
    # y offset(indent from top)(for player board)
    offset_y = 40
    # x offset(for player)
    offset_x_user = 30
    # x offset(for second player/computer)
    offset_x_comp = 430
    # computer random list for testing, after merging the programs,it will become empty
    random_list_comp = []
    # Random list for player
    player_board = []
    count_player = 0
    # count_comp=0
    # all_ship_coord=[]
    # cheking edit
    k = 0
    stug = 0
    # cheking button
    press = 0
    #for button press
    corX = indent + offset_x_user
    corY = indent + offset_y

    # Adding canvas
    def createCanvas(self):
        self.k = 0
        self.canv = Canvas(self)
        self.canv["height"] = self.height
        self.canv["width"] = self.width
        self.canv["bg"] = self.bg
        self.canv.pack()
        self.img = ImageTk.PhotoImage(Image.open(os.path.dirname(__file__)+"\\img\\Battleship.png"))
        self.canv.create_image(0, 0, anchor=NW, image=self.img)
        self.canv.image = self.img

    def new_game(self):
        self.canv.delete('all')
        self.k = 1
        self.stug = 0
        self.img2 = ImageTk.PhotoImage(Image.open(os.path.dirname(__file__)+"\\img\\board_background.jpg"))
        self.canv.create_image(0, 0, anchor=NW, image=self.img2)
        self.canv.image = self.img2
        # board for player
        for i in range(10):
            for j in range(10):
                xn = j * self.gauge + (j + 1) * self.indent + self.offset_x_user
                xk = xn + self.gauge
                yn = i * self.gauge + (i + 1) * self.indent + self.offset_y
                yk = yn + self.gauge
                # creating one rectangle for player board
                self.canv.create_rectangle(xn, yn, xk, yk,fill="lightskyblue")

        # board for second player/computer
        for i in range(10):
            for j in range(10):
                xn = j * self.gauge + (j + 1) * self.indent + self.offset_x_comp
                xk = xn + self.gauge
                yn = i * self.gauge + (i + 1) * self.indent + self.offset_y
                yk = yn + self.gauge
                # creating one rectangle for computer/second player board
                self.canv.create_rectangle(xn, yn, xk, yk, fill="CornflowerBlue")

        # board number
        for i in reversed(range(10)):
            # player board numbers
            xc = self.offset_x_user - 15
            yc = i * self.gauge + (i + 1) * self.indent + self.offset_y + round(self.gauge / 2)
            self.canv.create_text(xc, yc, text=str(i + 1),font=(15))
            # second player/computer board numbers
            xc = self.offset_x_comp - 15
            yc = i * self.gauge + (i + 1) * self.indent + self.offset_y + round(self.gauge / 2)
            self.canv.create_text(xc, yc, text=str(i + 1),font=(15))
        # Letters
        symbols = "АBCDEFGHIJ"
        for i in range(10):
            # буквы пользователя
            xc = i * self.gauge + (i + 1) * self.indent + self.offset_x_user + round(self.gauge / 2)
            yc = self.offset_y - 15
            self.canv.create_text(xc, yc, text=symbols[i],font=(15))

            # Letters for second player/computer board
            xc = i * self.gauge + (i + 1) * self.indent + self.offset_x_comp + round(self.gauge / 2)
            yc = self.offset_y - 15
            self.canv.create_text(xc, yc, text=symbols[i], font=(15))
        #Start button
        btn2 = Button(self.canv, text="START", width=15, height=3, bg="#00FF00", command=self.start)
        btn2.place(x=self.offset_x_user + 300, y=self.offset_y + 380, anchor=NW)

    # Functions below we need to take matrix with random ships
    # for first player. this list we will creat/take onece
    def get_random_list_player(self):
        if self.k == 1:
            self.stug = 1
            for i in range(10):
                for j in range(10):
                    xn = j * self.gauge + (j + 1) * self.indent + self.offset_x_user
                    xk = xn + self.gauge
                    yn = i * self.gauge + (i + 1) * self.indent + self.offset_y
                    yk = yn + self.gauge
                    # creating one rectangle for player board
                    self.canv.create_rectangle(xn, yn, xk, yk, fill="lightskyblue")
            # for testing
            self.player_board, self.all_ship_coord_player = random_board_create()
            self.playerShip_painting()
        else:
            showwarning("Battleship", "Please start game")

    # for computer/second player.this list we must update after every turn in another function
    def get_random_list_comp(self):
        for i in range(10):
            for j in range(10):
                xn = j * self.gauge + (j + 1) * self.indent + self.offset_x_comp
                xk = xn + self.gauge
                yn = i * self.gauge + (i + 1) * self.indent + self.offset_y
                yk = yn + self.gauge
                # creating one rectangle for computer/second player board
                self.canv.create_rectangle(xn, yn, xk, yk, fill="CornflowerBlue")
        self.random_list_comp, self.all_ship_coord_comp = random_board_create()

    # painting ships
    def playerShip_painting(self):
        for i in range(10):
            for j in range(10):
                # find out rectangle cordiants and size
                xn = j * self.gauge + (j + 1) * self.indent + self.offset_x_user
                yn = i * self.gauge + (i + 1) * self.indent + self.offset_y
                xk = xn + self.gauge
                yk = yn + self.gauge
                if self.player_board[i][j] == "X":
                    self.canv.create_rectangle(xn, yn, xk, yk, fill="dimgray")

    # painting all miss oval on computer board
    def paint_miss_all(self):
        self.playerboard_filter()
        for i in range(10):
            for j in range(10):
                # find out rectangle cordiants and size
                xn = j * self.gauge + (j + 1) * self.indent + self.offset_x_comp
                yn = i * self.gauge + (i + 1) * self.indent + self.offset_y
                xk = xn + self.gauge
                yk = yn + self.gauge
                if self.random_list_comp[i][j] == '-':
                    self.canv.create_rectangle(xn, yn, xk, yk, fill="lightskyblue")
                    self.canv.create_oval(xn + 13, yn + 13, xn + 18, yn + 18, fill="gray", width="1")
        self.player_win()

    # painting one miss oval on computer board
    def paint_miss(self, xn, yn, xk, yk):
        self.canv.create_rectangle(xn, yn, xk, yk, fill="lightskyblue")
        self.canv.create_oval(xn + 13, yn + 13, xn + 18, yn + 18, fill="gray", width="1")
        self.comp_turn()

    # painting hit cross and paint background red on computer board
    def paint_hit(self, xn, yn, xk, yk, i, j):

        tf1 = True
        if j + 1 != 10:
            if self.random_list_comp[i][j + 1] == 'X':
                tf1 = False
        if i + 1 != 10:
            if self.random_list_comp[i + 1][j] == 'X':
                tf1 = False

        if j - 1 != -1:
            if self.random_list_comp[i][j - 1] == 'X':
                tf1 = False
        if i - 1 != -1:
            if self.random_list_comp[i - 1][j] == 'X':
                tf1 = False

        if j + 1 != 10:
            if self.random_list_comp[i][j + 1] == '+':
                if j + 2 != 10:
                    if self.random_list_comp[i][j + 2] == '+':
                        if j + 3 != 10:
                            if self.random_list_comp[i][j + 3] == '+':
                                tf1 = True
                            elif self.random_list_comp[i][j + 3] == 'X':
                                tf1 = False
                    elif self.random_list_comp[i][j + 2] == 'X':
                        tf1 = False
        if i + 1 != 10:
            if self.random_list_comp[i + 1][j] == '+':
                if j + 2 != 10:
                    if self.random_list_comp[i + 2][j] == '+':
                        if j + 3 != 10:
                            if self.random_list_comp[i + 3][j] == '+':
                                tf1 = True
                            elif self.random_list_comp[i + 3][j] == 'X':
                                tf1 = False
                    elif self.random_list_comp[i + 2][j] == 'X':
                        tf1 = False
        if j - 1 != -1:
            if self.random_list_comp[i][j - 1] == '+':
                if j - 2 != -1:
                    if self.random_list_comp[i][j - 2] == '+':
                        if j - 3 != -1:
                            if self.random_list_comp[i][j - 3] == '+':
                                tf1 = True
                            elif self.random_list_comp[i][j - 3] == 'X':
                                tf1 = False
                    elif self.random_list_comp[i][j - 2] == 'X':
                        tf1 = False
        if i - 1 != -1:
            if self.random_list_comp[i - 1][j] == '+':
                if j - 2 != -1:
                    if self.random_list_comp[i - 2][j] == '+':
                        if j - 3 != -1:
                            if self.random_list_comp[i - 3][j] == '+':
                                tf1 = True
                            elif self.random_list_comp[i - 3][j] == 'X':
                                tf1 = False
                    elif self.random_list_comp[i - 2][j] == 'X':
                        tf1 = False

        if tf1:
            xn = j * self.gauge + (j + 1) * self.indent + self.offset_x_comp
            yn = i * self.gauge + (i + 1) * self.indent + self.offset_y
            xk = xn + self.gauge
            yk = yn + self.gauge
            self.canv.create_rectangle(xn, yn, xk, yk, fill="#DC143C")
            self.canv.create_line(xn + 2, yn + 2, xk - 2, yk - 2, fill="Black", width="2")
            self.canv.create_line(xk - 2, yn + 2, xn + 2, yk - 2, fill="Black", width="2")
            if j + 1 != 10:
                if self.random_list_comp[i][j + 1] == '+':
                    xn = (j + 1) * self.gauge + (j + 2) * self.indent + self.offset_x_comp
                    yn = i * self.gauge + (i + 1) * self.indent + self.offset_y
                    xk = xn + self.gauge
                    yk = yn + self.gauge
                    self.canv.create_rectangle(xn, yn, xk, yk, fill="#DC143C")
                    self.canv.create_line(xn + 2, yn + 2, xk - 2, yk - 2, fill="Black", width="2")
                    self.canv.create_line(xk - 2, yn + 2, xn + 2, yk - 2, fill="Black", width="2")
                    if j + 2 != 10:
                        if self.random_list_comp[i][j + 2] == '+':
                            xn = (j + 2) * self.gauge + (j + 3) * self.indent + self.offset_x_comp
                            yn = i * self.gauge + (i + 1) * self.indent + self.offset_y
                            xk = xn + self.gauge
                            yk = yn + self.gauge
                            self.canv.create_rectangle(xn, yn, xk, yk, fill="#DC143C")
                            self.canv.create_line(xn + 2, yn + 2, xk - 2, yk - 2, fill="Black", width="2")
                            self.canv.create_line(xk - 2, yn + 2, xn + 2, yk - 2, fill="Black", width="2")

                            if j + 3 != 10:
                                if self.random_list_comp[i][j + 3] == '+':
                                    xn = (j + 3) * self.gauge + (j + 4) * self.indent + self.offset_x_comp
                                    yn = i * self.gauge + (i + 1) * self.indent + self.offset_y
                                    xk = xn + self.gauge
                                    yk = yn + self.gauge
                                    self.canv.create_rectangle(xn, yn, xk, yk, fill="#DC143C")
                                    self.canv.create_line(xn + 2, yn + 2, xk - 2, yk - 2, fill="Black", width="2")
                                    self.canv.create_line(xk - 2, yn + 2, xn + 2, yk - 2, fill="Black", width="2")
            if i + 1 != 10:
                if self.random_list_comp[i + 1][j] == '+':
                    xn = j * self.gauge + (j + 1) * self.indent + self.offset_x_comp
                    yn = (i + 1) * self.gauge + (i + 2) * self.indent + self.offset_y
                    xk = xn + self.gauge
                    yk = yn + self.gauge
                    self.canv.create_rectangle(xn, yn, xk, yk, fill="#DC143C")
                    self.canv.create_line(xn + 2, yn + 2, xk - 2, yk - 2, fill="Black", width="2")
                    self.canv.create_line(xk - 2, yn + 2, xn + 2, yk - 2, fill="Black", width="2")
                    if i + 2 != 10:
                        if self.random_list_comp[i + 2][j] == '+':
                            xn = j * self.gauge + (j + 1) * self.indent + self.offset_x_comp
                            yn = (i + 2) * self.gauge + (i + 3) * self.indent + self.offset_y
                            xk = xn + self.gauge
                            yk = yn + self.gauge
                            self.canv.create_rectangle(xn, yn, xk, yk, fill="#DC143C")
                            self.canv.create_line(xn + 2, yn + 2, xk - 2, yk - 2, fill="Black", width="2")
                            self.canv.create_line(xk - 2, yn + 2, xn + 2, yk - 2, fill="Black", width="2")
                            if i + 3 != 10:
                                if self.random_list_comp[i + 3][j] == '+':
                                    xn = j * self.gauge + (j + 1) * self.indent + self.offset_x_comp
                                    yn = (i + 3) * self.gauge + (i + 4) * self.indent + self.offset_y
                                    xk = xn + self.gauge
                                    yk = yn + self.gauge
                                    self.canv.create_rectangle(xn, yn, xk, yk, fill="#DC143C")
                                    self.canv.create_line(xn + 2, yn + 2, xk - 2, yk - 2, fill="Black", width="2")
                                    self.canv.create_line(xk - 2, yn + 2, xn + 2, yk - 2, fill="Black", width="2")
            if j - 1 != -1:
                if self.random_list_comp[i][j - 1] == '+':
                    xn = (j - 1) * self.gauge + j * self.indent + self.offset_x_comp
                    yn = i * self.gauge + (i + 1) * self.indent + self.offset_y
                    xk = xn + self.gauge
                    yk = yn + self.gauge
                    self.canv.create_rectangle(xn, yn, xk, yk, fill="#DC143C")
                    self.canv.create_line(xn + 2, yn + 2, xk - 2, yk - 2, fill="Black", width="2")
                    self.canv.create_line(xk - 2, yn + 2, xn + 2, yk - 2, fill="Black", width="2")
                    if j - 2 != -1:
                        if self.random_list_comp[i][j - 2] == '+':
                            xn = (j - 2) * self.gauge + (j - 1) * self.indent + self.offset_x_comp
                            yn = i * self.gauge + (i + 1) * self.indent + self.offset_y
                            xk = xn + self.gauge
                            yk = yn + self.gauge
                            self.canv.create_rectangle(xn, yn, xk, yk, fill="#DC143C")
                            self.canv.create_line(xn + 2, yn + 2, xk - 2, yk - 2, fill="Black", width="2")
                            self.canv.create_line(xk - 2, yn + 2, xn + 2, yk - 2, fill="Black", width="2")
                            if j - 3 != -1:
                                if self.random_list_comp[i][j - 3] == '+':
                                    xn = (j - 3) * self.gauge + (j - 2) * self.indent + self.offset_x_comp
                                    yn = i * self.gauge + (i + 1) * self.indent + self.offset_y
                                    xk = xn + self.gauge
                                    yk = yn + self.gauge
                                    self.canv.create_rectangle(xn, yn, xk, yk, fill="#DC143C")
                                    self.canv.create_line(xn + 2, yn + 2, xk - 2, yk - 2, fill="Black", width="2")
                                    self.canv.create_line(xk - 2, yn + 2, xn + 2, yk - 2, fill="Black", width="2")
            if i - 1 != -1:
                if self.random_list_comp[i - 1][j] == '+':
                    xn = j * self.gauge + (j + 1) * self.indent + self.offset_x_comp
                    yn = (i - 1) * self.gauge + i * self.indent + self.offset_y
                    xk = xn + self.gauge
                    yk = yn + self.gauge
                    self.canv.create_rectangle(xn, yn, xk, yk, fill="#DC143C")
                    self.canv.create_line(xn + 2, yn + 2, xk - 2, yk - 2, fill="Black", width="2")
                    self.canv.create_line(xk - 2, yn + 2, xn + 2, yk - 2, fill="Black", width="2")
                    if i - 2 != -1:
                        if self.random_list_comp[i - 2][j] == '+':
                            xn = j * self.gauge + (j + 1) * self.indent + self.offset_x_comp
                            yn = (i - 2) * self.gauge + (i - 1) * self.indent + self.offset_y
                            xk = xn + self.gauge
                            yk = yn + self.gauge
                            self.canv.create_rectangle(xn, yn, xk, yk, fill="#DC143C")
                            self.canv.create_line(xn + 2, yn + 2, xk - 2, yk - 2, fill="Black", width="2")
                            self.canv.create_line(xk - 2, yn + 2, xn + 2, yk - 2, fill="Black", width="2")
                            if i - 3 != -1:
                                if self.random_list_comp[i - 3][j] == '+':
                                    xn = j * self.gauge + (j + 1) * self.indent + self.offset_x_comp
                                    yn = (i - 3) * self.gauge + (i - 2) * self.indent + self.offset_y
                                    xk = xn + self.gauge
                                    yk = yn + self.gauge
                                    self.canv.create_rectangle(xn, yn, xk, yk, fill="#DC143C")
                                    self.canv.create_line(xn + 2, yn + 2, xk - 2, yk - 2, fill="Black", width="2")
                                    self.canv.create_line(xk - 2, yn + 2, xn + 2, yk - 2, fill="Black", width="2")
            self.paint_miss_all()

        elif tf1 == False:
            self.canv.create_rectangle(xn, yn, xk, yk, fill="lightskyblue")
            self.canv.create_line(xn + 2, yn + 2, xk - 2, yk - 2, width="2")
            self.canv.create_line(xk - 2, yn + 2, xn + 2, yk - 2, width="2")
            self.player_win()

    # ------------------------------------------------range_ship
    def dead_ship_shape(self, ship_coord_unique):
        dead_shape_list = []

        for i in range(len(ship_coord_unique)):
            dead_shape_list.extend(self.dead_ship_shape_cord(ship_coord_unique[i]))
            dead_shape_list = list(set(dead_shape_list))
        for i in range(len(ship_coord_unique)):
            dead_shape_list.remove(ship_coord_unique[i])
        for i in range(len(dead_shape_list)):
            x, y = dead_shape_list[i]
            self.random_list_comp[x][y] = "-"

    def dead_ship_shape_cord(self, tup):
        lis1 = []
        x = tup[0]
        y = tup[1]
        if x == 0:
            for i in range(0, 2):
                if y == 0:
                    for j in range(0, 2):
                        lis1.append((x + i, y + j))
                elif y == 9:
                    for j in range(-1, 1):
                        lis1.append((x + i, y + j))
                else:
                    for j in range(-1, 2):
                        lis1.append((x + i, y + j))
        elif x == 9:
            for i in range(-1, 1):
                if y == 0:
                    for j in range(0, 2):
                        lis1.append((x + i, y + j))
                elif y == 9:
                    for j in range(-1, 1):
                        lis1.append((x + i, y + j))
                else:
                    for j in range(-1, 2):
                        lis1.append((x + i, y + j))
        else:
            for i in range(-1, 2):
                if y == 0:
                    for j in range(0, 2):
                        lis1.append((x + i, y + j))
                elif y == 9:
                    for j in range(-1, 1):
                        lis1.append((x + i, y + j))
                else:
                    for j in range(-1, 2):
                        lis1.append((x + i, y + j))
        return lis1

    def playerboard_filter(self):
        lis = [["+", "+", "+", "+"], ["+", "+", "+"], ["+", "+"], ["+"]]
        all_ship_coord_plus = []
        for i in range(len(self.all_ship_coord_comp)):
            for j in range(len(self.all_ship_coord_comp[i])):
                x, y = self.all_ship_coord_comp[i][j]
                all_ship_coord_plus.append(self.random_list_comp[x][y])
            if all_ship_coord_plus in lis:
                self.dead_ship_shape(self.all_ship_coord_comp[i])

            all_ship_coord_plus = []

    # painting miss oval on player board
    def paint_comp_miss(self, xn, yn, xk, yk):
        self.canv.create_oval(xn + 13, yn + 13, xn + 18, yn + 18, fill="Black", width="1")

    # painting hit cross on playre board
    def paint_comp_hit(self, xn, yn, xk, yk):
        self.canv.create_line(xn + 2, yn + 2, xk - 2, yk - 2, fill="blue", width="2")
        self.canv.create_line(xk - 2, yn + 2, xn + 2, yk - 2, fill="blue", width="2")

    # for finish text show
    def player_win(self):
        if self.count_player == 20:
            showinfo("Battleship", "You win")
        else:
            self.canv.bind("<Button-1>", self.player_turn())
    #computer win
    def comp_win(self):
        showinfo("Battleship", "You lose")

    def start(self):
        if self.stug == 1:
            self.k = 0
            self.stug = 0
            self.press = 2
            self.get_random_list_comp()
            self.player_turn()
        else:
            showwarning("Battleship", "Please put ships")

    # This function must ensure priority of the players
    def player_turn(self):
        # clicking on the canvas calls play function
        self.canv.bind("<Button-1>", self.userPlay)

    def check_paint(self):
        count_comp = 0
        for i in range(10):
            for j in range(10):
                # find out rectangle cordiants and size
                xn = j * self.gauge + (j + 1) * self.indent + self.offset_x_user
                yn = i * self.gauge + (i + 1) * self.indent + self.offset_y
                xk = xn + self.gauge
                yk = yn + self.gauge
                if self.player_board[i][j] == '-':
                    self.paint_comp_miss(xn, yn, xk, yk)
                elif self.player_board[i][j] == '+':
                    count_comp = count_comp + 1
                    self.paint_comp_hit(xn, yn, xk, yk)
        if count_comp == 20:
            self.comp_win()
        else:
            self.canv.bind("<Button-1>", self.player_turn())
    #computer turn
    def comp_turn(self):
        self.player_board = fire(self.player_board, shape_of_x, shape_of_x_values, self.all_ship_coord_player, 1)
        self.check_paint()

    # method for user play
    def userPlay(self, event):

        for i in range(10):
            for j in range(10):
                # find out rectangle cordiants and size
                xn = j * self.gauge + (j + 1) * self.indent + self.offset_x_comp
                yn = i * self.gauge + (i + 1) * self.indent + self.offset_y
                xk = xn + self.gauge
                yk = yn + self.gauge
                # checking out are mouse click on the opponent board
                if event.x >= xn and event.x <= xk and event.y >= yn and event.y <= yk:
                    if (self.random_list_comp[i][j] == "O"):
                        self.random_list_comp[i][j] = "-"
                        self.paint_miss(xn, yn, xk, yk)
                    elif self.random_list_comp[i][j] == "X":
                        self.random_list_comp[i][j] = "+"
                        self.count_player += 1
                        self.paint_hit(xn, yn, xk, yk, i, j)

    def moveship(self, event):
        if self.press == 1:
            xn = 0
            yn = 0
            step = self.indent + self.gauge
            if event.char == "a":
                self.corX -= step
                if self.corX >= (self.indent + self.offset_x_user):
                    xn = -step
                else:
                    self.corX += step
            elif event.char == "d":
                self.corX += step
                if self.corX <= (10 * self.gauge + 10 * self.indent + self.offset_x_user):
                    xn = step
                else:
                    self.corX -= step
            elif event.char == "w":
                self.corY -= step
                if self.corY >= (self.indent + self.offset_y):
                    yn = -step
                else:
                    self.corY += step
            elif event.char == "s":
                self.corY += step
                if self.corY <= (10 * self.gauge + 10 * self.indent + self.offset_y):
                    yn = step
                else:
                    self.corY -= step
            self.canv.move(r1, xn, yn)

    def __init__(self, master=None):
        # window initialization
        Frame.__init__(self, master)
        self.pack()

        # creating manu
        self.m = Menu(master)
        master.config(menu=self.m)
        self.m_play = Menu(self.m)
        self.m.add_cascade(label="Mеnu", menu=self.m_play)
        self.m_play.add_command(label="New game", command=self.new_game)

        master.config(menu=self.m)
        self.rand_play = Menu(self.m)
        self.m.add_cascade(label="Edit", menu=self.rand_play)
        self.rand_play.add_command(label="Place Random", command=self.get_random_list_player)
        master.bind("<Key>", self.moveship)
        # canvas creating
        self.createCanvas()


