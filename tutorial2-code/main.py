import pygame
import time
import math
from utils import scale_image, blit_rotate_center

GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("imgs/track.png"), 0.9)

TRACK_BORDER = scale_image(pygame.image.load("imgs/track-border.png"), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = pygame.image.load("imgs/finish.png")
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (130, 250)

RED_CAR = scale_image(pygame.image.load("imgs/red-car.png"), 0.45)
GREEN_CAR = scale_image(pygame.image.load("imgs/green-car.png"), 0.55)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")

FPS = 60


class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1
        self.score = 0
        self.sensors = []

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    # def draw_sensor(self, win):
    #     for i in range(8):
    #         rect = self.img.get_rect
    #         print(rect)
    #         pygame.draw.line(win, "black", center, (0,0))

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0

    def update_score(self, score):
        self.score += score

class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (180, 200)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()

    def crash(self):
        self.score -= 500


def draw(win, images, player_cars):
    for img, pos in images:
        win.blit(img, pos)
    for car in player_cars:
        car.draw(win)
        # car.draw_sensor(win)

    pygame.display.update()


def move_car(c):  # player_car
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        c.rotate(left=True)
    if keys[pygame.K_d]:
        c.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        c.move_forward()
    if keys[pygame.K_s]:
        moved = True
        c.move_backward()

    if not moved:
        c.reduce_speed()


run = True
clock = pygame.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (0, 0)),
          (FINISH, FINISH_POSITION), (TRACK_BORDER, (0, 0))]
# player_car = PlayerCar(8, 8)

# Creation of cars
car_array = []
for i in range(1, 3):
    temp = PlayerCar(i, i)
    car_array.append(temp)


while run:
    clock.tick(FPS)

    draw(WIN, images, car_array)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    for cars in car_array:
        move_car(cars)
    # print(player_car.score)
    for car in car_array:
        if car.collide(TRACK_BORDER_MASK) != None:
            car.crash()
            car.reset()

        finish_poi_collide = car.collide(FINISH_MASK, *FINISH_POSITION)
        if finish_poi_collide != None:
            if finish_poi_collide[1] == 0:
                car.bounce()
            else:
                car.score += 1000
                print("finish")


pygame.quit()
