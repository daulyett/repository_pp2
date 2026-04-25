import pygame
import sys
import math

pygame.init()

w, h = 800, 600 # размеры
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("lab10_paint") 
clk = pygame.time.Clock()
fnt = pygame.font.SysFont("Verdana", 16) # пойдет любой шрифт

# холст
surf = pygame.Surface((w, h))
surf.fill((255, 255, 255)) 

cc = (0, 0, 0) # current color
tool = "brush" # brush, eraser, rect, circle
size = 5

flag = False 
x1, y1 = 0, 0 


colors_gui = [
    (pygame.Rect(10, 10, 30, 30), (0, 0, 0)),
    (pygame.Rect(50, 10, 30, 30), (255, 0, 0)),
    (pygame.Rect(90, 10, 30, 30), (0, 255, 0)),
    (pygame.Rect(130, 10, 30, 30), (0, 0, 255))
]

tools_gui = [
    (pygame.Rect(200, 10, 60, 30), "brush"),
    (pygame.Rect(270, 10, 60, 30), "eraser"),
    (pygame.Rect(340, 10, 60, 30), "rect"),
    (pygame.Rect(410, 10, 60, 30), "circle")
]

def render_ui():
    # верхняя панелька
    pygame.draw.rect(screen, (200, 200, 200), (0, 0, w, 50))
    
    # цвета
    for r, c in colors_gui:
        pygame.draw.rect(screen, c, r)
        if c == cc and tool != "eraser":
            pygame.draw.rect(screen, (255, 255, 255), r, 3) # белая рамка для выделения

    # кнопки тулзов
    for r, t in tools_gui:
        if t == tool:
            bg = (150, 150, 150) # нажато
        else:
            bg = (100, 100, 100)
        pygame.draw.rect(screen, bg, r)
        
        txt = fnt.render(t, True, (255, 255, 255))
        tr = txt.get_rect(center=r.center)
        screen.blit(txt, tr)

while 1: 
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit() 
            
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1: 
                mx, my = e.pos
                if my < 50: 
                    for r, c in colors_gui:
                        if r.collidepoint(e.pos):
                            cc = c
                            if tool == "eraser": 
                                tool = "brush" #чтобы переключалось обратно при выборе цвета
                                
                    for r, t in tools_gui:
                        if r.collidepoint(e.pos):
                            tool = t
                else:
                    flag = True
                    x1, y1 = e.pos

        elif e.type == pygame.MOUSEBUTTONUP:
            if e.button == 1 and flag:
                flag = False
                x2, y2 = e.pos
                
                if tool == "rect":
                    rw = x2 - x1
                    rh = y2 - y1
                    pygame.draw.rect(surf, cc, (x1, y1, rw, rh), size)
                
                elif tool == "circle":
                    # формула расстояния между точками 
                    rad = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5) 
                    pygame.draw.circle(surf, cc, (x1, y1), rad, size)

        elif e.type == pygame.MOUSEMOTION:
            if flag:
                if tool == "brush":
                    pygame.draw.circle(surf, cc, e.pos, size)
                elif tool == "eraser":
                    pygame.draw.circle(surf, (255, 255, 255), e.pos, size * 4) # ластик потолще

    # рендер
    screen.blit(surf, (0, 0))

    if flag:
        mx, my = pygame.mouse.get_pos()
        if tool == "rect":
            pygame.draw.rect(screen, cc, (x1, y1, mx - x1, my - y1), size)
            
        elif tool == "circle":
            r = int(((mx - x1)**2 + (my - y1)**2)**0.5)
            pygame.draw.circle(screen, cc, (x1, y1), r, size)

    render_ui()
    pygame.display.update()
    clk.tick(120)