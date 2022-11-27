import math

import pygame


def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)


def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    center = new_rect.center
    while angle < 0:
        angle += 360
    radians = math.radians(angle)

    for i in range(8):
        x, y = center
        pygame.draw.line(win, "Black", center, (x + 100*math.sin(radians), y + 100*math.cos(radians)))
        radians -= math.pi/4
    win.blit(rotated_image, new_rect.topleft)
