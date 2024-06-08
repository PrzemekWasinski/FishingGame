import pygame
from pygame.locals import *
from functions import catch_fish, show_inventory, sell, shop, show_help
import csv
import os

pygame.init()
clock = pygame.time.Clock()

def main():
    
    SCREEN_WIDTH = 700
    SCREEN_HEIGHT = 400

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fishing Game")

    fish_list = []
    with open("fish.csv") as file:
        fish_csv = csv.reader(file, delimiter = ",")
        next(fish_csv)
        for row in fish_csv:
            fish_list.append(row)

    rods_list = [] 
    with open("rods.csv") as file:
        rods_csv = csv.reader(file, delimiter = ",")
        next(rods_csv)
        for row in rods_csv:
            rods_list.append(row)

    inventory = {} # {"Fish Name": [Weight, Price]}
    balance = {"Coins": 0}
    current_rod = {"Wooden rod": [50, 50, 10]} # {"Rod Name": [Health, Max Health, Luck]}

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))
    text_font = pygame.font.Font(os.path.join("textures", "pixellari.ttf"),16)

    class Water(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            super().__init__()
            self.sprites = []
            self.sprites.append(pygame.image.load(os.path.join("textures", "water_sprite", "_water1.png")))
            self.sprites.append(pygame.image.load(os.path.join("textures", "water_sprite", "_water2.png")))
            self.current_sprite = 0
            self.image = self.sprites[self.current_sprite]
            self.rect = self.image.get_rect()
            self.rect.topleft = [pos_x, pos_y]
        
        def update(self):
            draw_text(f"Balance: ${balance['Coins']}", text_font, (255, 254, 255), 580, 15)
            draw_text(f"{next(iter(current_rod))}: {next(iter(current_rod.values()))[0]} / {next(iter(current_rod.values()))[1]}", text_font, (255, 254, 255), 540, 370)
            self.current_sprite += 0.02
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
            self.image = self.sprites[int(self.current_sprite)]
        
    moving_sprites = pygame.sprite.Group()
    water = Water(0, 0)
    moving_sprites.add(water)

    sand = pygame.image.load(os.path.join("textures", "images", "_sand.png"))
    rod_store = pygame.image.load(os.path.join("textures", "images", "_rod_store.png"))
    sell_fish = pygame.image.load(os.path.join("textures", "images", "_sell_fish.png"))
    bridge = pygame.image.load(os.path.join("textures", "images", "_bridge.png"))
    hat = pygame.image.load(os.path.join("textures", "images", "_hat.png"))
    bucket = pygame.image.load(os.path.join("textures", "images", "_bucket.png"))

    sand_image = sand.get_rect(center=(100, 200))
    shop_image = rod_store.get_rect(center=(100, 37))
    sell_image = sell_fish.get_rect(center=(100, 362))
    bridge_image = bridge.get_rect(center=(250, 145))
    hat_image = hat.get_rect(center=(325, 160))
    bucket_image = bucket.get_rect(center=(325, 130))

    run = True
    while run:

        if int(next(iter(current_rod.values()))[0]) < 0:
            next(iter(current_rod.values()))[0] = 0

        screen.blit(sand, (sand_image))
        screen.blit(rod_store, (shop_image))
        screen.blit(sell_fish, (sell_image))
        screen.blit(bridge, (bridge_image))
        screen.blit(hat, (hat_image))
        screen.blit(bucket, (bucket_image))
        draw_text(f"Balance: ${balance['Coins']}", text_font, (255, 254, 255), 580, 15)
        draw_text(f"{next(iter(current_rod))}: {next(iter(current_rod.values()))[0]} / {next(iter(current_rod.values()))[1]}", text_font, (255, 254, 255), 520, 370)
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, 24, 24))
        draw_text("?", text_font, (255, 0, 0), 8, 5)
        moving_sprites.draw(screen)
        moving_sprites.update()
        pygame.display.flip()
        clock.tick(60)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        #print(mouse_x, mouse_y)
        #print(screen.get_at((mouse_x, mouse_y)))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            elif event.type == MOUSEBUTTONDOWN:
                if mouse_x > 313 and mouse_x < 337 and mouse_y > 120 and mouse_y <139:
                    show_inventory(inventory, screen)

                elif mouse_x > 400:
                    catch_fish(current_rod, inventory, fish_list, screen, balance)

                elif mouse_x > 25 and mouse_x < 175 and mouse_y > 0 and mouse_y < 75:
                    shop(balance, current_rod, rods_list, screen)

                elif mouse_x > 25 and mouse_x < 175 and mouse_y > 325 and mouse_y < 400:
                    sell(balance, inventory, screen)
                
                elif mouse_x > 0 and mouse_x < 24 and mouse_y > 0 and mouse_y < 24:
                    show_help(screen)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
