import pygame
pygame.init()

win = pygame.display.set_mode((500, 480))
pygame.display.set_caption ("Arcade Game")

walkRight = [pygame.image.load("R1.png"), pygame.image.load("R2.png"), pygame.image.load("R3.png"), pygame.image.load("R4.png"), pygame.image.load("R5.png"), pygame.image.load("R6.png"), pygame.image.load("R7.png"), pygame.image.load("R8.png"), pygame.image.load("R9.png")]
walkLeft = [pygame.image.load("L1.png"), pygame.image.load("L2.png"), pygame.image.load("L3.png"), pygame.image.load("L4.png"), pygame.image.load("L5.png"), pygame.image.load("L6.png"), pygame.image.load("L7.png"), pygame.image.load("L8.png"), pygame.image.load("L9.png")]
bg = pygame.image.load("bg.jpg")
char = pygame.image.load("standing.png")

clock = pygame.time.Clock()
score = 0

bulletSound = pygame.mixer.Sound("bullet.wav")
hitSound = pygame.mixer.Sound("hit.wav")

bgMusic = pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)  # the -1 makes the background music play continuously


screen_x = 500
screen_y = 500

class Protagonist():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.left = False
        self.right = False
        self.isJump = False
        self.jumpCount = 10
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)



    def draw(self, win):
        win.blit(bg, (0,0))
        if self.walkCount + 1 >= 27:                   # this is because 3 sprites in the direction list is going to be displayed for 1 sec
            self.walkCount = 0                         # and there are 9 sprites for each direction and hence are integer divided by 3 if the
                                                       # direction boolean is true as depicted.
        if not (self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))

        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2) commented out to avoid showing the hitbox around the sprites

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 60
        self.y = 410
        self.walkCount = 0
        self.font1 = pygame.font.SysFont("arial", 100)
        text = self.font1.render("-5", 1, (255, 0, 0))
        win.blit(text, (250 - (text.get_width())//2, 200))
        pygame.display.update()
        self.delay_ms = 0
        while self.delay_ms < 200:
            pygame.time.delay(10)
            self.delay_ms += 1
            for events in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.delay_ms = 301
                    pygame.quit()


class Projectile():
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class Enemy():
    walkRight = [pygame.image.load("R1E.png"), pygame.image.load("R2E.png"), pygame.image.load("R3E.png"), pygame.image.load("R4E.png"), pygame.image.load("R5E.png"), pygame.image.load("R6E.png"), pygame.image.load("R7E.png"), pygame.image.load("R8E.png"), pygame.image.load("R9E.png"), pygame.image.load("R10E.png"), pygame.image.load("R11E.png")]
    walkLeft = [pygame.image.load("L1E.png"), pygame.image.load("L2E.png"), pygame.image.load("L3E.png"), pygame.image.load("L4E.png"), pygame.image.load("L5E.png"), pygame.image.load("L6E.png"), pygame.image.load("L7E.png"), pygame.image.load("L8E.png"), pygame.image.load("L9E.png"), pygame.image.load("L10E.png"), pygame.image.load("L11E.png")]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 15, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0 :
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - ((5) * (10 - self.health)), 10))
            self.hitbox = (self.x + 15, self.y + 2, 31, 57)
            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2) commented out to avoid showing the hitbox around the sprites

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1

        else:
            self.visible = False

        #print("Hit")



def redrawGameWindow():
    win.blit(bg, (0,0))
    man.draw(win)
    text = font.render("Score: " + str(score), 1, (0,0,0))
    win.blit(text, (360, 10))
    for bullet in bullets:
        bullet.draw(win)
    goblin.draw(win)
    pygame.display.update()

font = pygame.font.SysFont("arial", 30, True)
man = Protagonist(300, 405, 64, 64)
goblin = Enemy(100, 410, 64, 64, 450)
bullets = []
shootLoop = 0
running = True
while running:
    clock.tick(27)

    if goblin.visible == True:
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                score -= 5

    if shootLoop > 0:
        shootLoop += 1

    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for bullet in bullets:
        if goblin.visible == True:
            if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
                if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                    hitSound.play()
                    goblin.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))

        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        bulletSound.play()
        if man.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 5:
            bullets.append(Projectile(round(man.x + man.width//2), round(man.y + man.height//2), 6, (255,0,0), facing))

        shootLoop = 1


    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False

    elif keys[pygame.K_RIGHT] and man.x < (screen_x - man.width - man.vel):
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False

    else:
        man.walkCount = 0
        man.standing = True

    if not (man.isJump):
        # if keys[pygame.K_UP] and y > vel:       # wanna keep the Protagonist on the ground only. can move up and down by jumps only.
        #     y -= vel
        #
        # if keys[pygame.K_DOWN] and y < (screen_y - height - vel):
        #     y += vel

        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= ((man.jumpCount) ** 2) * 0.5 * neg
            man.jumpCount -= 1

        else:
            man.isJump = False
            man.jumpCount = 10

    redrawGameWindow()

pygame.quit()
