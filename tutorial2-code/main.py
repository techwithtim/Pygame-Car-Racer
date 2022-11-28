import pygame
import time
import math
from utils import scale_image, blit_rotate_center, draw_sensors

GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("imgs/track.png"), 0.9)

TRACK_LINES = [((35, 130), (35, 650)),
    ((35, 650), (160, 770)),
    ((160, 770), (670, 770)),
    ((670, 770), (760, 640)),
    ((760, 640), (760, 110)),
    ((760, 110), (670, 20)),
    ((670, 20), (430, 20)),
    ((170, 200), (170, 600)),
    ((170, 600), (240, 660)),
    ((240, 660), (580, 670)),
    ((580, 670), (660, 590)),
    ((660, 590), (660, 190)),
    ((35, 130), (130, 20)),
    ((130, 20), (220, 20)),
    ((220, 20), (300, 110)),
    ((300, 110), (300, 510)),
    ((430, 20), (370, 90)),
    ((370, 90), (370, 180)),
    ((370, 180), (420, 240)),
    ((420, 240), (500, 240)),
    ((660, 190), (620, 130)),
    ((620, 130), (500, 130)),
    ((500, 240), (560, 300)),
    ((560, 300), (560, 510)),
    ((560, 510), (500, 560)),
    ((500, 560), (330, 560)),
    ((330, 560), (300, 510))]

BONUS_LINES = [

((173, 216),(296, 219)),
    ((171, 201),(299, 112)),

    ((170, 200),(175, 20)),
    ((39, 131),(168, 202)),
    ((40, 250),(167, 250)),
    ((167, 326),(38, 321)),
    ((37, 427),(165, 427)),
    ((167, 558),(37, 559)),
    ((190, 621),(100, 708)),
    ((249, 662),(252, 769)),
    ((344, 666),(347, 764)),


((420, 667),(434, 764)),
((535, 673),(548, 767)),
((582, 672),(671, 768)),
((627, 626),(717, 692)),
((660, 590),(760, 641)),
((662, 502),(762, 501)),
((662, 402),(754, 405)),
((660, 313),(763, 306)),
((661, 224),(759, 218)),
((662, 189),(758, 106)),
((715, 67),(640, 159)),
((621, 130),(669, 25)),
((588, 22),(583, 126)),



     ((498, 129),(488, 25)),
     ((374, 91),(501, 132)),
     ((420, 242),(498, 133)),
     ((528, 264),(633, 158)),
     ((561, 304),(657, 286)),
     ((566, 369),(660, 366)),




     ((561, 439),(658, 444)),
     ((563, 510),(658, 523)),
     ((534, 541),(620, 623)),
     ((464, 567),(465, 660)),
     ((354, 564),(356, 659)),
     ((316, 545),(212, 627)),
     ((174, 503),(297, 496)),
     ((294, 414),(170, 405))]


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
        self.sensors = draw_sensors(win, self.img, (self.x, self.y), self.angle)

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

    def collide(self):
        car_rect = self.img.get_rect(x=self.x, y=self.y)
        for line in TRACK_LINES:
            if car_rect.clipline(line):
                return True
        return False

        # if car_rect.clipline((1,1),(800,200)):
        #     print("BOOM")
        # car_mask = pygame.mask.from_surface(self.img)
        # offset = (int(self.x - x), int(self.y - y))
        # check collision with lines
        # poi = mask.overlap(car_mask, offset)

    def sense(self, win):
        # print(TRACK_BORDER_MASK.outline())
            # pygame.draw.circle(win,"black", point, 15)
        # for point in *TRACK_BORDER_MASK.outline():
        # pygame.draw.lines(win, "Pink", *TRACK_BORDER_MASK.outline())
        for i in range(0, len(self.sensors), 2):
            # print(self.sensors[i])
            # print(self.sensors[i+1])
            pass

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0

    def update_score(self, score):
        self.score += score


class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (240, 310)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()

    def crash(self):
        self.score -= 500


def draw(win, player_cars):
    win.fill("black")
    for bonus_line in BONUS_LINES:
        pygame.draw.line(WIN, ((0,255,255)), *bonus_line)
    for track_line in TRACK_LINES:
        pygame.draw.line(WIN, ((200, 200, 200)), *track_line)

    for car in player_cars:
        car.draw(win)
        # print(TRACK_BORDER_MASK.overlap_area(car.sensors))
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
for i in range(1, 2):
    temp = PlayerCar(i+5, i+5)
    car_array.append(temp)

while run:
    clock.tick(FPS)

    pygame.display.update()
    draw(WIN, car_array)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            pygame.draw.circle(WIN, (0,255,0) , pos, 2)
            print(pos)

    for cars in car_array:
        move_car(cars)
        cars.sense(WIN)

    for car in car_array:
        if car.collide():
            car.crash()
            car.reset()
        finish_poi_collide = None
        # finish_poi_collide = car.collide(FINISH_MASK, *FINISH_POSITION)
        if finish_poi_collide != None:
            if finish_poi_collide[1] == 0:
                car.bounce()
            else:
                car.score += 1000
                print("finish")

pygame.quit()
