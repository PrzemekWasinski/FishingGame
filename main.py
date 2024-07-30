import pygame
from pygame.locals import *
import os
import time
import csv
from functions import catch_fish, show_inventory, sell, shop, show_help

pygame.init()
clock = pygame.time.Clock()

def main():
    
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 500

    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    icon = pygame.image.load(os.path.join("textures", "images", "_icon.png")) 
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Fishing Game")

    fish_list = [] # [["Name", min_weight, max_weight, price_per_kg, rarity, image]]
    with open(os.path.join("databases", "fish.csv")) as file:
        fish_csv = csv.reader(file, delimiter = ",")
        next(fish_csv)
        for row in fish_csv:
            fish_list.append(row)

    rods_list = []  # [["Name", durability, price, order, luck]]
    with open(os.path.join("databases", "rods.csv")) as file:
        rods_csv = csv.reader(file, delimiter = ",")
        next(rods_csv)
        for row in rods_csv:
            rods_list.append(row)

    inventory = {} # {"Fish Name": [Weight, Price]}
    balance = {"Coins": 0} # {"Currency": Amount}
    current_rod = {"Wooden rod": [50, 50, 60]} # {"Rod Name": [Health, Max Health, Luck]}

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        window.blit(img, (x, y))
    text_font = pygame.font.Font(os.path.join("textures", "pixellari.ttf"),16)

    class Water(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            super().__init__()
            self.sprites = []
            self.sprites.append(pygame.image.load(os.path.join("textures", "water_sprite", "_water1.png")))
            self.sprites.append(pygame.image.load(os.path.join("textures", "water_sprite", "_water2.png")))
            self.sprites.append(pygame.image.load(os.path.join("textures", "water_sprite", "_water3.png")))
            self.sprites.append(pygame.image.load(os.path.join("textures", "water_sprite", "_water4.png")))
            self.sprites.append(pygame.image.load(os.path.join("textures", "water_sprite", "_water5.png")))
            self.sprites.append(pygame.image.load(os.path.join("textures", "water_sprite", "_water6.png")))
            self.current_sprite = 0
            self.image = self.sprites[self.current_sprite]
            self.rect = self.image.get_rect()
            self.rect.topleft = [pos_x, pos_y]
        
        def update(self):
            draw_text(f"Balance: ${balance['Coins']}", text_font, (255, 254, 255), 660, 15)
            draw_text(f"{next(iter(current_rod))}: {round(int(next(iter(current_rod.values()))[0]))} / {next(iter(current_rod.values()))[1]}", text_font, (255, 254, 255), 620, 470)
            self.current_sprite += 0.015
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
            self.image = self.sprites[int(self.current_sprite)]

    water_sprite = pygame.sprite.Group()
    water = Water(0, 0)
    water_sprite.add(water)
        
    class Fisherman(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            super().__init__()
            self.sprites = []
            self.sprites.append(pygame.image.load(os.path.join("textures", "fisherman_sprite", "fisherman_pre-cast", "fisherman_pre-cast1.png")))
            self.sprites.append(pygame.image.load(os.path.join("textures", "fisherman_sprite", "fisherman_pre-cast", "fisherman_pre-cast2.png")))
            self.sprites.append(pygame.image.load(os.path.join("textures", "fisherman_sprite", "fisherman_pre-cast", "fisherman_pre-cast3.png")))
            self.sprites.append(pygame.image.load(os.path.join("textures", "fisherman_sprite", "fisherman_pre-cast", "fisherman_pre-cast4.png")))
            self.sprites.append(pygame.image.load(os.path.join("textures", "fisherman_sprite", "fisherman_pre-cast", "fisherman_pre-cast5.png")))
            self.sprites.append(pygame.image.load(os.path.join("textures", "fisherman_sprite", "fisherman_pre-cast", "fisherman_pre-cast6.png")))
            self.sprites.append(pygame.image.load(os.path.join("textures", "fisherman_sprite", "fisherman_pre-cast", "fisherman_pre-cast7.png")))
            self.current_sprite = 0
            self.image = self.sprites[self.current_sprite]
            self.rect = self.image.get_rect()
            self.rect.topleft = [pos_x, pos_y]
        
        def update(self):
            draw_text(f"Balance: ${balance['Coins']}", text_font, (255, 254, 255), 660, 15)
            draw_text(f"{next(iter(current_rod))}: {round(int(next(iter(current_rod.values()))[0]))} / {next(iter(current_rod.values()))[1]}", text_font, (255, 254, 255), 620, 470)
            self.current_sprite += 1
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
            self.image = self.sprites[int(self.current_sprite)]

    fisherman_sprite = pygame.sprite.Group()
    fisherman = Fisherman(400, 325)
    fisherman_sprite.add(fisherman)

    sand = pygame.image.load(os.path.join("textures", "images", "_sand.png"))
    rod_store = pygame.image.load(os.path.join("textures", "images", "_rod_store.png"))
    dock = pygame.image.load(os.path.join("textures", "images", "_dock.png"))
    bucket = pygame.image.load(os.path.join("textures", "images", "_bucket.png"))
    fisherman = pygame.image.load(os.path.join("textures", "images", "_fisherman.png"))

    sand_image = sand.get_rect(topleft=(-6, 0))
    shop_image = rod_store.get_rect(center=(120, 110))
    dock_image = dock.get_rect(center=(355, 365))
    bucket_image = bucket.get_rect(center=(475, 410))
    fisherman_image = fisherman.get_rect(topleft=(400, 325))

    run = True
    while run:

        if int(next(iter(current_rod.values()))[0]) < 0:
            next(iter(current_rod.values()))[0] = 0

        window.blit(sand, (sand_image))
        window.blit(rod_store, (shop_image))
        draw_text(f"Balance: ${balance['Coins']}", text_font, (255, 254, 255), 660, 15)
        draw_text(f"{next(iter(current_rod))}: {round(int(next(iter(current_rod.values()))[0]))} / {next(iter(current_rod.values()))[1]}", text_font, (255, 254, 255), 620, 370)
        pygame.draw.rect(window, (255, 255, 255), (0, 0, 24, 24))
        draw_text("?", text_font, (255, 0, 0), 8, 5)
        water_sprite.draw(window)
        water_sprite.update()
        window.blit(dock, (dock_image))
        window.blit(bucket, (bucket_image))
        window.blit(fisherman, (fisherman_image))
        clock.tick(60)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                run = False

            elif event.type == MOUSEBUTTONDOWN:
                if mouse_x > 460 and mouse_x < 490 and mouse_y > 395 and mouse_y <425:
                    show_inventory(inventory, window)

                elif mouse_x > 330 and mouse_x < 725 and mouse_y > 85 and mouse_y < 280:
                    for i in range(7):
                        time.sleep(0.1)
                        water_sprite.draw(window)
                        water_sprite.update()
                        window.blit(dock, (dock_image))
                        window.blit(bucket, (bucket_image))
                        fisherman_sprite.draw(window)
                        fisherman_sprite.update()
                        pygame.display.update()
                    catch_fish(current_rod, inventory, fish_list, window, balance)

                elif mouse_x > 30 and mouse_x < 210 and mouse_y > 15 and mouse_y < 200:
                    shop(balance, current_rod, rods_list, window)

                elif mouse_x > 257 and mouse_x < 345 and mouse_y > 348 and mouse_y < 420:
                    sell(balance, inventory, window)
                
                elif mouse_x > 0 and mouse_x < 24 and mouse_y > 0 and mouse_y < 24:
                    show_help(window)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
