from timer import Timer
from tkinter import PhotoImage


class AnimationNode:

    def __init__(self, canvas, name, img, anim, current_anim):
        self.canvas = canvas
        self.id = name
        self.img = img
        self.anim = anim
        self.current_anim = current_anim
        self.timer  = Timer( anim[ current_anim ][ -1 ] )
        self.frame = 0
        self.frames = len(self.anim[self.current_anim]) - 3
        self.loop = self.anim[self.current_anim][ -2 ]

    def play(self, name: str):
        if self.timer.stopped():
            self.change_frame( name, name == self.current_anim )

    def change_frame(self, name: str, flag: bool):
        if flag:
            self.frame = self.frame + 1 if self.frame < self.frames else 0 if self.loop else self.frame
        else:
            self.frame = 0
            self.frames = len(self.anim[ name ] ) - 3
            self.timer = Timer( self.anim[ name ][ -1 ] )
            self.loop = self.anim[name][-2]
            self.current_anim = name
        self.img = self.anim[self.current_anim][self.frame]
        self.canvas.itemconfig(self.id, image=self.img)

    def finished(self):
        if not self.loop:
            return self.frame == self.frames
        return False
        
