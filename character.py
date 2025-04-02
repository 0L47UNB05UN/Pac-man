from vector import Vector2D
from timer import Timer

class Character:
    
    bots = {}

    def __init__(self, canvas, name, the_map, valid_points, size, color, home, img,  human=False, offset=1):
        self.canvas = canvas
        self.id = name
        self.map = the_map
        self.offset = offset
        self.valid_points = valid_points
        self.size = size
        self.color = color
        self.HOME = home
        self.img = img
        self.human = human
        self.radius = self.get_radius()
        self.prev = None
        self.vel = Vector2D()
        self.width = 0
        self.score = 0
        self.lives = 3
        self.speed = 7
        self.scatter_pos = None
        self.should_scatter = True
        self.c_direction = self.p_direction = Vector2D()
        self.is_vulnerable = False
        self.attack_time = 10
        self.vulnerable_time = 15
        self.vulnerable_timer = Timer(self.vulnerable_time)
        self.attack_timer = Timer(self.attack_time)
        if not human:
            Character.bots[self.color] = self
        else:
            self.map_input()
            self.update_stats = None
        self.anim = None
        self.current_anim = ""
        self.reset_game = None

    def activate_vulnerability(self):
        for bot in Character.bots:
            Character.bots[bot].become_vulnerable()

    def map_input(self):
        if self.human:
            self.canvas.bind('<KeyRelease-Up>', self.move_up)
            self.canvas.bind('<KeyRelease-Down>', self.move_down)
            self.canvas.bind('<KeyRelease-Right>', self.move_right)
            self.canvas.bind('<KeyRelease-Left>', self.move_left)

    def move_up(self, _event):
        self.c_direction = Vector2D(0, -self.speed)

    def move_down(self, _event):
        self.c_direction = Vector2D(0, self.speed)

    def move_right(self, _event):
        self.c_direction = Vector2D(self.speed, 0)

    def move_left(self, _event):
        self.c_direction = Vector2D(-self.speed, 0)

    def get_shortest_path(self, start, end):
        paths = self.map.get((start, end))
        return Vector2D(paths[0][:2]) if paths else None

    def collide(self, obj):
        coord = self.canvas.coords(self.id)
        pos = Vector2D( coord[0] + self.radius.x, coord[1] + self.radius.y )
        fcoord = self.canvas.coords(obj.id)
        fpos = Vector2D( fcoord[0] + obj.radius.x, fcoord[1] + obj.radius.y )
        if (self.radius.length() + obj.radius.length() - 8) > pos.distance_to(fpos):
            return True
        return False

    def get_radius(self):
        return Vector2D( self.img.width() / 2, self.img.height() / 2 )

    def move(self, obj):
        if self.human:
            self.human_move()
        else:
            self.bot_move(obj)

    def bot_move(self, obj):
        pos = Vector2D(self.canvas.coords(self.id)[:2])
        ppos = self.get_position()
        if self.is_vulnerable:
            self.vulnerable(obj, pos, ppos)
        else:
            if self.should_scatter:
                self.scatter(pos, ppos)
            else:
                getattr(self, self.color)(obj, pos, ppos)
                if self.attack_timer.stopped():
                    self.should_scatter = True
            if self.collide(obj):
                self.reset_game()
        self.anim.play(self.current_anim)

    def human_move(self):
        self.canvas.move(self.id, self.vel.x, self.vel.y)
        pos = self.canvas.coords(self.id)
        ppos = self.get_position()
        if pos[0] <= 0:
            self.canvas.moveto(self.id, self.width, ppos[1])
        elif pos[0]+self.size >= self.width + self.size:
            self.canvas.moveto(self.id, -self.size/2+self.offset, ppos[1])
            self.c_direction = Vector2D(self.speed, 0)

        if self.is_valid_direction(self.c_direction):
            self.vel = self.c_direction
            self.p_direction = self.vel
        elif self.is_valid_direction(self.p_direction):
            self.vel = self.p_direction
        else:
            self.vel = self.c_direction = Vector2D()
        self.current_anim = self.vel.coord_direction()
        self.anim.play(self.current_anim)

    def is_valid_direction(self, direction: Vector2D) -> bool:
        pos = self.get_position()
        direction = direction.direction().mult(self.size).add(Vector2D(pos))
        if (direction.x, direction.y) in self.valid_points:
            if pos != tuple(self.canvas.coords(self.id)[:2]) and not self.vel.length():
                self.canvas.moveto(self.id, pos[0] - self.offset, pos[1] - self.offset)
            return True
        return False

    def collision(self, val=None):
        if val:
            if 'normal' in val:
                self.score += val[0]
                self.update_stats(self.score, self.lives)
            else:  
                self.activate_vulnerability()
        else:
            self.canvas.move(self.id, -self.p_direction.x, -self.p_direction.y)
            self.vel = Vector2D()

    def get_position(self):
        pos = tuple(self.canvas.coords(self.id) )
        self.prev = pos if pos in self.valid_points else self.prev
        if self.human:
            x, y = round(pos[0] / self.size), round(pos[1] / self.size)
            x = x * self.size + self.offset if x else self.offset
            y = y * self.size + self.offset if y else self.offset
            return x, y
        return self.prev

    def vulnerable(self, obj, pos, ppos):
        path = self.get_shortest_path(ppos, self.HOME)
        if path:
            vel = pos.direction_to(path).mult(self.speed)
            self.canvas.move(self.id, vel.x, vel.y)
        if self.collide(obj):
            pass
        if self.vulnerable_timer.stopped():
            self.is_vulnerable = False
        self.current_anim = "agitate" if self.vulnerable_timer.time_left() > 5 else "acclimate"

    def become_vulnerable(self):
        self.is_vulnerable = True
        self.vulnerable_timer.start()

    def red(self, obj, pos, ppos):
        path = self.get_shortest_path(ppos, obj.get_position())
        if path:
            vel = pos.direction_to(path).mult(self.speed)
            self.current_anim = vel.coord_direction()
            self.canvas.move(self.id, vel.x, vel.y)

    def cyan(self, obj, pos, ppos):
        blinky_pos = Character.bots['red'].get_position()
        obj_pos = obj.get_position()
        two_tiles_ahead = (obj_pos[0] + 4 * obj.p_direction.x, obj_pos[1] + 4 * obj.p_direction.y)

        vector_x = two_tiles_ahead[0] - blinky_pos[0]
        vector_y = two_tiles_ahead[1] - blinky_pos[1]

        target_x = blinky_pos[0] + 1 * vector_x
        target_y = blinky_pos[1] + 1 * vector_y
        path = self.get_shortest_path(ppos, (target_x, target_y))
        if path:
            vel = pos.direction_to(path).mult(self.speed)
            self.current_anim = vel.coord_direction()
            self.canvas.move(self.id, vel.x, vel.y)

    def orange(self, obj, pos, ppos):
        obj_pos = obj.get_position()
        path = self.get_shortest_path( ppos, obj_pos )
        if path:
            vel = pos.direction_to(path).mult(self.speed)
            self.current_anim = vel.coord_direction()
            self.canvas.move(self.id, vel.x, vel.y)
        if pos.distance_to( Vector2D( obj_pos) ) < self.size * 3.12:
            self.attack_timer.stop()
            self.should_scatter = True

    def pink(self, obj, pos, ppos):
        obj_direction = obj.p_direction.direction().mult(self.size).add( Vector2D(obj.get_position()) )
        path = self.get_shortest_path(ppos, ( obj_direction.x, obj_direction.y ) )
        if path:
            vel = pos.direction_to(path).mult(self.speed)
            self.current_anim = vel.coord_direction()
            self.canvas.move(self.id, vel.x, vel.y)

    def scatter(self, pos, ppos):
        path = self.get_shortest_path(ppos, self.scatter_pos )
        if path:
            vel = pos.direction_to(path).mult(self.speed)
            self.current_anim = vel.coord_direction()
            self.canvas.move(self.id, vel.x, vel.y)
        if pos.distance_to( Vector2D(self.scatter_pos) ) < self.size:
            self.should_scatter = False
            self.attack_timer.start()
