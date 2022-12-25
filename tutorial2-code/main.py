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
import create_road


def draw(_win, _player_cars):
    _win.fill("black")
    i = 0

    for bonus_line in settings.BONUS_LINES:

        if i % 6 == 0:
            rgb = (255,0,0)
        elif i % 6 == 1:
            rgb = (255,160,0)
        elif i % 6 == 2:
            rgb = (255,255,0)
        elif i % 6 == 3:
            rgb = (0,255,0)
        elif i % 6 == 4:
            rgb = (0,0,255)
        elif i % 6 == 5:
            rgb = (100,0,200)
        pygame.draw.line(_win, rgb, *bonus_line)
        i+=1
    i = 1

    for track_line in settings.TRACK_LINES:
        i += 1
        pygame.draw.line(_win, (max(0, 255), 200, min(255,0)), *track_line)

    for __car in _player_cars:
        __car.draw(_win)
    pygame.display.update()


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

    win = pygame.display.set_mode(settings.WIN_SHAPE)
    while run:
        # print("buya", len(cars))
        clock.tick(settings.FPS)
        pygame.display.update()
        draw(win, cars)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                pygame.draw.circle(win, (0, 255, 0), pos, 2)
                print(pos)
        if len(cars) != 0:
            runs += 1
            for x, car in enumerate(cars):

                ge[x].fitness -= 1

                car.update_input_layer()
                output = nets[x].activate(car.input_layer)
                car.take_action(output)
                car.move()
                for point in car.points_sensor:
                    if point is not None:
                        pygame.draw.circle(win, *point)
                pygame.display.update()
                if car.collide() or runs >= 100 + 40 * car.index_of_bonus_line +\
                        18 * car.rounds_completed * len(settings.BONUS_LINES):

                    ge[x].fitness -= 5000

                    cars.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                else:
                    rect = car.img.get_rect(topleft=(car.x, car.y))
                    if rect.clipline(car.next_bonus_line):
                        if car.index_of_bonus_line >= len(settings.BONUS_LINES) - 2:
                            car.rounds_completed += 1
                            car.index_of_bonus_line = 0
                        # print("BONUS!")
                        ge[x].fitness += 1000
                        car.index_of_bonus_line += 1
                        car.next_bonus_line = settings.BONUS_LINES[car.index_of_bonus_line]
                        # print("this is my next bonus line,", car.next_bonus_line)

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
    track_lines, bonus_lines, starting_position, win_size = create_road.main()
    settings.TRACK_LINES = track_lines
    settings.BONUS_LINES = bonus_lines
    settings.STARTING_POSITION = starting_position
    print("win size", win_size)
    settings.WIN_SHAPE = win_size
    print("starting position", starting_position)
    print("bonus lines", settings.BONUS_LINES)

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
