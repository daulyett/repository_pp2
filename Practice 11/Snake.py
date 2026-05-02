import pygame, random, sys

pygame.init()

cs = 20
w, h = 30, 20
screen = pygame.display.set_mode((w * cs, h * cs))
pygame.display.set_caption("lab11_zmeika_hardcore")
clk = pygame.time.Clock()
fnt = pygame.font.SysFont("Verdana", 16)

zmeika = [[15, 10], [14, 10]]
dx, dy = 1, 0 
ndx, ndy = 1, 0 

sc = 0
lvl = 1

def make_eda():
    while 1:
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)
        if [x, y] not in zmeika:
            # вес: 1 или 3. Таймер: 100 кадров или 50 кадров
            weight = random.choice([1, 1, 3]) 
            timer = 100 if weight == 1 else 50
            return [x, y, weight, timer]

eda = make_eda()

while 1:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP and dy != 1: ndx, ndy = 0, -1
            elif e.key == pygame.K_DOWN and dy != -1: ndx, ndy = 0, 1
            elif e.key == pygame.K_LEFT and dx != 1: ndx, ndy = -1, 0
            elif e.key == pygame.K_RIGHT and dx != -1: ndx, ndy = 1, 0

    dx, dy = ndx, ndy
    nx, ny = zmeika[0][0] + dx, zmeika[0][1] + dy

    if nx < 0 or nx >= w or ny < 0 or ny >= h or [nx, ny] in zmeika:
        break 

    zmeika.insert(0, [nx, ny])

    # таймер еды
    eda[3] -= 1
    if eda[3] <= 0:
        eda = make_eda() # протухла, спавним новую

    # логика поедания
    if nx == eda[0] and ny == eda[1]:
        sc += eda[2] # прибавляем вес
        if sc // 4 + 1 > lvl: # костыль для левелапа
            lvl += 1
        eda = make_eda()
    else:
        zmeika.pop()

    screen.fill((0, 0, 0))

    # отрисовка еды (красная = 1, синяя = 3)
    eda_color = (255, 0, 0) if eda[2] == 1 else (0, 150, 255)
    pygame.draw.rect(screen, eda_color, (eda[0] * cs, eda[1] * cs, cs, cs))
    
    # мигание еды когда таймер кончается (чисто шоб красиво было)
    if eda[3] < 20 and eda[3] % 2 == 0:
        pygame.draw.rect(screen, (0, 0, 0), (eda[0] * cs, eda[1] * cs, cs, cs))

    for s in zmeika:
        pygame.draw.rect(screen, (0, 255, 0), (s[0] * cs, s[1] * cs, cs, cs))

    txt_sc = fnt.render(f"Score: {sc}", True, (255, 255, 255))
    txt_lvl = fnt.render(f"Level: {lvl}", True, (255, 255, 255))
    
    screen.blit(txt_sc, (10, 10))
    screen.blit(txt_lvl, ((w * cs) - txt_lvl.get_width() - 10, 10)) 

    pygame.display.update()
    clk.tick(8 + (lvl * 2))

screen.fill((0, 0, 0))
f2 = pygame.font.SysFont("Verdana", 40)
msg = f2.render("GAME OVER", True, (255, 0, 0))
screen.blit(msg, ((w * cs) // 2 - msg.get_width() // 2, (h * cs) // 2 - msg.get_height() // 2)) 
pygame.display.update()
pygame.time.wait(2000)
sys.exit()