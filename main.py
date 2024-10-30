import random
import pygame_menu
import pygame
pygame.init()

WIDTH,HEIGHT = 400,600
display = pygame. display. set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("СОСОК")
clock = pygame.time.Clock()

GRAVITY = 1
JUMP = -23

def show_start_screen():
    menu=pygame_menu.Menu('MENU',300,400,theme=pygame_menu.themes.THEME_DARK)
    menu.add.button("GO",main)
    menu.add.button("EXIT",pygame_menu.events.EXIT)
    menu.mainloop(display)
def show_end_screen(score):
    menu=pygame_menu.Menu(' Doodle Jump',300,400,theme=pygame_menu.themes.THEME_DARK)
    menu.add.label(f"Score:{int(score)}", font_size = 30)
    menu.add.button("RESTART", main)
    menu.add.button("EXIT",pygame_menu.events.EXIT)
    menu.mainloop(display)

def draw_text(text,pos):
    font = pygame.font.Font(None, 36)
    text_img = font.render(text, True, (0,0,0))
    display.blit(text_img, pos)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_left = pygame.image.load("Копия left.png")
        self.image_right = pygame.transform.flip(self.image_left,True,False)
        self.image = self.image_left
        self.rect = self.image.get_rect(center=(WIDTH//2,HEIGHT//2))
        self.speed = 0
    def draw ( self ) :
        display.blit(self.image,self.rect)
    def update (self) :
        self.rect.y+= self.speed
        self.speed+= GRAVITY
        keys= pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x+= 5
            self.image = self.image_right
        if keys[pygame.K_LEFT]:
            self.rect.x-= 5
            self.image = self.image_left
        if self.rect.right > WIDTH:
            self.rect.left = 0
        if self.rect.left < 0:
            self.rect.right = WIDTH

class Platform ( pygame. sprite. Sprite ) :
    def __init__(self, x, y, img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect(topleft=(x,y))
    def collide_with (self, player) :
        player.speed = JUMP
    def is_on_screen (self) :
        return self.rect.bottom > 0

class NormalPlatform (Platform) :
    def __init__(self, x, y):
        super().__init__(x, y, "Копия green.png")

class SpringPlatform (Platform):
    def __init__(self, x, y):
        super().__init__(x, y, "Копия purple.png")
    def collide_with (self, player) :
        player.speed = JUMP*1.5

class BreakablePlatform (Platform):
    def __init__(self,x,y):
        super().__init__(x,y,"Копия red.png")
    def collide_with (self, player) :
        player.speed = JUMP
        self.kill()
class MovingPlatform (Platform):
    def __init__(self,x,y):
        super().__init__(x,y,"Копия blue.png")
        self.direction = random.choice([-1, 1])
        self.speed = 3
    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.direction *= -1


platforms=pygame. sprite. Group()

def spawn_platform():
    try:
        platform =platforms.sprites()[-1]
    except:
        platform = NormalPlatform (WIDTH // 2 - 50,HEIGHT - 50)
        platforms.add(platform)
    x= random.randint(0,WIDTH-105)
    y=platform.rect.y-random.randint(90,180)
    types = [NormalPlatform,SpringPlatform,BreakablePlatform,MovingPlatform]
    Plat=random.choice(types)
    platforms.add(Plat(x,y))

def is_collision(player:Player,platform:Platform):
    if player.rect.colliderect(platform.rect) and player.speed > 0 and platform.is_on_screen():
        if player.rect.bottom < platform.rect.bottom:
            platform.collide_with(player)
            return True


def main():
    player=Player()
    platforms.empty()
    score = 0
    while True:
        for event in pygame.event.get():
            if event. type == pygame.QUIT:
                return

        player.update()
        platforms.update()
        if len(platforms) < 25:
            spawn_platform()
        hits = pygame.sprite.spritecollide(player,platforms, False, collided = is_collision)
        if player.speed < 0 and player.rect.bottom < HEIGHT / 2:
            player.rect.y -= player.speed
            score += 1
            for p in platforms:
                p.rect.y -= player.speed
        off_platforms = [p for p in platforms if p.rect.y > HEIGHT]
        for p in off_platforms:
            p.kill()
        if player.rect.y > HEIGHT:
            show_end_screen(score)


        display.fill("blue")
        platforms.draw(display)
        player.draw()
        draw_text(f'Score: {score}', (10,10))
        #display. blit ( p1. image, p1. rect )
        pygame.display.update()
        clock.tick(30)

show_start_screen()