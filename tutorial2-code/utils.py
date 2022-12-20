import copy
import math
import numpy as np
import pygame
import settings

def relu(_w):
    return np.maximum(0, _w)


def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)


def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)


def draw_sensors(win, img, top_left, angle):
    sensors_coordinates = []
    center = img.get_rect(topleft=top_left).center
    while angle < 0:
        angle += 360
    angle += 180
    radians = math.radians(angle)
    x, y = center
    sensor_length = 250
    sensor_length_multiplaier = 2
    pygame.draw.line(win, "white", center, (x + sensor_length_multiplaier * sensor_length * math.sin(radians), y + sensor_length_multiplaier * sensor_length * math.cos(radians)))
    sensors_coordinates.append((center, (x + sensor_length_multiplaier * sensor_length * math.sin(radians), y + sensor_length_multiplaier * sensor_length * math.cos(radians))))
    # sensors_coordinates.append((x + 1000 * math.sin(radians), y + 1000 * math.cos(radians)))
    radians -= math.pi / 4
    for i in range(7):
        pygame.draw.line(win, "white", center, (x + sensor_length*math.sin(radians), y + sensor_length*math.cos(radians)))
        sensors_coordinates.append((center,(x + sensor_length * math.sin(radians), y + sensor_length * math.cos(radians))))
        # sensors_coordinates.append()
        radians -= math.pi/4
    return sensors_coordinates


def crossover(_top_values, _top_scores):
    values_for_next_generation = []
    counter = 0
    num_of_cars = len(_top_scores)
    first_value = _top_values.pop()
    for i in range(len(_top_values)):
        j = 0
        for net in _top_values[i]:
            for y in range(len(net[0])):
                for x in range(len(net)):
                    first_value[j][x][y] += net[x][y]

            j += 1
    mutation_rate = 0.1
    temp = copy.deepcopy(first_value)
    for i in range(settings.NUM_OF_MUTATIONS):
        j = 0
        for net in first_value:
            for y in range(len(net[0])):
                for x in range(len(net)):

                    mutation = np.random.uniform((-1) * mutation_rate, mutation_rate)
                    net[x][y] = net[x][y] / num_of_cars + mutation
                    if counter % 2 == 0 and not -2 <= net[x][y] <= 2:  # weight
                        net[x][y] = min(net[x][y], 2)
                        net[x][y] = max(net[x][y], -2)
            j += 1
            counter += 1
        values_for_next_generation.append(first_value)
        first_value = temp

    return values_for_next_generation

