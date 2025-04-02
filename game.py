import sqlite3 as sql
from ast import literal_eval
from collections import deque
from time import time
from tkinter import Tk, Canvas, PhotoImage, TclError, CENTER, NW, Label, W, E
from block import Block
from character import Character
from animation import AnimationNode



class Game:

    def __init__(self):
        self.world_blocks = []
        self.pick_ups = []
        self.valid_points = []
        self.bot_home = []
        self.scatter_pos = []
        self.block_size = 14
        self.food = {'0': (4, 1, 'white'), '2': (12, 10, 'pink')}
        self.the_map = [
            '111111111111111111111',
            '120000000111000000021',
            '101101110111011101101',
            '100000000000000000001',
            '101101011111110101101',
            '101101000111000101101',
            '100001110111011100001',
            '111101000000000101111',
            '111101011000110101111',
            'f0000001004001000000b',
            '111101010444010101111',
            '111101011111110101111',
            '100000000000000000001',
            '101101101111101101101',
            '101100000000000001101',
            '101101111111111101101',
            '100000000111300000001',
            '101111110111011111101',
            '120000000000000000021',
            '111111111111111111111'
        ]
        self.width, self.height = self.block_size * len(self.the_map[0]), self.block_size * len(self.the_map)

        self.window = Tk()
        self.window.title("Testing")
        self.window.winfo_toplevel()
        self.canvas = Canvas(self.window, width=self.width, height=self.height, background='black')
        self.canvas.grid(row=0, column=0, sticky=NW)

        self.score = Label( self.window, text='Score: 0', font=( "Arial", 12 ) )
        self.lives = Label( self.window, text='Lives: 0', font=( "Arial", 12 ) )
        self.score.grid(row=1, column=0, sticky=W)
        self.lives.grid(row=1, column=0, sticky=E)
        self.window.resizable(0 , 0)
       
        self.game_images = {
                'paused': [
                    PhotoImage(file="assets/pause1.png"),
                    PhotoImage(file="assets/pause2.png"),
                    PhotoImage(file="assets/pause3.png"),
                    PhotoImage(file="assets/pause4.png"),
                    False, 1
                    ],
                "reset": [
                    PhotoImage(file="assets/pause2.png"),
                    PhotoImage(file="assets/pause3.png"),
                    PhotoImage(file="assets/pause4.png"),
                    False, 1
                    ],
                "game_over": [
                    PhotoImage(file="assets/game_over1.png"),
                    PhotoImage(file="assets/game_over2.png"),
                    PhotoImage(file="assets/game_over3.png"),
                    True, 0.03
                    ],
                "red": {
                    "up": [
                        PhotoImage(file="assets/red_up1.png"),
                        PhotoImage(file="assets/red_up2.png"),
                        True, 0.03
                        ],
                    "down": [
                        PhotoImage(file="assets/red_down1.png"),
                        PhotoImage(file="assets/red_down2.png"),
                        True, 0.03
                        ],
                    "left": [
                        PhotoImage(file="assets/red_left1.png"),
                        PhotoImage(file="assets/red_left2.png"),
                        True, 0.03
                        ],
                    "right": [
                        PhotoImage(file="assets/red_right1.png"),
                        PhotoImage(file="assets/red_right2.png"),
                        True, 0.03
                        ]
                    },
                "cyan": {
                    "up": [
                        PhotoImage(file="assets/cyan_up1.png"),
                        PhotoImage(file="assets/cyan_up2.png"),
                        True, 0.03
                        ],
                    "down": [
                        PhotoImage(file="assets/cyan_down1.png"),
                        PhotoImage(file="assets/cyan_down2.png"),
                        True, 0.03
                        ],
                    "left": [
                        PhotoImage(file="assets/cyan_left1.png"),
                        PhotoImage(file="assets/cyan_left2.png"),
                        True, 0.03
                        ],
                    "right": [
                        PhotoImage(file="assets/cyan_right1.png"),
                        PhotoImage(file="assets/cyan_right2.png"),
                        True, 0.03
                        ]
                    },
                "pink": {
                    "up": [
                        PhotoImage(file="assets/pink_up1.png"),
                        PhotoImage(file="assets/pink_up2.png"),
                        True, 0.03
                        ],
                    "down": [
                        PhotoImage(file="assets/pink_down1.png"),
                        PhotoImage(file="assets/pink_down2.png"),
                        True, 0.03
                        ],
                    "left": [
                        PhotoImage(file="assets/pink_left1.png"),
                        PhotoImage(file="assets/pink_left2.png"),
                        True, 0.03
                        ],
                    "right": [
                        PhotoImage(file="assets/pink_right1.png"),
                        PhotoImage(file="assets/pink_right2.png"),
                        True, 0.03
                        ]
                    },
                "orange": {
                    "up": [
                        PhotoImage(file="assets/orange_up1.png"),
                        PhotoImage(file="assets/orange_up2.png"),
                        True, 0.03
                        ],
                    "down": [
                        PhotoImage(file="assets/orange_down1.png"),
                        PhotoImage(file="assets/orange_down2.png"),
                        True, 0.03
                        ],
                    "left": [
                        PhotoImage(file="assets/orange_left1.png"),
                        PhotoImage(file="assets/orange_left2.png"),
                        True, 0.03
                        ],
                    "right": [
                        PhotoImage(file="assets/orange_right1.png"),
                        PhotoImage(file="assets/orange_right2.png"),
                        True, 0.03
                        ]
                    },
                "yellow": {
                    "normal": [ PhotoImage(file="assets/pacman_normal.png"), False, 1 ],
                    "up": [
                        PhotoImage(file="assets/pacman_up1.png"),
                        PhotoImage(file="assets/pacman_up2.png"),
                        PhotoImage(file="assets/pacman_normal.png"),
                        True, 0.03
                        ],
                    "down": [
                        PhotoImage(file="assets/pacman_down1.png"),
                        PhotoImage(file="assets/pacman_down2.png"),
                        PhotoImage(file="assets/pacman_normal.png"),
                        True, 0.03
                        ],
                    "left": [
                        PhotoImage(file="assets/pacman_left1.png"),
                        PhotoImage(file="assets/pacman_left2.png"),
                        PhotoImage(file="assets/pacman_normal.png"),
                        True, 0.03
                        ],
                    "right": [
                        PhotoImage(file="assets/pacman_right1.png"),
                        PhotoImage(file="assets/pacman_right2.png"),
                        PhotoImage(file="assets/pacman_normal.png"),
                        True, 0.03
                        ]
                    },
                "scared": {
                    "agitate": [
                        PhotoImage(file="assets/scared1.png"),
                        PhotoImage(file="assets/scared2.png"),
                        True, 0.03
                        ],
                    "acclimate": [
                        PhotoImage(file="assets/scared1.png"),
                        PhotoImage(file="assets/scared3.png"),
                        PhotoImage(file="assets/scared2.png"),
                        PhotoImage(file="assets/scared4.png"),
                        True, 0.05
                        ]
                       },
                "wall": [ PhotoImage(file="assets/wall.png"), False, 1],
                "food": [ PhotoImage(file="assets/food.png"), False, 1],
                "power_up": [ PhotoImage(file="assets/power_up.png"), False, 1]
                }

        self.cx = sql.connect("paths.db")
        self.cu = self.cx.cursor()
        self.offset = 1
        y = self.offset
        for i, blocks in enumerate(self.the_map):
            x = self.offset
            for j, block in enumerate(blocks):
                if block in self.food.keys():
                    x1 = ((self.block_size / 2) + x) - (self.food[block][0] / 2)
                    y1 = ((self.block_size / 2) + y) - (self.food[block][0] / 2)
                    fimg = self.game_images["food" if block == '0' else "power_up"][0]
                    f = self.canvas.create_image( x1, y1, anchor=NW, image=fimg )
                    fd = Block(self.canvas, f, block, self.world_blocks, self.pick_ups,  fimg, self.game_images, "food", self.food[block][1] )
                    if block == '2':
                        self.scatter_pos.append((x, y))
                    self.world_blocks.append(fd)
                    self.pick_ups.append(fd)
                    self.valid_points.append((x, y))
                elif block == '1':
                    bimg = self.game_images["wall"][0]
                    b = self.canvas.create_image( x, y, anchor=NW, image=bimg )
                    blk = Block(self.canvas, b, block, self.world_blocks, self.pick_ups, bimg, self.game_images, "wall")
                    self.world_blocks.append(blk)

                elif block == '3':
                    cpos = (x, y)
                    self.valid_points.append((x, y))
                elif block == '4':
                    self.bot_home.append((x, y))
                    self.valid_points.append((x, y))
                elif block in ['f', 'b']:
                    x1 = ((self.block_size / 2) + x) - (self.food['0'][0] / 2)
                    y1 = ((self.block_size / 2) + y) - (self.food['0'][0] / 2)
                    fimg = self.game_images["food"][0]
                    f = self.canvas.create_image( x1, y1, anchor=NW, image=fimg )
                    fd = Block(self.canvas, f, block, self.world_blocks, self.pick_ups, fimg, self.game_images, "food", self.food['0'][1])
                    self.world_blocks.append(fd)
                    self.pick_ups.append(fd)
                    self.valid_points.append((x, y))
                    self.valid_points.append((x - self.block_size if block == 'f' else x + self.block_size, y))
                x += self.block_size
            y += self.block_size
        
        paths = {}
        t1 = time()
        try:
            self.cu.execute("create table coord(start_stop, path)")
            for index, spoint in enumerate(self.valid_points):
                print(round((100 * index + self.offset) / len(self.valid_points), 2), "%")
                for epoint in self.valid_points:
                    if spoint == epoint:
                        continue
                    else:
                        the_path = self.get_shortest_path(self.valid_points, spoint, epoint)
                        if the_path:
                            paths[(spoint, epoint)] = the_path
                            self.cu.execute("insert into coord values (?, ?)", (f'({spoint}, {epoint})', f'{the_path}'))
            self.cx.commit()
        except sql.OperationalError:
            for key, val in self.cu.execute('select * from coord'):
                paths[literal_eval(key)] = literal_eval(val)
        self.cx.close()

        t = time() - t1
        print('took: ', int(t // 60), 'min ', int(t % 60), 'sec')


        cimg = self.game_images["yellow"]["normal"][0]
        cname = self.canvas.create_image( cpos[0], cpos[1], anchor=NW, image=cimg)
        self.character = Character( self.canvas, cname, paths, self.valid_points, self.block_size,
                                    'yellow', cpos, cimg, True)
        self.character.anim =  AnimationNode(self.canvas, cname, cimg, self.game_images["yellow"], "normal")
        self.character.width = self.width
        self.character.update_stats = self.update_stats
        self.world_blocks.insert(0, self.character)
        self.update_stats( self.character.score, self.character.lives)
        colors = ['cyan', 'pink', 'orange', 'red']
        for i in range( len(colors) ):
            color = colors.pop()
            home = self.bot_home.pop()
            bimg = self.game_images[color]["down"][0]
            bot_name = self.canvas.create_image(home[0], home[1], anchor=NW, image=bimg)
            the_bot = Character(self.canvas, bot_name, paths, self.valid_points, self.block_size,
                                color, home, bimg)
            the_bot.anim = AnimationNode(self.canvas, bot_name, bimg,
                                         self.game_images[color]|self.game_images["scared"], "down")
            the_bot.scatter_pos = self.scatter_pos.pop()
            the_bot.reset_game = self.reset_game
            self.world_blocks.append(the_bot)

        self.paused = True
        self.canvas.bind("<KeyRelease-Return>", self.start_game)

        self.img = self.game_images["paused"][0]
        self.pd = self.canvas.create_image( self.width/2, self.height/2, anchor=CENTER, image= self.img )
        self.start_anim = AnimationNode(self.canvas, self.pd, self.img, self.game_images, "paused")

        self.canvas.focus_set()
        self.window.after(100, self.update_game)
        self.window.mainloop()
        

    def get_shortest_path(self, d_map, start, end):
            if start in d_map and end in d_map:
                directions = [
                    (0, self.block_size), (self.block_size, 0), (0, -self.block_size), (-self.block_size, 0)
                ]
                queue = deque([(start, [])])
                visited = set()
                while queue:
                    (x_axis, y_axis), path = queue.popleft()
                    if (x_axis, y_axis) == end:
                        return path
                    for dx, dy in directions:
                        nx, ny = x_axis + dx, y_axis + dy
                        next_pos = (nx, ny)
                        if next_pos in d_map and next_pos not in visited:
                            visited.add(next_pos)
                            queue.append((next_pos, path + [next_pos]))
            return None

    def update_game(self):
            try:
                if not self.paused and self.pick_ups and self.character.lives:
                    for bk in self.world_blocks:
                        bk.move(self.character)
                    self.canvas.update()
            except TclError:
                pass
            self.window.after(100, self.update_game)
    
    def start_game(self, _event):
        self.start_screen()

    def start_screen(self):
        self.start_screen_anim()

    def start_screen_anim(self):
        if not self.start_anim.finished():
            self.start_anim.play(self.start_anim.current_anim)
            self.canvas.after(1000 if self.character.lives else 100, self.start_screen_anim)
        else:
            self.canvas.delete(self.pd)
            del self.pd, self.start_anim
            self.canvas.unbind("<KeyRelease-Return>")
            self.paused = False

    def update_stats(self, score, lives):
        self.score['text'] = f'Score: {score}'
        self.lives['text']  = f'Lives: {lives}'

    def reset_game(self):
        self.paused = True
        self.character.current_anim = "normal"
        for the_bot in Character.bots:
            bot = Character.bots[ the_bot ]
            self.canvas.moveto(bot.id, bot.HOME[0], bot.HOME[1])
        self.canvas.moveto( self.character.id, self.character.HOME[0], self.character.HOME[1] )
        self.character.lives -= 1
        self.update_stats( self.character.score, self.character.lives)
        self.reset_game_screen() if self.character.lives else self.game_over_screen()

    def game_over_screen(self):
        self.img = self.game_images["game_over"][0]
        self.pd = self.canvas.create_image( self.width/2, self.height/2, anchor=CENTER, image= self.img )
        self.start_anim = AnimationNode(self.canvas, self.pd, self.img, self.game_images, "game_over")
        self.start_screen_anim()

    def reset_game_screen(self):
        self.img = self.game_images["reset"][0]
        self.pd = self.canvas.create_image( self.width/2, self.height/2, anchor=CENTER, image= self.img )
        self.start_anim = AnimationNode(self.canvas, self.pd, self.img, self.game_images, "reset")
        self.start_screen_anim()
