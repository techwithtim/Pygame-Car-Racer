import settings
import numpy
import pygame
import numpy as np
import math
import pandas as pd
from utils import *
from AbstractCar import *


def draw(_win, _player_cars):
    _win.fill("black")
    for bonus_line in settings.BONUS_LINES:
        pygame.draw.line(settings.WIN, (0, 255, 255), *bonus_line)
    i = 1
    for track_line in settings.TRACK_LINES:
        i += 1
        pygame.draw.line(settings.WIN, (max(0, 255-i*10), 200, min(255, i * 10)), *track_line)

    for __car in _player_cars:
        __car.draw(_win)
    pygame.display.update()


run = True

clock = pygame.time.Clock()


def create_next_generation(_car_scores_and_values):
    _car_array = []
    if len(_car_scores_and_values) <= 1:
        return None
    top_scores_array = []
    top_values_array = []
    top_score, top_values = _car_scores_and_values.pop(0)

    for car in _car_scores_and_values:
        score, values = car
        if score > top_score:
            top_score = score
    if top_score <= 0:
        pass
    else:
        for car in _car_scores_and_values:
            score, values = car
            if score - 100 < top_score:
                top_score = score
                top_values_array.append(values)
                top_scores_array.append(score)

    _car_array.append(PlayerCar(settings.MAX_VEL, settings.ROTATION_VEL, *top_values_array[0]))
    for i in range(settings.NUM_OF_RANDOM_CARS_IN_GENERATION):
        _car_array.append(PlayerCar(settings.MAX_VEL, settings.ROTATION_VEL))

    values_for_next_generation = crossover(top_values_array, top_scores_array)

    for value in values_for_next_generation:

        _car_array.append(PlayerCar(settings.MAX_VEL, settings.ROTATION_VEL, *value))

    return _car_array


car_array = []

for j in range(1, 8):
    temp = PlayerCar(settings.MAX_VEL, settings.ROTATION_VEL)
    car_array.append(temp)
runs = 0
car_scores_and_values = []
generations = 0

copy_of_car_array = []

best_of_all_generation = (0, [])
last_ratio = 0
num_of_bonus_lines_hit = 1

while run:
    clock.tick(settings.FPS)
    pygame.display.update()
    draw(settings.WIN, car_array)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            _car = copy_of_car_array[0]
            # _car.print_model()
            _car.save_model()
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            pygame.draw.circle(settings.WIN, (0, 255, 0), pos, 2)
            print(pos)
    if len(car_array) != 0:
        runs += 1
        for c in car_array:
            c.score -= 10
            c.take_action()
            for point in c.points_sensor:
                if point is not None:
                    pygame.draw.circle(settings.WIN, *point)
            pygame.display.update()
            if c.collide() or runs >= 120 + 20 * (c.index_of_next_bonus_line + c.rounds_completed *
                                                  len(settings.BONUS_LINES)):
                if runs >= 120 + 20 * (c.index_of_next_bonus_line + c.rounds_completed *
                                       len(settings.BONUS_LINES)):
                    c.crash(500)
                car_scores_and_values.append((c.score, (c.weights_input_layer, c.bias_input_layer,
                                                        c.weights_l1, c.bias_l1)))
                c.reset()
                car_array.remove(c)
            else:
                rect = c.img.get_rect(topleft=(c.x, c.y))
                if rect.clipline(c.next_bonus_line):
                    if c.index_of_next_bonus_line >= len(settings.BONUS_LINES) - 1:
                        c.index_of_next_bonus_line = -1

                        c.rounds_completed += 1
                    # print("BONUS!")
                    c.score += 1000
                    c.index_of_next_bonus_line += 1
                    if c.index_of_next_bonus_line > num_of_bonus_lines_hit:
                        num_of_bonus_lines_hit = c.index_of_next_bonus_line
                    c.next_bonus_line = settings.BONUS_LINES[c.index_of_next_bonus_line]

    else:

        if not runs <= 200 + 20 * num_of_bonus_lines_hit:
            print("THEY DIED OF OLD AGE ;-;")
        elif len(car_array) == 0:
            print("They all CRUSHED TO DEATHH!!")

        for _c in car_array:
            car_scores_and_values.append((_c.score, (_c.weights_input_layer, _c.bias_input_layer, _c.weights_l1, _c.bias_l1)))
            _c.reset()

        car_array = create_next_generation(car_scores_and_values)
        copy_of_car_array = car_array.copy()
        runs = 0
        generations += 1
print(generations, "Generations")

pygame.quit()
