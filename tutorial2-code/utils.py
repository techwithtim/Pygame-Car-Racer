import math
import numpy as np
import pygame


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


def crossover(_nn1, _nn2, _ratio, _repetitions, bias=False):
    if _ratio == 0:
        nnn = (2 * np.random.rand(len(_nn1), len(_nn1[0])) - 1)
        return nnn
    # if _last_ratio == _ratio and False:
    #     print("REPETITION")
    #     # mutation_rate = 0.3
    # else:
    mutation_rate = 0.1

    nnn = np.zeros((len(_nn1), len(_nn1[0])))
    for y in range(len(_nn1[0])):
        for x in range(len(_nn1)):
            if _repetitions >= 5:
                print("MUTATION RATE IS 0.6")
                mutation_rate = 0.6
            mutation = np.random.uniform((-1)*mutation_rate, mutation_rate)
            nnn[x][y] = _ratio*_nn1[x][y] + (1-_ratio) * (_nn2[x][y]) + mutation
            if not -2 <= nnn[x][y] <= 2 and not bias:
                nnn[x][y] = min(nnn[x][y], 2)
                nnn[x][y] = max(nnn[x][y], -2)

    return nnn

