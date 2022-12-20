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

    top_score, top_values = _car_scores_and_values.pop(0)
    second_score, second_values = _car_scores_and_values.pop(0)

    if top_score < second_score:
        top_score += second_score
        second_score = top_score - second_score
        top_score -= second_score

        temp_values = top_values
        top_values = second_values
        second_values = temp_values
    repetitions = 0
    for car in _car_scores_and_values:
        score, values = car
        if score == top_score:
            repetitions += 1
        if score > top_score:
            top_score = score
            top_values = values
            repetitions = 0
        elif score >= second_score:
            second_score = score
            second_values = values

    if top_score <= 0:
        ratio = 0
    elif second_score <= 0:
        ratio = 1
    else:
        ratio = top_score / (top_score + second_score)

    twi, tbi, tw1, tb1 = top_values
    swi, sbi, sw1, sb1 = second_values
    max_vel = 12
    rotation_vel = 5
    _car_array.append(PlayerCar(max_vel, rotation_vel, twi, tbi, tw1, tb1))
    _car_array.append(PlayerCar(max_vel, rotation_vel, swi, sbi, sw1, sb1))

    for r in range(1, 10):
        nwi = crossover(twi, swi, ratio, repetitions)
        nbi = crossover(tbi, sbi, ratio, repetitions, bias=True)
        nw1 = crossover(tw1, sw1, ratio, repetitions)
        nb1 = crossover(tb1, sb1, ratio, repetitions, bias=True)
        _car_array.append(PlayerCar(max_vel, rotation_vel, nwi, nbi, nw1, nb1))
    _car_array.append(PlayerCar(max_vel, rotation_vel, twi, tbi, tw1, tb1))
    _last_ratio = ratio
    return _car_array, _last_ratio


car_array = []

for j in range(1, 8):
    temp = PlayerCar(100, 100)
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
            _car.print_model()
            _car.save_model()
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            pygame.draw.circle(settings.WIN, (0, 255, 0), pos, 2)
            print(pos)
    if len(car_array) != 0 and runs <= 200 + 20 * num_of_bonus_lines_hit:
        runs += 1
        for c in car_array:
            c.score -= 1
            c.sense()
            c.input_layer = np.append(c.input_layer, np.array(c.vel))
            c.take_action()
            for point in c.points_sensor:
                if point is not None:
                    pygame.draw.circle(settings.WIN, *point)
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
                    if c.index_of_bonus_line >= len(settings.BONUS_LINES) - 1:
                        c.index_of_bonus_line = -1
                    # print("BONUS!")
                    c.score += 1000
                    c.index_of_bonus_line += 1
                    if c.index_of_bonus_line > num_of_bonus_lines_hit:
                        num_of_bonus_lines_hit = c.index_of_bonus_line
                    c.next_bonus_line = settings.BONUS_LINES[c.index_of_bonus_line]

    else:

        if not runs <= 200 + 20 * num_of_bonus_lines_hit:
            print("THEY DIED OF OLD AGE ;-;")
        elif len(car_array) == 0:
            print("They all CRUSHED TO DEATHH!!")

        for _c in car_array:
            car_scores_and_values.append((_c.score, (_c.weights_input_layer, _c.bias_input_layer, _c.weights_l1, _c.bias_l1)))
            _c.reset()

        car_array, last_ratio = create_next_generation(car_scores_and_values)
        copy_of_car_array = car_array.copy()
        runs = 0
        generations += 1
print(generations)

pygame.quit()
