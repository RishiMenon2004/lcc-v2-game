import pygame


# Entity class for all characters
class Entity:

    # Default variables
    hp = 100
    facing = None
    speed = 10

    width = 50
    height = 50

    def __init__(self, x, y):

        # Getting the character location setup
        self.x = x
        self.y = y

    # Taking health away
    def hurt(self, damage):
        self.hp -= damage

    # Getting health
    def re_gen(self, hp):
        self.hp += hp


class Enemy(Entity):

    # Variables
    points = 100
    hit = 5

    # Class initialization
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # load anim_function
    def load_anim(self, path):
        self.idle = pygame.image.load(path)
        self.moving = pygame.image.load(path)
        self.attack = pygame.image.load(path)

    # Move function fall back
    def move(self):
        pass

    # Draw method fallback
    def draw(self):
        pass


# Main player class
class Player(Entity):

    height = 128
    speed = 10
    vel = 5
    jumping = False
    on_platform = False

    # loading animation function
    def load_anim(self, path):

        # empty hand animations
        self.anim = pygame.image.load(path)
        '''
        self.anim = {"idle_L": [], "jumping_L": [], "running_L": [],
                     "idle_R": [], "jumping_R": [], "running_R": []}
        '''
    # Moving control
    def move(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.x += self.speed

        elif keys[pygame.K_LEFT]:
            self.x -= self.speed

        if keys[pygame.K_UP] and self.on_platform:
            if not self.jumping:
                self.vel = 10
                self.jumping = True

        if self.jumping and self.vel > 0:
            self.y -= self.vel
            self.vel -= 1

        elif self.jumping and self.vel <= 0:
            self.jumping = False

        if not self.on_platform and not self.jumping:
            self.y += self.vel
            self.vel += 1

    def on_ground(self, platform):
        if (platform.y + platform.height) > (self.y + self.height) >= platform.y:
            self.on_platform = True
            self.vel = 10
            self.y = platform.y - self.height

        else:
            self.on_platform = False

    # rendering function
    def draw(self, win):
        win.blit(self.anim, (self.x, self.y))
