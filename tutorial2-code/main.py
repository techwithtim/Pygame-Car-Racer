import pygame
import time
import math
from utils import scale_image, blit_rotate_center, draw_sensors

GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("imgs/track.png"), 0.9)

TRACK_LINES = [((35, 130), (35, 650)), ((35, 650), (160, 770)), ((160, 770), (670, 770)), ((670, 770), (760, 640)),
               ((760, 640), (760, 110)), ((760, 110), (670, 20)), ((670, 20), (430, 20)), ((170, 200), (170, 600)),
               ((170, 600), (240, 660)), ((240, 660), (580, 670)), ((580, 670), (660, 590)), ((660, 590), (660, 190)),
               ((35, 130), (130, 20)), ((130, 20), (220, 20)), ((220, 20), (300, 110)), ((300, 110), (300, 510)),
               ((430, 20), (370, 90)), ((370, 90), (370, 180)), ((370, 180), (420, 240)), ((420, 240), (500, 240)),
               ((660, 190), (620, 130)), ((620, 130), (500, 130)), ((500, 240), (560, 300)), ((560, 300), (560, 510)),
               ((560, 510), (500, 560)), ((500, 560), (330, 560)), ((330, 560), (300, 510))]

BONUS_LINES = [((173, 216), (296, 219)), ((171, 201), (299, 112)), ((170, 200), (175, 20)), ((39, 131), (168, 202)),
               ((40, 250), (167, 250)), ((167, 326), (38, 321)), ((37, 427), (165, 427)), ((167, 558), (37, 559)),
               ((190, 621), (100, 708)), ((249, 662), (252, 769)), ((344, 666), (347, 764)), ((420, 667), (434, 764)),
               ((535, 673), (548, 767)), ((582, 672), (671, 768)), ((627, 626), (717, 692)), ((660, 590), (760, 641)),
               ((662, 502), (762, 501)), ((662, 402), (754, 405)), ((660, 313), (763, 306)), ((661, 224), (759, 218)),
               ((662, 189), (758, 106)), ((715, 67), (640, 159)), ((621, 130), (669, 25)), ((588, 22), (583, 126)),
               ((498, 129), (488, 25)), ((374, 91), (501, 132)), ((420, 242), (498, 133)), ((528, 264), (633, 158)),
               ((561, 304), (657, 286)), ((566, 369), (660, 366)), ((561, 439), (658, 444)), ((563, 510), (658, 523)),
               ((534, 541), (620, 623)), ((464, 567), (465, 660)), ((354, 564), (356, 659)), ((316, 545), (212, 627)),
               ((174, 503), (297, 496)), ((294, 414), (170, 405))]


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
        self.index_of_bonus_line = 0
        self.next_bonus_line = BONUS_LINES[self.index_of_bonus_line]

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

    def sense(self):
        points = []
        for sensor in self.sensors:
            sensed_point = None
            shortest_point = None
            for track_line in TRACK_LINES:

                (x1, y1), (x2, y2) = track_line
                (x3, y3), (x4, y4) = sensor
                x1 = int(round(x1))
                x2 = int(round(x2))
                x3 = int(round(x3))
                x4 = int(round(x4))
                y1 = int(round(y1))
                y2 = int(round(y2))
                y3 = int(round(y3))
                y4 = int(round(y4))
                if (max(x1, x2) < min(x3, x4)) or (min(x1, x2) > max(x3, x4)) or (max(y1, y2) < min(y3, y4)) or (min(y1, y2) > max(y3, y4)):
                    pass
                else:
                    if x1 == x2 and x3 == x4:
                        pass

                    elif x1 == x2:

                        y = int(((y4-y3)/(x4-x3)) * (x1 - x3) + y3)
                        if min(y1, y2) <= y <= max(y1, y2):
                            # pygame.draw.circle(WIN, (0, 255, 0), (x1, y), 5)
                            dist = math.sqrt((x1-x3)**2 + (y-y3)**2)
                            if shortest_point is None or shortest_point > dist:
                                shortest_point = dist
                                sensed_point = ((255, 0, 0), (x1, y), 5)
                    elif x3 == x4:
                        y = int(((y2-y1)/(x2-x1)) * (x3 - x1) + y1)
                        if min(y3, y4) <= y <= max(y3, y4):
                            # pygame.draw.circle(WIN, ((255, 0, 0), (x3, y), 5))
                            dist = math.sqrt((x3-x3)**2 + (y3-y)**2)
                            if shortest_point is None or shortest_point > dist:
                                shortest_point = dist
                                sensed_point = ((255, 0, 0), (x3, y), 5)
                    else:
                        b1 = ((y2-y1)/(x2-x1))
                        b2 = ((y4-y3)/(x4-x3))
                        if b1 != b2:
                            x = ((b2*x3 - b1*x1 + y1 - y3) / (b2 - b1))
                            y = (y1 + b1 * (x - x1))
                            if min(y3, y4) <= y <= max(y3, y4) and min(x3, x4) <= x <= max(x3, x4) and min(x1, x2) <= x <= max(x1, x2):
                                dist = math.sqrt((x-x3)**2 + (y3-y)**2)
                                if shortest_point is None or shortest_point > dist:
                                    sensed_point = ((255, 0, 0), (x, y), 5)
            if sensed_point is not None:
                points.append(sensed_point)
        return points

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0
        self.index_of_bonus_line = 0
        self.next_bonus_line = BONUS_LINES[0]
        print(self.score)
        self.score = 0

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
        pygame.draw.line(WIN, (0, 255, 255), *bonus_line)
    for track_line in TRACK_LINES:
        pygame.draw.line(WIN, (200, 200, 200), *track_line)

    for c in player_cars:
        c.draw(win)
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
            pygame.draw.circle(WIN, (0, 255, 0), pos, 2)
            print(pos)

    for c in car_array:
        c.score-=1
        move_car(c)
        points_sensor = c.sense()
        for point in points_sensor:
            pygame.draw.circle(WIN, *point)
        pygame.display.update()

        if c.collide():
            c.crash()
            c.reset()
        # finish_poi_cowllide = car.collide(FINISH_MASK, *FINISH_POSITION)
        rect = c.img.get_rect(topleft=(c.x, c.y))
        if rect.clipline((c.next_bonus_line)):
            if c.index_of_bonus_line >= len(BONUS_LINES) - 1:
                c.index_of_bonus_line = -1
            c.score += 1000
            c.index_of_bonus_line+=1
            print("Bonus!")
            c.next_bonus_line = BONUS_LINES[c.index_of_bonus_line]

pygame.quit()
