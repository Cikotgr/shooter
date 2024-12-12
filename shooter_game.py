from pygame import *
from random import randint

#background music
mixer.init()
# mixer.music.load('space.ogg')
# mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('Arial',26)
font2 = font.SysFont('Arial', 66)
you_lose = font2.render('YOU LOSE',1,(240,0,0))



#we need the following images:
img_back = "galaxy.jpg" #game background
img_hero = "kapal perang.png" #hero


#parent class for other sprites
class GameSprite(sprite.Sprite):
#class constructor
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        #Call for the class (Sprite) constructor:
        sprite.Sprite.__init__(self)


        #every sprite must store the image property
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed


        #every sprite must have the rect property – the rectangle it is fitted in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
#method drawing the character on the window
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


#main player class
class Player(GameSprite):
    #method to control the sprite with arrow keys
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        
    #method to "shoot" (use the player position to create a bullet there)
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 10,20, 20)
        bullets.add(bullet)
        fire_sound.play()

missed = 0
class Enemy(GameSprite):
    def update(self):
        global missed
        self.rect.y += self.speed
        if self.rect.y >= win_height:
            self.rect.y = 2
            self.rect.x = randint(5, win_width - 40)
            self.speed = randint(1,5)
            missed += 1

missed = 0
class Enemy(GameSprite):
    def update(self):
        global missed
        self.rect.y += self.speed
        if self.rect.y >= win_height:
            self.rect.y = 2
            self.rect.x = randint(5, win_width - 40)
            self.speed = randint(1,5)
            missed += 1

class Enemy2(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= win_height:
            self.rect.y = 2
            self.rect.x = randint(5, win_width - 40)
            self.speed = randint(1,5)
            

        
        

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        
        

#create a window
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


#create sprites
ship = Player("kapal perang.png", 5, win_height - 100, 10, 80, 100)


enemy = sprite.Group()

for i in range(5):
    ufo = Enemy("ufo.png", randint(5, win_width - 40), 2, randint(1,5), 100, 60)
    enemy.add(ufo)



bullets = sprite.Group()


#the "game is over" variable: as soon as True is there, sprites stop working in the main loop
finish = False
clock = time.Clock()
FPS = 60
#Main game loop:
run = True #the flag is reset by the window close button
score = 0



while run:
    #"Close" button press event
    for e in event.get():
        if e.type == QUIT:
            run = False
        
        if e.type == KEYDOWN:
            keys = key.get_pressed()
            if keys[K_SPACE]:
                ship.fire()
    

    if not finish:

        text_lose = font1.render('Alien terlewat:' + str(missed),1,(245,132,132))
        text_score = font1.render('Sekor'+str(score),1,(255,255,255))
        #update the background
        window.blit(background,(0,0))
        window.blit(text_lose,(0,20))
        window.blit(text_score,(0,0))
        
        if missed > 5 : 
            finish = True
            window.blit(you_lose,(win_width/2, win_height/2))
        

        collides = sprite.groupcollide(enemy, bullets, True, True)
        # colides_rock = sprite.groupcollide(rock, bullets, False, True)
        if collides:
            ufo = Enemy("ufo.png", randint(5, win_width - 40), 2, randint(1,5), 100, 60)
            enemy.add(ufo)
            score += 1
        
        #launch sprite movements
        ship.update()


        #update them in a new location in each loop iteration
        ship.reset()

        enemy.draw(window)
        enemy.update()


        bullets.draw(window)

        bullets.update()

        display.update()
    
    #the loop is executed each 0.05 sec
    clock.tick(FPS)