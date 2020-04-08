# Imports
import os
import pygame
from LCCV2.chars import Player
from LCCV2.platforms import BackDrop, FloatingPlatform, MovingTile, BasePlatform
from LCCV2.enemies import Virus1

# Setting up the font
pygame.font.init()
font = pygame.font.Font("resources/fonts/Anonymous.ttf", 14)

# Working file paths
IMAGES_PATH = 'resources/Images/'

# Starting pygame
pygame.init()

# Loading the image for hud
hud = pygame.image.load(IMAGES_PATH + "HUD/hud.png")

# Setting the screen up
win = pygame.display.set_mode((1200, 640))
pygame.display.set_caption("LCC GAME")
ICON = pygame.image.load(os.path.join(IMAGES_PATH+"Icon/", 'GameIcon_64.png'))
pygame.display.set_icon(ICON)

# Setting up the player
man = Player(x=300, y=100)
man.load_anim(IMAGES_PATH+"Characters/Player/")
man.init_guns()

# Setting up the clock
clock = pygame.time.Clock()

# Setting up the platform
platforms = [BasePlatform(0), MovingTile(400, 400), FloatingPlatform(900, 400),
             BasePlatform(1601), FloatingPlatform(1300, 400),
             MovingTile(1650, 400)]

# Loading the images for platform
platforms[0].load_anim(IMAGES_PATH + "Tilesets/level_5/platform_base.png")
platforms[1].load_anim(IMAGES_PATH + "Tilesets/level_5/moving_tile.png")
platforms[2].load_anim(IMAGES_PATH + "Tilesets/level_5/platform.png")
platforms[3].load_anim(IMAGES_PATH + "Tilesets/level_5/platform_base.png")
platforms[4].load_anim(IMAGES_PATH + "Tilesets/level_5/platform.png")
platforms[5].load_anim(IMAGES_PATH + "Tilesets/level_5/moving_tile.png")

# Making the backdrop
bottom = BackDrop()
top = BackDrop()

# Loading the images for the backdrop
bottom.load_anim(IMAGES_PATH + "Background/level_1/bg_bottom.png")
top.load_anim(IMAGES_PATH + "Background/level_1/bg_top.png")
bg_layers = [top, bottom]

# Setting up Enemy
enemies = [Virus1(x=800, y=500), Virus1(x=1000, y=500)]
enemies[0].load_anim(IMAGES_PATH+"Characters/Virus/Virus_1/idle.png", IMAGES_PATH+"Projectiles/virus_1_")
enemies[0].set_max_distance(200)

enemies[1].load_anim(IMAGES_PATH+"Characters/Virus/Virus_1/idle.png", IMAGES_PATH+"Projectiles/virus_1_")
enemies[1].set_max_distance(200)


# Loading images for hud
weapons_list = [pygame.image.load(IMAGES_PATH + "Weapons/gun_pistol.png"),
                pygame.image.load(IMAGES_PATH + "Weapons/gun_shotgun.png"),
                pygame.image.load(IMAGES_PATH + "Weapons/gun_rpg.png"),
                pygame.image.load(IMAGES_PATH + "Weapons/gun_ar.png")]


# Running the game
def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        man.move(keys, platforms, enemies, bg_layers)
        platforms[1].move_x(1)
        platforms[5].move_y(1)
        for enemy in enemies:
            enemy.move(3, man)
        man.change_weapon(keys)
        man.on_ground(platforms)
        clock.tick(30)
        redraw(win)


# draw function
def redraw(win):
    win.fill((104, 98, 112))
    bottom.draw(win)
    top.draw(win)
    man.draw(win)
    for enemy in enemies:
        enemy.draw(win)

    for platform in platforms:
        platform.draw(win)

    # Stats part
    win.blit(hud, (0, 0))
    score = font.render(f"score: {man.score}", 1, (255, 255, 255))
    life_left = font.render(f"life left: {man.hp}", 1, (255, 255, 255))
    win.blit(life_left, (18, 14))
    win.blit(score, (18, 37))
    if man.current_weapon != 0:
        weapon_name = font.render(man.weapon_list[man.current_weapon], 1, (255, 255, 255))
        ammo_left = font.render(
            f"ammo left: {man.weapons[man.weapon_list[man.current_weapon]].ammo_count}/{man.weapons[man.weapon_list[man.current_weapon]].ammo_limit}",
            1, (255, 255, 255))
        ammo_on_load = font.render(
            f"loaded ammo: {man.weapons[man.weapon_list[man.current_weapon]].on_load}/{man.weapons[man.weapon_list[man.current_weapon]].hold_limit}",
            1, (255, 255, 255))
        win.blit(weapon_name, (28, 565))
        win.blit(ammo_left, (100, 620))
        win.blit(ammo_on_load, (100, 630))
        win.blit(weapons_list[man.current_weapon - 1], (28, 580))

    for enemy in enemies:
        enemy.update_bullets(win)

    pygame.display.update()


if __name__ == "__main__":
    main()
