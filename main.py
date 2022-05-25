import pygame as pg
import sys
from settings import *
from objects import *
import random
import math
from os import path
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        self.font=path.join("PixelatedRegular-aLKm.ttf")
    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.snake = Snake(((WIDTH//TILESIZE//2)*TILESIZE,(HEIGHT//TILESIZE//2)*TILESIZE))
        self.columns = WIDTH//TILESIZE
        self.rows = HEIGHT//TILESIZE
        self.food = Food((random.randint(0,self.columns-1) * TILESIZE, random.randint(0, self.rows-1) * TILESIZE))


    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def dist(self, vec1, vec2):
        return math.sqrt((vec2.x - vec1.x)**2 + (vec2.y - vec1.y)**2)

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.snake.update()
        # food eating
        if self.dist(self.snake.body[-1]+(TILESIZE//2, TILESIZE//2), self.food.pos+(TILESIZE//2, TILESIZE//2)) < TILESIZE:
            self.snake.body.insert(-1,self.food.pos)
            self.food.pos = vec((random.randint(0,self.columns-1) * TILESIZE, random.randint(0, self.rows-1) * TILESIZE))

        # biting self
        for p in self.snake.body[:-2]:
            if self.dist(self.snake.body[-1] + (TILESIZE // 2, TILESIZE // 2), p + (TILESIZE // 2, TILESIZE // 2)) < TILESIZE:
                self.snake.body = [self.snake.body[-1]]

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        #self.all_sprites.draw(self.screen)
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        # fps
        self.draw_text(str(int(self.clock.get_fps())), self.font, 40, WHITE, 50, 50, align="center")
        self.draw_text(f"LENGTH: {len(self.snake.body)}", self.font, 40, WHITE, WIDTH//2, 50, align="center")
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                



# create the game object
g = Game()
g.new()
g.run()
