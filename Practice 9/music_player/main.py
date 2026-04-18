import pygame
from player import MusicPlayer

pygame.init()
pygame.mixer.init()

WIDTH = 800
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont("Arial", 32)
small_font = pygame.font.SysFont("Arial", 24)

player = MusicPlayer()

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next_track()
            elif event.key == pygame.K_b:
                player.previous_track()
            elif event.key == pygame.K_q:
                running = False

    screen.fill((255, 255, 255))

    title_text = font.render("Music Player", True, (0, 0, 0))
    track_text = small_font.render("Current track: " + player.get_current_track_name(), True, (0, 0, 0))
    pos_text = small_font.render("Position: " + str(player.get_position()) + " sec", True, (0, 0, 0))
    controls_text = small_font.render("P=Play  S=Stop  N=Next  B=Back  Q=Quit", True, (0, 0, 0))

    screen.blit(title_text, (280, 80))
    screen.blit(track_text, (180, 180))
    screen.blit(pos_text, (180, 230))
    screen.blit(controls_text, (110, 320))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()