#Создай собственный Шутер!

from pygame import *
from random import *

win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))



class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, plaeyr_width, player_height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (plaeyr_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and self.rect.y > 5 :
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.y < 400:
            self.rect.y += self.speed
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -15, 20, 15)
        bullets.add(bullet)
        

font.init()
points = 0
lost = 0
font2 = font.SysFont('Arial', 25)
font1 = font.SysFont('Arial', 25)
font3 = font.SysFont('Arial', 70)
font4 = font.SysFont('Arial', 70)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


class Boss(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            finish = True
            window.blit(text_stop, (170, 100))
            

            
monsters = sprite.Group()
bullets = sprite.Group()



for i in range(5):
    monster = Enemy('ufo.png', randint(80, win_width - 80), -20, randint(1, 5), 80, 50)
    monsters.add(monster)
player = Player('rocket.png', 100, 400, 5, 80, 100)

boss = Boss('ufo.png', randint(80, win_width - 80), -20, 1, 240, 150)

game = True
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')
clock = time.Clock()
FPS = 60
finish = False
hp_boss = 10

while game:
    
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
                fire.play()
    if not finish:
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        text_points = font1.render('Счет: ' + str(points), 1, (255, 255, 255))
        text_stop = font3.render('YOU LOSE!!!', 1, (255, 0, 0))
        text_win = font4.render('YOU WIN!!!', 1, (0, 255, 0))
        
        window.blit(background,(0, 0))
        monsters.draw(window)
        bullets.draw(window)
        window.blit(text_lose, (0, 0))
        window.blit(text_points, (0, 30))
        player.reset()
        player.update()
        bullets.update()
        monsters.update()

        sprite_list = sprite.groupcollide(monsters, bullets, True, True)
        for i in sprite_list:
            points += 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), -20, randint(1, 7), 80, 50)
            monsters.add(monster)
            
        if sprite.spritecollide(player, monsters, False):
            finish = True
            window.blit(text_stop, (170, 100))

        if sprite.collide_rect(player, boss):
            finish = True
            window.blit(text_stop, (170, 100))
            
            

        if lost >= 4:
            finish = True
            window.blit(text_stop, (170, 100))
            
            
        if points >= 11:
            for monster in monsters:
                monster.kill()
            boss.reset()
            boss.update()
            if sprite.spritecollide(boss, bullets, True):
                hp_boss -= 1
                if hp_boss <= 0:
                    finish = True
                    window.blit(text_win, (170, 100))
                
        
        
                            
        

    display.update()
    clock.tick(FPS)

