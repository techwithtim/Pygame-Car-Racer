import os

import neat.config

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


def main(genomes, config):
    nets = []
    ge = []
    cars = []
    # _car_array.append(PlayerCar(max_vel, rotation_vel, twi, tbi, tw1, tb1))

    for _, g in genomes:
        # print("bazinga")
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        cars.append(PlayerCar(settings.MAX_VEL, settings.ROTATION_VEL))
        g.fitness = 0
        ge.append(g)

    run = True

    clock = pygame.time.Clock()



    runs = 0
    car_scores_and_values = []
    generations = 0

    copy_of_car_array = []

    best_of_all_generation = (0, [])
    last_ratio = 0
    num_of_bonus_lines_hit = 1

    while run:
        # print("buya", len(cars))
        clock.tick(settings.FPS)
        pygame.display.update()
        draw(settings.WIN, cars)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                pygame.draw.circle(settings.WIN, (0, 255, 0), pos, 2)
                print(pos)
        if len(cars) != 0:
            runs += 1
            for x, car in enumerate(cars):
                if runs%60 ==59:
                    car.print_input_layer()
                ge[x].fitness += 1

                car.update_input_layer()
                output = nets[x].activate(car.input_layer)
                car.take_action(output)
                car.move()
                for point in car.points_sensor:
                    if point is not None:
                        pygame.draw.circle(settings.WIN, *point)
                pygame.display.update()
                if car.collide() or runs >= 40 + 18 * car.index_of_bonus_line + 18 * car.rounds_completed * len(settings.BONUS_LINES):
                    if car.rounds_completed !=0:
                        print(40 + 18 * car.index_of_bonus_line +
                        car.rounds_completed * len(settings.BONUS_LINES))
                    ge[x].fitness -= 10000

                    cars.pop(x)
                    nets.pop(x)
                    ge.pop(x) #בייייייייייייייייייייייייייייייייייייייב תפסיק לתכנת

                else:
                    rect = car.img.get_rect(topleft=(car.x, car.y))
                    if rect.clipline(car.next_bonus_line):
                        if car.index_of_bonus_line >= len(settings.BONUS_LINES) - 2:
                            car.rounds_completed += 1
                            print("round completed")
                            car.index_of_bonus_line = 0
                        # print("BONUS!")
                        ge[x].fitness += 1000
                        car.index_of_bonus_line += 1
                        car.next_bonus_line = settings.BONUS_LINES[car.index_of_bonus_line]

        else:
            break


def run(_config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet
                                , neat.DefaultStagnation, _config_path)
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 1000)
    print(winner, "winner")


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
