import pygame
import random
from pygame import mixer
import math
import time

pygame.init()
mixer.init()

mixer.music.load("background.mp3")
mixer.music.play(-1)

pop_sound = mixer.Sound("pop.mp3")
shooting_sound = mixer.Sound("shoot.wav")
tadaa_sound = mixer.Sound("tadaa.mp3")

clock = pygame.time.Clock()

width = 1000
height = 700

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("HuntingGame")
pygame.display.set_icon(pygame.image.load("target.png"))
background = pygame.transform.scale(pygame.image.load("background.jpg"),(width, height))

gun = pygame.transform.scale(pygame.image.load("gun.png"), (38, 300))
baloon_number = 0

class Baloon(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        super().__init__()
        self.rect = pygame.Rect(x, y, 150, 150)
        self.image = pygame.transform.scale(pygame.image.load(img), (150, 150))
        self.speed = random.choice([-1, 1])
        self.counter = 0

    def update(self):
        self.counter += 1
        if self.counter > 25:
            self.counter = 0
            self.speed = random.choice([-1, 1])

        self.rect.y += self.speed

        if self.rect.top <= 0:
            self.rect.top = 0

        if self.rect.bottom >= 300:
            self.rect.bottom = 300


class TargetClass:
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load("target.png"), (50, 50))
        self.rect = self.image.get_rect(centerx=width/2, centery=height/2)

    def draw(self):
        screen.blit(self.image, self.rect)

    def movement(self):
        self.rect.center = pygame.mouse.get_pos()

    def update(self):
        self.draw()
        self.movement()

class BulletClass(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(img), (10, 10))
        self.rect = self.image.get_rect(centerx=width/2, centery=height)

        self.speed = 5
        self.dx = 0
        self.dy = 0

    def movement(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.bottom < 0:
            self.kill()

    def update(self):
        self.movement()



baloon_group = pygame.sprite.Group()

images = ["red.png", "green.png", "yellow.png"]
for i, img in enumerate(images):
    baloon1 = Baloon(i * 400, 100, img)
    baloon_group.add(baloon1)
    baloon_number += 1


pygame.mouse.set_visible(False)
target1 = TargetClass()

background = pygame.transform.scale(pygame.image.load("background.jpg"), (width, height))
bullet_group = pygame.sprite.Group()
run = True
score = 0


def write(text, font_size, color, x, y):
    font = pygame.font.Font(None, font_size)
    rendered_text = font.render(text, True, color)
    rect = rendered_text.get_rect(centerx=x, centery=y)
    screen.blit(rendered_text, rect)

transformed_gun = gun


start_time = time.time()
while run:

    clock.tick(60)
    # screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    for bullet in bullet_group:
        for baloon in baloon_group:
            if bullet.rect.colliderect(baloon.rect):
                baloon.kill()
                bullet.kill()
                score += 1
                pop_sound.play()

    # screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            bullet = BulletClass("bullet.png")
            bullet_group.add(bullet)

            mouse_x = pygame.mouse.get_pos()[0]
            mouse_y = pygame.mouse.get_pos()[1]

            distance_x = mouse_x - bullet.rect.x
            distance_y = mouse_y - bullet.rect.y

            angle = math.atan2(distance_y, distance_x)


            #ტყვიის ლოკაციის ცვლილება
            bullet.rect.x += 150 * math.cos(angle)
            bullet.rect.y += 150 * math.sin(angle)

            bullet.dx = bullet.speed * math.cos(angle)
            bullet.dy = bullet.speed * math.sin(angle)

            shooting_sound.play()

    #იარაღის დახატვა და მოძრაობა
    pos = pygame.mouse.get_pos()
    x_dist = pos[0] - width/2
    y_dist = pos[1] - height
    angle = math.degrees(math.atan2(y_dist, x_dist))
    transformed_gun = pygame.transform.rotate(gun, -(angle+90))
    gun_rect = transformed_gun.get_rect(centerx=width/2, centery=height)
    screen.blit(transformed_gun, gun_rect)

    bullet_group.draw(screen)
    bullet_group.update()

    baloon_group.draw(screen)
    baloon_group.update()
    target1.update()

    write(f"Score {score}", 60, (100, 200, 100), 100, 20)
    pygame.display.update()

    if baloon_number == score:
        break

mixer.music.stop()
end_time = time.time()

write(f"You Won in {round(end_time-start_time)} seconds!", 90, (255, 255, 100), width/2, height/2)
pygame.display.update()
tadaa_sound.play()
pygame.time.wait(5000)
