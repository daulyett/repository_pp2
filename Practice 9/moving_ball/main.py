import pygame
from ball import Ball

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")

clock = pygame.time.Clock()

ball = Ball(
    x=WIDTH // 2,
    y=HEIGHT // 2,
    radius=25,
    step=20,
    screen_width=WIDTH,
    screen_height=HEIGHT
)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ball.move_up()
            elif event.key == pygame.K_DOWN:
                ball.move_down()
            elif event.key == pygame.K_LEFT:
                ball.move_left()
            elif event.key == pygame.K_RIGHT:
                ball.move_right()

    screen.fill((255, 255, 255))
    ball.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()