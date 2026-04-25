import pygame, random, sys
from pygame.locals import *

pygame.init()

#400x600
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("lab10_1")
clk = pygame.time.Clock()

f1 = pygame.font.SysFont("Verdana", 20)
f2 = pygame.font.SysFont("Verdana", 60)

spd = 5
sc = 0
monetki = 0
timer = 0 # таймер для скорости 

class Vrag(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 60))
        self.image.fill((255, 0, 0)) # красный
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, 360), 0)

    def move(self):
        global sc
        self.rect.move_ip(0, spd) 
        
        # если уехал вниз
        if self.rect.top > 600:
            sc += 1 # халявные очки
            self.rect.top = 0
            self.rect.center = (random.randint(40, 360), 0)

class Ya(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 60))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520) 

    def move(self):
        k = pygame.key.get_pressed()
        
        #cкорость 5
        if k[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)
        if k[K_RIGHT] and self.rect.right < 400:
            self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25, 25))
        self.image.fill((255, 215, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, 360), -50)

    def move(self):
        self.rect.move_ip(0, spd)
        
        if self.rect.top > 600:
            self.rect.top = -50
            self.rect.center = (random.randint(40, 360), -50)

p1 = Ya()
v1 = Vrag()
c1 = Coin()


vragi_grp = pygame.sprite.Group()
vragi_grp.add(v1)

coins_grp = pygame.sprite.Group()
coins_grp.add(c1)

all_spr = pygame.sprite.Group()
all_spr.add(p1)
all_spr.add(v1)
all_spr.add(c1)

while 1:
    for e in pygame.event.get():
        if e.type == QUIT:
            sys.exit()
            
    
    timer += 1
    if timer >= 60: # 60 кадров = 1 сек
        spd += 0.5
        timer = 0

    screen.fill((255, 255, 255))
    
    # текст
    txt1 = f1.render(f"Score: {sc}", True, (0, 0, 0))
    txt2 = f1.render(f"Coins: {monetki}", True, (0, 0, 0))
    
    screen.blit(txt1, (10, 10))
    # Считаем точный отступ: ширина экрана (400) минус ширина самого текста и минус 10 пикселей от края
    screen.blit(txt2, (400 - txt2.get_width() - 10, 10))

    for s in all_spr:
        s.move()
        screen.blit(s.image, s.rect)
        
    # монетки
    if pygame.sprite.spritecollideany(p1, coins_grp):
        monetki += 1
        c1.rect.top = -50
        c1.rect.center = (random.randint(40, 360), -50)

    # врезались
    if pygame.sprite.spritecollideany(p1, vragi_grp):
        screen.fill((255, 0, 0))
        gg = f2.render("CRASHED!", True, (0, 0, 0))
        
        #(середина экрана минус половина текста)
        cx = 400 // 2 - gg.get_width() // 2
        cy = 600 // 2 - gg.get_height() // 2
        screen.blit(gg, (cx, cy))
        
        pygame.display.update()
        
        pygame.time.wait(2000)
        sys.exit() # все

    pygame.display.update()
    clk.tick(60)