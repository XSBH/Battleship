from random import *
from Tkinter import *


class InputError(Exception):
    pass


class Battleship(object):

    def __init__(self, n):
        '''(Battleship, int) -> None
        Constructor of class; takes an int parameter to set up game board. '''

        if type(n) != int or n < 2:
            raise InputError()

        self.crd = []
        self.n = int(n)
        self.comp_count = 0
        self.human_count = 0
        self.p1_count = 0
        self.p2_count = 0
        self.c_grid = {}
        self.p1_grid = {}
        self.p2_grid = {}

        for x in range(self.n):
            for y in range(self.n):
                self.p1_grid[(x, y)] = 0
                self.c_grid[(x, y)] = 0
                self.p2_grid[(x, y)] = 0

    def human_move(self, coord):
        '''(Battleship, str) -> int
        Returns an int value to indicate whether location at coord is a "Hit"
        or "Miss". '''

        value = self.check_coord(coord)
        if self.c_grid[value] == 'X':
            self.human_count += 1
            return 1
        else:
            return 3

    def check_coord(self, coord):
        '''(Battleship, str) -> str
        Takes a str input and returns the coord if input is valid, otherwise
        raises error. '''

        if type(coord) != str:
            raise InputError()

        self.coord = coord.split(',')

        try:
            a = int(self.coord[0])
            b = int(self.coord[1])

        except Exception:
            raise InputError()

        if a < 0 or b < 0:
            raise InputError()

        return (a, b)

    def player1_move(self, coord):
        '''(Battleship, str) -> int
        Returns an int value to indicate whether location at coord is a "Hit"
        or "Miss". '''

        value = self.check_coord(coord)
        if self.p2_grid[value] == 'X':
            self.p1_count += 1
            return 1
        else:
            return 3

    def player2_move(self, coord):
        '''(Battleship, str) -> int
        Return an int value to indicate whether location at coordinate
        is "Hit" or "Miss". '''

        value = self.check_coord(coord)
        if self.p1_grid[value] == 'X':
            self.p2_count += 1
            return 1
        else:
            return 3

    def comp_move(self):
        '''(Battleship) -> int
        Return an int value to indicate wether location at a random coordinate
        is "Hit" or "Miss". '''

        self.random = self.rand_coord()

        if self.random not in self.crd:
            self.crd.append(self.random)

        elif self.random in self.crd:
            while self.random in self.crd:
                self.random = self.rand_coord()
            self.crd.append(self.random)

        if self.p1_grid[self.random] == 'X':
            self.comp_count += 1
            return 1
        else:
            return 3

    def check_space(self, x, n):
        '''(Battleship, dict, int) -> Boolean
        Return a boolean value to indicate whether ship with length n
        can fit in grid with dict x. '''
        count, n_list, n_list2 = [], [], []

        for i in range(self.n):
            for k in range(self.n):
                for key in x:
                    if key == (i, k):
                        n_list.append(x[key])
                    if key == (k, i):
                        n_list2.append(x[key])

        self.max_space(n_list, count)
        count = self.max_space(n_list2, count)

        if max(count) >= n:
            return True
        else:
            return False

    def max_space(self, new_list, ct_list):
        '''(Battleship, list, list) -> list
        Return list containing the length of empty spaces in a given grid. '''

        ct = 0
        while len(new_list) != 0:

            if len(new_list) == 1:
                if new_list.pop() == 0:
                    ct += 1
                    ct_list.append(ct)
                    ct = 0
                else:
                    ct_list.append(ct)
                    ct = 0
            else:
                if new_list.pop() == 0:
                    ct += 1
                else:
                    ct_list.append(ct)
                    ct = 0

        for item in ct_list:
            if item > self.n:
                ct_list.remove(item)
                ct_list.append(self.n)
                ct_list.append(item - self.n)

        return ct_list

    def pick_ships(self, n2, n3, n4, n5):
        '''(Battleship, int, int, int, int) -> None
        Provided int parameters gets appended to ship_dict. '''

        self.ship_dict = {}
        l = [n2, n3, n4, n5]

        for item in l:
            try:
                int(item)
            except Exception:
                raise InputError()
            if item == '':
                item = 0
            if item < 0:
                raise InputError()

        self.ship_dict[2] = n2
        self.ship_dict[3] = n3
        self.ship_dict[4] = n4
        self.ship_dict[5] = n5

    def rand_coord(self):
        '''(Battleship) -> tuple
        Returns a random coordinate in the for of a tuple. '''
        a = randrange(self.n)
        b = randrange(self.n)
        return (a, b)

    def place_ships(self, x, ship_n):
        '''(Battleship, dict, int) -> None
        Ships of size ship_n gets placed randomly in grid x. '''

        self.ship_n = ship_n
        crd = self.rand_coord()
        n, e, s, w = [], [], [], []

        while x[crd] == 'X':
            crd = self.rand_coord()

        # Checking which direction will fit a ship of size ship_n
        for i in range(ship_n):
            if (crd[1] + i) < self.n:
                right = (crd[0], crd[1] + i)
                if x[right] == 0:
                    e.append(1)
            if (crd[1] - i) > 0 and (crd[1] - i) < self.n:
                left = (crd[0], crd[1] - i)
                if x[left] == 0:
                    w.append(1)
            if (crd[0] + i) < self.n:
                down = (crd[0] + i, crd[1])
                if x[down] == 0:
                    s.append(1)
            if (crd[0] - i) > 0 and (crd[0] - i) < self.n:
                up = (crd[0] - i, crd[1])
                if x[up] == 0:
                    n.append(1)

        # Marking the coordinates of the ship in the grid x
        if len(e) == ship_n:
            for i in range(ship_n):
                right = (crd[0], crd[1] + i)
                x[right] = 'X'
        elif len(w) == ship_n:
            for i in range(ship_n):
                left = (crd[0], crd[1] - i)
                x[left] = 'X'
        elif len(n) == ship_n:
            for i in range(ship_n):
                up = (crd[0] - i, crd[1])
                x[up] = 'X'
        elif len(s) == ship_n:
            for i in range(ship_n):
                down = (crd[0] + i, crd[1])
                x[down] = 'X'

        else:
            if self.check_space(x, self.ship_n):
                self.place_ships(x, ship_n)


class GUI(object):

    def __init__(self):
        '''(GUI) -> None
        Constructor of class. Takes no parameters. '''

        self.bt_dict = {}
        self.bt_dict2 = {}
        self.bt_dict3 = {}
        self.bt_dict4 = {}
        self.bt_dict5 = {}
        self.error_value = 0

    def set_up(self):
        '''(GUI) -> None
        Resets GUI'''

        self.set_ship()
        self.ship_count()
        self.destroy_frame()

    def destroy_frame(self):
        '''(GUI) -> None
        Removes a few widgets from GUI. '''

        self.done.forget()
        self.logo2.forget()
        self.rb.forget()
        self.rb2.forget()
        self.label.forget()

    def set_ship(self):
        '''(GUI) -> None
        Takes entry from gui as input for ship_dict. '''

        n2 = self.l2_e.get()
        n3 = self.l3_e.get()
        n4 = self.l4_e.get()
        n5 = self.l5_e.get()
        self.b.pick_ships(n2, n3, n4, n5)

    def ship_count(self):
        '''(GUI) -> None
        Randomly places ships on grid and calculates total count of ships. '''

        self.count = 0
        info = self.b.ship_dict
        grid1 = self.b.p1_grid
        grid2 = self.b.c_grid
        grid3 = self.b.p2_grid
        for item in info:
            n = int(info[item])
            for i in range(n):
                self.b.place_ships(grid1, int(item))
                self.b.place_ships(grid2, int(item))
                self.b.place_ships(grid3, int(item))
            self.count += int(item) * n

    def new_game(self):
        '''(GUI) -> None
        Resets previous battleship dicts, and recreates start menu. '''

        self.cmp_frame.destroy()
        self.player_frame.destroy()
        self.mid_frame.destroy()
        self.bt_dict = {}
        self.bt_dict2 = {}
        self.bt_dict3 = {}
        self.bt_dict4 = {}
        self.bt_dict5 = {}

        self.start_menu()

        try:
            self.top.destroy()
        except Exception:
            pass

    def make_button_handler(self, event):
        '''(GUI, event) -> None
        Binding handler. '''

        self.make_button()

    def error(self, image):
        '''(GUI, str) -> None
        Creates an error message with provided image. '''

        top = Toplevel()
        top.title("Error")

        image = PhotoImage(file=image)
        top_label = Label(top, image=image)
        top_label.image = image
        top_label.after(3500, top.destroy)
        top_label.pack()

    def board_design(self, a, b):
        '''(GUI, str, str) -> None
        Creates a board with images a and b as header title. '''

        i2 = PhotoImage(file=a)
        i1 = PhotoImage(file=b)
        bg = 'black'

        label3 = Label(self.cmp_frame, image=i2, bd=6, bg=bg)
        label3.image = i2
        label3.grid(row=0, column=0)
        self.cf2 = Frame(self.cmp_frame, bd=10, bg=bg)
        self.cf2.grid(row=1, column=0)

        label2 = Label(self.player_frame, image=i1, bd=6, bg=bg)
        label2.image = i1
        label2.grid(row=0, column=0)
        self.hf2 = Frame(self.player_frame, bd=10, bg=bg)
        self.hf2.grid(row=1, column=0)

    def win_frame(self, image):
        '''(GUI, str) -> None
        Returns a restart frame with provided image after all ship have been
        sunk. '''

        self.top = Toplevel()
        bg = 'black'
        self.top['bg'] = bg

        image = PhotoImage(file=image)
        label = Label(self.top, image=image, bg=bg)
        label.image = image
        label.pack()

        a = Button(self.top, text="Restart", fg='red', bg=bg)
        a['command'] = lambda: self.new_game()
        a.pack()
        b = Button(self.top, text="Quit", fg='red', bg=bg)
        b['command'] = lambda: root.destroy()
        b.pack()

    def make_button(self):
        '''(GUI) -> None
        Create a grid with buttons at every coordinate. '''

        if self.v.get() == 0:
            self.error('image/warning.gif')

        else:
            value = self.entry.get()
            num = value.split('x')[0]

            try:
                int(num)
                # Display Player vs Player interface or Player vs Computer
                # interface based on user selection
                if self.v.get() == 1:
                    self.board_design('image/4.gif', 'image/2.gif')
                else:
                    self.board_design('image/player2.gif', 'image/player1.gif')

                # Set up Battleship class based on user inputs
                self.change_background()
                i = int(value.split('x')[0])
                n = i * i
                self.b = Battleship(i)
                self.set_up()
                img = PhotoImage(file='image/but3.gif')
                img2 = PhotoImage(file='image/but1.gif')

                for index in range(n):
                    r = index / i
                    c = index % i

                    crd = '%s, %s' % (str(r), str(c))
                    crd2 = '(%s, %s)' % (str(r), str(c))
                    tup = (r, c)

                    # Setting up the individual unit buttons on the grid
                    btn = Button(self.hf2, text=crd, image=img, fg='#C9DECB')
                    btn.config(width=30, height=30, bg='black')
                    btn.config(compound=CENTER, relief=FLAT)
                    btn.image = img
                    btn2 = Button(self.cf2, text=crd, image=img2, fg='#74138C')
                    btn2.config(width=30, height=30, bg='black')
                    btn2.config(relief=FLAT, compound=CENTER)
                    btn2.image = img2

                    # Display the player's ships on his own board
                    if self.v.get() == 1:
                        if self.b.p1_grid[tup] == 'X':
                            btn.config(text='o', font=('Webdings', 24))

                    # Display each unit on the grid as a button with its
                    # respective coordinates
                    self.bt_dict[crd2] = btn
                    self.bt_dict4[tup] = btn
                    self.bt_dict2[btn2] = crd
                    self.bt_dict3[btn] = crd
                    self.bt_dict5[tup] = btn2
                    btn.grid(row=r, column=c)
                    btn2.grid(row=r, column=c)

                    # If in Player vs Player mode, make units on both board
                    # clickable, otherwise only make player units clickable
                    if self.v.get() == 1:
                        btn2.bind("<Button-1>", self.selected_click2, '+')
                    elif self.v.get() == 2:
                        btn.bind("<Button-1>", self.selected_click3, '+')
                        btn2.bind("<Button-1>", self.selected_click1, '+')

            except Exception:
                self.new_game()
                self.error('image/warning3.gif')

    def change_background(self):
        '''(GUI) -> None
        Changes the background of widgets to black/grey. '''

        f_list = [self.mid_frame, self.logo2, self.label, self.label2, \
                  self.l2, self.l3, self.l4, self.l5]
        e_list = [self.entry, self.l2_e, self.l3_e, self.l4_e, self.l5_e]
        s_dict = {'image/2unit2.gif': self.l2, 'image/3unit2.gif': self.l3, \
                  'image/4unit2.gif': self.l4, 'image/5unit2.gif': self.l5, \
                  'image/grid2.gif': self.label2}

        for item in f_list:
            item['bg'] = 'black'
        for item in e_list:
            item['bg'] = 'grey'
        for key in s_dict:
            image = PhotoImage(file=key)
            s_dict[key]['image'] = image
            s_dict[key].image = image

    def selected_click1(self, event):
        '''(GUI, event) -> None
        A binding event for player 1 buttons on grid; unbinds player 2 buttons
        so game does not proceed until move made. '''

        if event.widget in self.bt_dict2:
            func = self.b.player1_move(self.bt_dict2[event.widget])
            key = event.widget
            self.config(func, key)
            for key in self.bt_dict2:
                key.unbind('<Button-1>')
            self.bt_dict2.pop(event.widget)
            for key in self.bt_dict3:
                key.bind("<Button-1>", self.selected_click3, '+')

        self.show_boat(self.bt_dict5, self.bt_dict4, \
                       self.b.p2_grid, self.b.p1_grid)

        self.win_message(self.b.p1_count, self.b.p2_count,\
                         'image/p2win.gif', 'image/p1win.gif')

    def show_boat(self, dict1, dict2, grid, grid2):
        '''(GUI, dict, dict, dict, dict) -> None
        Shows boat image at coordinates with ships. '''

        for key in dict1:
            if grid[key] == 'X':
                dict1[key].config(text='o', font=('Webdings', 24))
        for key in dict2:
            if grid2[key] == 'X':
                text = str(key)[1:-1]
                dict2[key].config(text=text, font=("Times", 10))

    def selected_click3(self, event):
        '''(GUI, event) -> None
        A binding event for player 2 buttons on grid; unbinds player 1 buttons
        so game does not proceed until move made. '''

        if event.widget in self.bt_dict3:
            func = self.b.player2_move(self.bt_dict3[event.widget])
            key = event.widget
            self.config(func, key)
            for key in self.bt_dict3:
                key.unbind('<Button-1>')
            self.bt_dict3.pop(event.widget)
            for key in self.bt_dict2:
                key.bind("<Button-1>", self.selected_click1, '+')

        self.show_boat(self.bt_dict4, self.bt_dict5, \
                       self.b.p1_grid, self.b.p2_grid)

        self.win_message(self.b.p1_count, self.b.p2_count,\
                         'image/p2win.gif', 'image/p1win.gif')

    def config(self, func, key):
        '''(GUI, method, widget) -> none
        Changes image of button if coordinate at widget contains a ship. '''

        image = PhotoImage(file='image/but4.gif')

        if func == 1:
            key.config(text='HIT', font=("Impact", 11))
            key.config(fg='black', image=image, compound=CENTER)
            key.image = image

        else:
            key.config(font=("Impact", 10), text='MISS')

    def win_message(self, count1, count2, image1, image2):
        '''(GUI, int, int, str, str) -> None
        Opens up a "win frame" if count of boat sunk matchs
        total boat count. '''

        if count1 == self.count:
            self.win_frame(image1)

        elif count2 == self.count:
            self.win_frame(image2)

    def selected_click2(self, event):
        '''(GUI, event) -> None
        A binding event to bind button to coordinate. '''

        func = self.b.human_move(self.bt_dict2[event.widget])
        key = event.widget
        self.config(func, key)
        event.widget.unbind('<Button-1>')

        func2 = self.b.comp_move()
        key2 = self.bt_dict[str(self.b.random)]
        self.config(func2, key2)

        self.win_message(self.b.human_count, self.b.comp_count,\
                         'image/win.gif', 'image/lost.gif')

    def validate(self, string):
        '''(GUI, str) -> Boolean
        A validation method: only allows user to input ints. '''

        if string in '0123456789':
            return True
        else:
            return False

    def start_menu(self):
        '''(GUI) -> None
        The start menu. '''

        global root

        self.mid_frame = Frame(root, bd=10)
        self.mid_frame.grid(row=0, column=1)

        self.cmp_frame = Frame(root, borderwidth=8, bg='black')
        self.cmp_frame.grid(row=0, column=2)

        self.player_frame = Frame(root, borderwidth=8, bg='black')
        self.player_frame.grid(row=0, column=0)

        # Creating menu logo
        logo = PhotoImage(file='image/logo2.gif')
        self.logo2 = Label(self.mid_frame, image=logo, bd=10)
        self.logo2.image = logo
        self.logo2.pack()

        # Creating menu labels and radiobuttons
        image = PhotoImage(file='image/paga.gif')
        self.label = Label(self.mid_frame, image=image)
        self.label.image = image
        self.label.pack()
        self.v = IntVar()
        self.rb = Radiobutton(self.mid_frame, text="Computer", variable=self.v)
        self.rb['value'] = 1
        self.rb.pack()
        self.rb2 = Radiobutton(self.mid_frame, text="Human", variable=self.v)
        self.rb2['value'] = 2
        self.rb2.pack()

        grid = PhotoImage(file='image/grid.gif')
        self.label2 = Label(self.mid_frame, image=grid, bd=3)
        self.label2.image = grid
        self.label2.pack()
        v = StringVar()
        self.entry = Entry(self.mid_frame, textvariable=v)
        self.entry.insert(0, '10x10')
        self.entry.pack()

        # Validating necessary inputs
        vcmd = (self.mid_frame.register(self.validate), '%S')

        # Creating the different unit images
        unit2 = PhotoImage(file='image/2unit.gif')
        self.l2 = Label(self.mid_frame, image=unit2, bd=3, )
        self.l2.image = unit2
        self.l2.pack()
        self.l2_e = Entry(self.mid_frame, validate='key', validatecommand=vcmd)
        self.l2_e.insert(0, 1)
        self.l2_e.pack()

        unit3 = PhotoImage(file='image/3unit.gif')
        self.l3 = Label(self.mid_frame, image=unit3, bd=3)
        self.l3.image = unit3
        self.l3.pack()
        self.l3_e = Entry(self.mid_frame, validate='key', validatecommand=vcmd)
        self.l3_e.insert(0, 1)
        self.l3_e.pack()

        unit4 = PhotoImage(file='image/4unit.gif')
        self.l4 = Label(self.mid_frame, image=unit4, bd=3)
        self.l4.image = unit4
        self.l4.pack()
        self.l4_e = Entry(self.mid_frame, validate='key', validatecommand=vcmd)
        self.l4_e.insert(0, 1)
        self.l4_e.pack()

        unit5 = PhotoImage(file='image/5unit.gif')
        self.l5 = Label(self.mid_frame, image=unit5, bd=3)
        self.l5.image = unit5
        self.l5.pack()
        self.l5_e = Entry(self.mid_frame, validate='key', validatecommand=vcmd)
        self.l5_e.insert(0, 1)
        self.l5_e.pack()

        done = PhotoImage(file='image/a3.gif')
        self.done = Button(self.mid_frame, image=done, relief=FLAT, bd=10)

        # Creating a return button in the actual game interface
        self.done['command'] = lambda: self.make_button()
        self.done.image = done
        self.done.focus_force()
        self.done.bind('<Return>', self.make_button_handler)
        self.done.pack()

if __name__ == '__main__':

    root = Tk()
    root.title('BATTLESHIP')
    root['background'] = 'black'
    gui = GUI()

    menu = Menu(root)
    root.config(menu=menu)

    # Adding additional menu options
    menu1 = Menu(menu)
    menu.add_cascade(label="File", menu=menu1)
    menu1.add_command(label="New Game", command=lambda: gui.new_game())
    menu1.add_command(label="Reset Board", command=lambda: gui.make_button())
    menu1.add_separator()
    menu1.add_command(label="Exit", command=lambda: root.destroy())

    gui.start_menu()
    root.mainloop()
