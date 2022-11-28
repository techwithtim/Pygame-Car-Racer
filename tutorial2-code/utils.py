import math

import pygame


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
    pygame.draw.line(win, "white", center, (x + 1000 * math.sin(radians), y + 1000 * math.cos(radians)))
    sensors_coordinates.append(center)
    sensors_coordinates.append((x + 1000 * math.sin(radians), y + 1000 * math.cos(radians)))
    radians -= math.pi / 4
    for i in range(7):
        x, y = center
        pygame.draw.line(win, "white", center, (x + 100*math.sin(radians), y + 100*math.cos(radians)))
        sensors_coordinates.append(center)
        sensors_coordinates.append((x + 1000 * math.sin(radians), y + 1000 * math.cos(radians)))
        radians -= math.pi/4
    return sensors_coordinates
