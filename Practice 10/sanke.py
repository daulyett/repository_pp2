import pygame, random, sys

pygame.init()

cs = 20 # cell size
w = 30
h = 20

screen = pygame.display.set_mode((w * cs, h * cs))
pygame.display.set_caption("lab10")
clk = pygame.time.Clock()
fnt = pygame.font.SysFont("Verdana", 16)

# змейка будет списком списков
zmeika = [[15, 10], [14, 10]]
dx, dy = 1, 0 
ndx, ndy = 1, 0 # next dir

sc = 0
lvl = 1

def make_eda():
    while 1:
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)
        if [x, y] not in zmeika:
            return [x, y]

eda = make_eda()

while 1:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP and dy != 1:
                ndx, ndy = 0, -1
            elif e.key == pygame.K_DOWN and dy != -1:
                ndx, ndy = 0, 1
            elif e.key == pygame.K_LEFT and dx != 1:
                ndx, ndy = -1, 0
            elif e.key == pygame.K_RIGHT and dx != -1:
                ndx, ndy = 1, 0

    dx, dy = ndx, ndy

    hx, hy = zmeika[0]
    nx, ny = hx + dx, hy + dy

    # стены
    if nx < 0 or nx >= w or ny < 0 or ny >= h:
        break 

    # съели себя
    if [nx, ny] in zmeika:
        break 

    zmeika.insert(0, [nx, ny])

    if [nx, ny] == eda:
        sc += 1
        if sc % 4 == 0:
            lvl += 1
        eda = make_eda()
    else:
        zmeika.pop()

    screen.fill((0, 0, 0))

    # еда
    pygame.draw.rect(screen, (255, 0, 0), (eda[0] * cs, eda[1] * cs, cs, cs))

    # змея
    for s in zmeika:
        pygame.draw.rect(screen, (0, 255, 0), (s[0] * cs, s[1] * cs, cs, cs))

    txt_sc = fnt.render(f"Score: {sc}", True, (255, 255, 255))
    txt_lvl = fnt.render(f"Level: {lvl}", True, (255, 255, 255))
    
    #(ширина окна) - (ширина текста) - 10 пикселей отступа
    screen.blit(txt_sc, (10, 10))
    screen.blit(txt_lvl, ((w * cs) - txt_lvl.get_width() - 10, 10)) 

    pygame.display.update()
    clk.tick(8 + (lvl * 2)) # скорость растет с уровнем

# если проиграли
screen.fill((0, 0, 0))
f2 = pygame.font.SysFont("Verdana", 40)
msg = f2.render("GAME OVER", True, (255, 0, 0))

#середина экрана минус половина текста
cx = (w * cs) // 2 - msg.get_width() // 2
cy = (h * cs) // 2 - msg.get_height() // 2

screen.blit(msg, (cx, cy)) 
pygame.display.update()

pygame.time.wait(2000)
sys.exit()