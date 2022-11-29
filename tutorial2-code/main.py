import pygame
import numpy as np
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
        self.index_of_bonus_line = 0
        self.next_bonus_line = BONUS_LINES[self.index_of_bonus_line]
        self.sensors = []
        self.input_layer = []
        self.points_sensor = []
        self.weights_input_layer = (2 * np.random.rand(6, 8) - 1)
        self.bias_input_layer = (2 * np.random.rand(1, 6) - 1)
        self.weights_l1 = (2 * np.random.rand(6, 4) - 1).T
        self.bias_l1 = (2 * np.random.rand(1, 4) - 1).T

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
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
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
        distances = []
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
                if (max(x1, x2) < min(x3, x4)) or (min(x1, x2) > max(x3, x4)) \
                        or (max(y1, y2) < min(y3, y4)) or (min(y1, y2) > max(y3, y4)):
                    pass
                else:
                    if x1 == x2 and x3 == x4:
                        pass

                    elif x1 == x2:

                        y = int(((y4 - y3) / (x4 - x3)) * (x1 - x3) + y3)
                        if min(y1, y2) <= y <= max(y1, y2):
                            # pygame.draw.circle(WIN, (0, 255, 0), (x1, y), 5)
                            dist = math.sqrt((x1 - x3) ** 2 + (y - y3) ** 2)
                            if shortest_point is None or shortest_point > dist:
                                shortest_point = dist
                                sensed_point = ((0, 0, 255), (x1, y), 5)
                    elif x3 == x4:
                        y = int(((y2 - y1) / (x2 - x1)) * (x3 - x1) + y1)
                        if min(y3, y4) <= y <= max(y3, y4):
                            # pygame.draw.circle(WIN, ((255, 0, 0), (x3, y), 5))
                            dist = math.sqrt((x3 - x3) ** 2 + (y3 - y) ** 2)
                            if shortest_point is None or shortest_point > dist:
                                shortest_point = dist
                                sensed_point = ((255, 0, 0), (x3, y), 5)
                    else:
                        b1 = ((y2 - y1) / (x2 - x1))
                        b2 = ((y4 - y3) / (x4 - x3))
                        if b1 != b2:
                            x = ((b2 * x3 - b1 * x1 + y1 - y3) / (b2 - b1))
                            y = (y1 + b1 * (x - x1))
                            if min(y3, y4) <= y <= max(y3, y4) and min(x3, x4) <= x <= max(x3, x4) \
                                    and min(x1, x2) <= x <= max(x1, x2):
                                dist = math.sqrt((x - x3) ** 2 + (y - y3) ** 2)
                                if shortest_point is None or shortest_point > dist:
                                    shortest_point = dist
                                    sensed_point = ((0, 255, 0), (x, y), 5)
            if sensed_point is not None and shortest_point is not None:
                points.append(sensed_point)
                distances.append(shortest_point)
            else:
                points.append(None)
                distances.append(400)
        self.input_layer = distances
        self.points_sensor = points

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0
        self.index_of_bonus_line = 0
        self.next_bonus_line = BONUS_LINES[0]
        print(self.score)
        self.score = 0

    def take_action(self):

        self.input_layer = np.array(self.input_layer)
        weighted_sum_input_layer = np.dot(self.weights_input_layer, self.input_layer) + self.bias_input_layer

        input_layer_results = np.arctan(weighted_sum_input_layer)
        # print(input_layer_results, "input layer results")

        weighted_sum_layer_1 = np.dot(self.weights_l1, input_layer_results.T) + self.bias_l1
        # print(weighted_sum_layer_1, "weighted_sum_layer_1")
        output_layer = (np.arctan(weighted_sum_layer_1))

        moved = False
        decided_action = np.argmax(output_layer)
        if decided_action == 0:
            self.rotate(left=True)
        elif decided_action == 1:
            self.rotate(right=True)
        elif decided_action == 2:
            self.move_forward()
        elif decided_action == 3:
            self.move_backward()

    def update_score(self, score):
        self.score += score


class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (237, 311)

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

    for _car in player_cars:
        _car.draw(win)
    pygame.display.update()


run = True

clock = pygame.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (0, 0)),
          (FINISH, FINISH_POSITION), (TRACK_BORDER, (0, 0))]

# Creation of cars


car_array = []

for j in range(1, 10):
    temp = PlayerCar(10, 10)
    car_array.append(temp)
runs = 0
car_scores_and_values = []
while run:
    if runs <= 200:
        pass
    else:
        print(car_scores_and_values)
        car_array = []
        for j in range(1, 10):
            temp = PlayerCar(10, 10)
            car_array.append(temp)
        car_scores_and_values = []

        runs = 0

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
        c.score -= 1
        c.sense()
        c.take_action()
        for point in c.points_sensor:
            if point is not None:
                pygame.draw.circle(WIN, *point)
        pygame.display.update()
        if c.collide():
            c.crash()

            car_scores_and_values.append((c.score, (c.weights_input_layer, c.bias_input_layer,
                                                    c.weights_l1, c.bias_l1)))
            c.reset()
            car_array.remove(c)

        else:
            rect = c.img.get_rect(topleft=(c.x, c.y))
            if rect.clipline(c.next_bonus_line):
                if c.index_of_bonus_line >= len(BONUS_LINES) - 1:
                    c.index_of_bonus_line = -1
                c.score += 1000
                c.index_of_bonus_line += 1
                print("Bonus!")
                c.next_bonus_line = BONUS_LINES[c.index_of_bonus_line]
    runs += 1
    print(runs)

pygame.quit()
