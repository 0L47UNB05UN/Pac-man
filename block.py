from vector import Vector2D
from animation import AnimationNode


class Block:

    def __init__( self, canvas, name,  tpe, world_objects, pick_ups,  img, anim, color, score=0 ):
        self.canvas = canvas
        self.id = name
        self.type = tpe
        self.world_objects = world_objects
        self.pick_ups = pick_ups
        self.img = img
        self.anim = anim
        self.color = color
        self.score = score
        self.offset = 5 if self.score else 8
        self.radius = self.get_radius()
        self.color = color
        self.anm = AnimationNode(canvas, name, img, anim, color)

    def move(self, obj):
        if self.collide(obj):              
            if  self.type == '1':
                obj.collision()
            else:
                self.world_objects.remove(self)
                self.pick_ups.remove( self )
                self.canvas.delete(self.id)
                obj.collision( [ self.score, 'power_up' if self.type == '2' else 'normal' ] )

    def collide(self, obj):
        coord = self.canvas.coords(self.id)
        pos = Vector2D( coord[0] + self.radius.x, coord[1] + self.radius.y )
        fcoord = self.canvas.coords(obj.id)
        fpos = Vector2D( fcoord[0] + obj.radius.x, fcoord[1] + obj.radius.y )
        if (self.radius.length() + obj.radius.length() - self.offset) > \
           pos.distance_to(fpos):
            return True
        return False

    def get_radius(self):
        return Vector2D( self.img.width() / 2, self.img.height() / 2 )

    def getPosition(self):
        return self.canvas.coords(self.id)
