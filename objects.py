import pygame as pg
from settings import *

vec = pg.Vector2


class Food:
    def __init__(self, pos):
        self.pos = vec(pos)
        self.color = RED

    def draw(self, surf):
        pg.draw.rect(surf, self.color, (self.pos.x, self.pos.y, TILESIZE, TILESIZE))


class Snake:
    def __init__(self, pos):
        self.dir = vec(0, 0)
        self.prev_dir = vec(0, 0)
        self.body = [vec(pos)]

    def prevent_going_inside_itself(self, vec):
        if len(self.body)>1 and (self.body[-1] - self.body[-2]) == vec*-1:
            self.dir = vec * -1

    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.dir = vec(-1, 0) * TILESIZE
            self.prevent_going_inside_itself(self.dir)
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.dir = vec(1, 0) * TILESIZE
            self.prevent_going_inside_itself(self.dir)
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.dir = vec(0, -1) * TILESIZE
            self.prevent_going_inside_itself(self.dir)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.dir = vec(0, 1) * TILESIZE
            self.prevent_going_inside_itself(self.dir)

        self.prev_dir = self.dir.copy()

    def update(self):
        self.get_keys()
        self.body.append(self.body[-1] + self.dir)
        self.body.pop(0)
        # wrapping around
        for prt in self.body:
            if prt.x > WIDTH:
                prt.x = 0
            elif prt.x <0:
                prt.x = WIDTH - TILESIZE

            if prt.y > HEIGHT:
                prt.y = 0
            elif prt.y < 0:
                prt.y = HEIGHT - TILESIZE

    def draw(self, surf):
        for part in self.body:
            pg.draw.rect(surf, WHITE, (part.x, part.y, TILESIZE, TILESIZE))
