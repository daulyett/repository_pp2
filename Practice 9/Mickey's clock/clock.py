import pygame
import datetime
import os

BASE_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(BASE_DIR, "images")

base = pygame.image.load(os.path.join(IMAGES_DIR, "base.png")).convert_alpha()
minute_hand = pygame.image.load(os.path.join(IMAGES_DIR, "minute_hand.png")).convert_alpha()
second_hand = pygame.image.load(os.path.join(IMAGES_DIR, "second_hand.png")).convert_alpha()

WIDTH = 800
HEIGHT = 600
CENTER = (400, 300)


MINUTE_OFFSET_X = 0
MINUTE_OFFSET_Y = 0

SECOND_OFFSET_X = 0
SECOND_OFFSET_Y = 0


MINUTE_ANGLE_OFFSET = 54.5   
SECOND_ANGLE_OFFSET = -60.8  

def draw_clock(screen):
    now = datetime.datetime.now()
    minutes = now.minute + now.second / 60
    seconds = now.second

    minute_angle = -(minutes * 6) + MINUTE_ANGLE_OFFSET
    second_angle = -(seconds * 6) + SECOND_ANGLE_OFFSET

    rotated_minute = pygame.transform.rotate(minute_hand, minute_angle)
    rotated_second = pygame.transform.rotate(second_hand, second_angle)

    base_rect = base.get_rect(center=CENTER)
    minute_rect = rotated_minute.get_rect(
        center=(CENTER[0] + MINUTE_OFFSET_X, CENTER[1] + MINUTE_OFFSET_Y)
    )
    second_rect = rotated_second.get_rect(
        center=(CENTER[0] + SECOND_OFFSET_X, CENTER[1] + SECOND_OFFSET_Y)
    )

    screen.fill((255, 255, 255))
    screen.blit(base, base_rect)
    screen.blit(rotated_minute, minute_rect)
    screen.blit(rotated_second, second_rect)