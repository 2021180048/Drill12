import random
import math
import game_framework
import game_world
from pico2d import *

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0
FRAMES_PER_TIME = FRAMES_PER_ACTION * ACTION_PER_TIME

animation_names = ['Walk']

class Zombie:
    images = None

    def load_images(self):
        if Zombie.images == None:
            Zombie.images = {}
            for name in animation_names:
                Zombie.images[name] = [load_image(f"./zombie/{name} ({i}).png") for i in range(1, 11)]

    def __init__(self):
        self.x, self.y = random.randint(1600-800, 1600), 150
        self.load_images()
        self.frame = random.randint(0, 9)
        self.dir = random.choice([-1, 1])
        self.hit = 0
        self.size = 200
        self.x1, self.y1, self.x2, self.y2 = 50, 90, 50, 90


    def update(self):
        self.frame = (self.frame + FRAMES_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if self.x > 1600:
            self.dir = -1
        elif self.x < 800:
            self.dir = 1
        self.x = clamp(800, self.x, 1600)

        if self.hit == 1:
            self.size = 100
            self.y = 100
            self.x1, self.y1, self.x2, self.y2 = 20, 40, 20, 40
        elif self.hit == 2:
            game_world.remove_object(self)
        pass


    def draw(self):
        if self.dir < 0:
            Zombie.images['Walk'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, self.size, self.size)
        else:
            Zombie.images['Walk'][int(self.frame)].draw(self.x, self.y, self.size, self.size)

        draw_rectangle(*self.get_bb())  # 튜플을 풀어서 인자로 전달


    def handle_event(self, event):
        pass

    def get_bb(self):
        return self.x - self.x1, self.y - self.y1, self.x + self.x2, self.y + self.y2

    def handle_collision(self, group, other):
        if group == 'zombie:ball':
            if self.hit == 0:
                self.hit += 1
            elif self.hit == 1:
                self.hit += 1
