import random
import pygame
from pygame.locals import *
import time
import os

pygame.init()
clock = pygame.time.Clock()
speed = 0.85

sand = pygame.image.load(os.path.join("textures", "images", "_sand.png"))
rod_store = pygame.image.load(os.path.join("textures", "images", "_rod_store.png"))
sell_fish = pygame.image.load(os.path.join("textures", "images", "_sell_fish.png"))
bridge = pygame.image.load(os.path.join("textures", "images", "_bridge.png"))
hat = pygame.image.load(os.path.join("textures", "images", "_hat.png"))
bucket = pygame.image.load(os.path.join("textures", "images", "_bucket.png"))
bobber = pygame.image.load(os.path.join("textures", "images", "_bobber.png"))

sand_image = sand.get_rect(center=(100, 200))
shop_image = rod_store.get_rect(center=(100, 37))
sell_image = sell_fish.get_rect(center=(100, 362))
bridge_image = bridge.get_rect(center=(250, 145))
hat_image = hat.get_rect(center=(325, 160))
bucket_image = bucket.get_rect(center=(325, 130))

def refresh_screen(screen, balance, current_rod, circle_x, circle_y, radius):
    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))
    text_font = pygame.font.Font(os.path.join("textures", "pixellari.ttf"),16)
    screen.blit(sand, (sand_image))
    screen.blit(rod_store, (shop_image))
    screen.blit(sell_fish, (sell_image))
    screen.blit(bridge, (bridge_image))
    screen.blit(hat, (hat_image))
    screen.blit(bucket, (bucket_image))
    pygame.draw.rect(screen, (0, 0, 0), (338, 160, 60, 2))
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, 24, 24))
    draw_text("?", text_font, (255, 0, 0), 8, 5)
    if circle_x or circle_y != 0:
        pygame.draw.circle(screen, (255, 255, 255), (circle_x, circle_y), radius, 1)
        pygame.draw.line(screen, (0, 0, 0), (397, 160), (circle_x, circle_y))
    draw_text(f"Balance: ${balance['Coins']}", text_font, (255, 254, 255), 580, 15)
    draw_text(f"{next(iter(current_rod))}: {next(iter(current_rod.values()))[0]} / {next(iter(current_rod.values()))[1]}", text_font, (255, 254, 255), 540, 370)
    pygame.display.flip()
    clock.tick(60)

def catch_fish(current_rod, inventory, fish_list, screen, balance):
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
        def update(self, speed):
            draw_text(f"Balance: ${balance['Coins']}", text_font, (255, 254, 255), 580, 15)
            draw_text(f"{next(iter(current_rod))}: {next(iter(current_rod.values()))[0]} / {next(iter(current_rod.values()))[1]}", text_font, (255, 254, 255), 540, 370)
            self.current_sprite += speed
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
            self.image = self.sprites[int(self.current_sprite)]
    moving_sprites = pygame.sprite.Group()
    water = Water(0, 0)
    moving_sprites.add(water)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    bobber_image = bobber.get_rect(center=(mouse_x, mouse_y))
    pygame.draw.rect(screen, (0, 0, 0), (338, 160, 60, 2))
    pygame.draw.line(screen, (0, 0, 0), (397, 160), (mouse_x, mouse_y))
    screen.blit(bobber, (bobber_image))
    circle_x = mouse_x
    circle_y = mouse_y
    while True:
        pygame.draw.line(screen, (0, 0, 0), (397, 160), (circle_x, circle_y))
        if int(next(iter(current_rod.values()))[0]) <= 0:
            draw_text("Fishing rod is broken", text_font, (255, 254, 255), 320, 15)
            pygame.display.update()
            time.sleep(1)
            break
        else:
            screen.blit(bobber, (bobber_image))
            pygame.display.update()
            pygame.event.clear()
            selected_fish = []
            random_n = random.randint(1, 100)
            possible_fish = []
            for i in fish_list:
                if int(i[4]) <= random_n:
                    possible_fish.append(i)
                    selected_fish = random.choice(possible_fish)
                else:
                    selected_fish = ["", 0, 0, 0, 0]
            fish = selected_fish[0]
            weight = random.randint(int(selected_fish[1]), int(selected_fish[2]))
            price = weight * int(selected_fish[3])
            rarity = selected_fish[4]
            radius = 35 - int(rarity)
            moving_sprites.draw(screen)
            moving_sprites.update(1)
            time.sleep(1)
            refresh_screen(screen, balance, current_rod, 0, 0, 0)
            if random.randint(1, 100) <= next(iter(current_rod.values()))[2]:
                fishing_passed = True
                for i in range(3):
                    direction_x = random.randint(1, 2)
                    direction_y = random.randint(1, 2)
                    random_x = random.randint(1, 2)
                    random_y = random.randint(1, 2)
                    for i in range(random.randint(50, 150)):    # I know how this looks but I truly believe there was no other
                        if circle_x > 650:                      # way of stopping the circle from going outside of the screen
                            random_x = random.randint(1, 2)
                            random_y = random.randint(1, 2)
                            if random_x == 1 and random_y == 1:
                                circle_x -= direction_x
                                circle_y -= direction_y
                            elif random_x == 1 and random_y == 2:
                                circle_x -= direction_x
                                circle_y += direction_y
                            elif random_x == 2 and random_y == 1:
                                circle_x -= direction_x
                                circle_y -= direction_y
                            elif random_x == 2 and random_y == 2:
                                circle_x -= direction_x
                                circle_y += direction_y
                        elif circle_x < 435:
                            random_x = random.randint(1, 2)
                            random_y = random.randint(1, 2)
                            if random_x == 1 and random_y == 1:
                                circle_x += direction_x
                                circle_y -= direction_y
                            elif random_x == 1 and random_y == 2:
                                circle_x += direction_x
                                circle_y += direction_y
                            elif random_x == 2 and random_y == 1:
                                circle_x += direction_x
                                circle_y -= direction_y
                            elif random_x == 2 and random_y == 2:
                                circle_x += direction_x
                                circle_y += direction_y
                        elif circle_y > 330:
                            random_x = random.randint(1, 2)
                            random_y = random.randint(1, 2)
                            if random_x == 1 and random_y == 1:
                                circle_x -= direction_x
                                circle_y -= direction_y
                            elif random_x == 1 and random_y == 2:
                                circle_x -= direction_x
                                circle_y -= direction_y
                            elif random_x == 2 and random_y == 1:
                                circle_x += direction_x
                                circle_y -= direction_y
                            elif random_x == 2 and random_y == 2:
                                circle_x += direction_x
                                circle_y -= direction_y
                        elif circle_y < 70:
                            random_x = random.randint(1, 2)
                            random_y = random.randint(1, 2)
                            if random_x == 1 and random_y == 1:
                                circle_x -= direction_x
                                circle_y += direction_y
                            elif random_x == 1 and random_y == 2:
                                circle_x -= direction_x
                                circle_y += direction_y
                            elif random_x == 2 and random_y == 1:
                                circle_x += direction_x
                                circle_y += direction_y
                            elif random_x == 2 and random_y == 2:
                                circle_x += direction_x
                                circle_y += direction_y
                        else:
                            if random_x == 1 and random_y == 1:
                                circle_x -= direction_x
                                circle_y -= direction_y
                            elif random_x == 1 and random_y == 2:
                                circle_x -= direction_x
                                circle_y += direction_y
                            elif random_x == 2 and random_y == 1:
                                circle_x += direction_x
                                circle_y -= direction_y
                            elif random_x == 2 and random_y == 2:
                                circle_x += direction_x
                                circle_y += direction_y
                        pygame.event.clear()
                        current_mouse_x, current_mouse_y = pygame.mouse.get_pos()
                        if current_mouse_x + radius > circle_x and current_mouse_x - radius < circle_x:
                            if current_mouse_y + radius > circle_y and current_mouse_y - radius < circle_y:
                                refresh_screen(screen, balance, current_rod, circle_x, circle_y, radius)
                                moving_sprites.draw(screen)
                                moving_sprites.update(0.05)
                                pygame.draw.circle(screen, (255, 255, 255), (circle_x, circle_y), radius, 1)
                                pygame.draw.line(screen, (0, 0, 0), (397, 160), (circle_x, circle_y))
                                pygame.draw.rect(screen, (0, 0, 0), (338, 160, 60, 2))
                                pygame.display.update()
                                time.sleep(0.05)
                            else:
                                fishing_passed = False
                                break
                        else:
                            fishing_passed = False
                            break
                if fishing_passed != False:
                    if fish in inventory:
                        inventory[fish][0] += weight
                        inventory[fish][1] += price
                        next(iter(current_rod.values()))[0] = int(next(iter(current_rod.values()))[0]) - weight
                    else:
                        inventory[fish] = [weight, price]
                        next(iter(current_rod.values()))[0] = int(next(iter(current_rod.values()))[0]) - weight
                    draw_text(f"You cought a {weight}kg {fish}", text_font, (255, 254, 255), 250, 15)
                    display_fish = pygame.image.load(os.path.join("textures", "images", f"_{fish.lower()}.png"))
                    display_fish_image = display_fish.get_rect(center=(230, 22))
                    screen.blit(display_fish, (display_fish_image))
                    pygame.display.update()
                    time.sleep(1)
                    return current_rod, inventory, fish_list
                else:
                    break
            else:
                pass

def show_inventory(inventory, screen):
    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))
    text_font = pygame.font.Font(os.path.join("textures", "pixellari.ttf"),16)
    if len(inventory) == 0:
        pygame.display.update()
    else:
        pygame.event.clear()
        while True:
            pygame.display.update()
            event = pygame.event.wait()
            text_y = 5
            rect_y = 5
            pygame.draw.rect(screen, (0, 0, 0), (495, 5, 200, 17))
            draw_text("Your fish:", text_font, (255, 254, 255), 500, 5)
            for key, value in inventory.items():
                text_y += 15
                rect_y += 15
                pygame.draw.rect(screen, (0, 0, 0), (495, rect_y, 200, 15))
                draw_text(f"{key} {value[0]}kg (${value[1]})", text_font, (255, 254, 255), 525, text_y)
                display_fish = pygame.image.load(os.path.join("textures", "images", f"_{key.lower()}.png"))
                display_fish_image = display_fish.get_rect(center=(495 + 15, text_y + 6))
                screen.blit(display_fish, (display_fish_image))
            if event.type == MOUSEBUTTONDOWN:
                break
            pygame.display.update()

def sell(balance, inventory, screen):
    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))
    text_font = pygame.font.Font(os.path.join("textures", "pixellari.ttf"),16)
    if len(inventory) == 0:
        draw_text("You have no fish to sell", text_font, (255, 254, 255), 320, 15)
        pygame.display.update()
        time.sleep(1)
    else:
        for value in inventory.values():
            balance["Coins"] += value[1]
        dict.clear(inventory)
        draw_text(f"All fish sold!", text_font, (255, 254, 255), 320, 15)
        pygame.display.update()
        time.sleep(1)
    return balance, inventory

def shop(balance, current_rod, rods_list, screen):
    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))
    text_font = pygame.font.Font(os.path.join("textures", "pixellari.ttf"),16)
    selected_rod = []
    for value in balance.values():
        pygame.draw.rect(screen, (0, 0, 0), (495, 5, 200, 17))
        draw_text(f"Balance: ${value}", text_font, (255, 254, 255), 500, 5)
    text_y = 5
    rect_y = 5
    for i in rods_list:
        text_y += 15
        rect_y += 15
        pygame.draw.rect(screen, (0, 0, 0), (495, rect_y, 200, 17))
        draw_text(f"{i[3]} - {i[0]}: (${i[2]})", text_font, (255, 254, 255), 500, text_y)
    pygame.event.clear()
    while True:
        try:
            pygame.display.update()
            event = pygame.event.wait()
            key = pygame.key.get_pressed()
            if event.type == KEYDOWN:
                if key[pygame.K_0] == True:
                    break
                else:
                    selected_rod = rods_list[int(event.key) - 49]
                    pygame.draw.rect(screen, (0, 0, 0), (495, rect_y + 17, 200, 51))
                    draw_text(f"Selected rod - {selected_rod[0]}", text_font, (255, 254, 255), 500, text_y + 17)
                    draw_text(f"Durability: {selected_rod[1]}     Luck: {selected_rod[4]}", text_font, (255, 254, 255), 500, text_y + 34)
                    draw_text(f"Press Enter to purchase", text_font, (255, 254, 255), 500, text_y + 51)
                    
            elif event.type == MOUSEBUTTONDOWN:
                break
        except IndexError:
            try:
                if event.type == KEYDOWN:
                    if key[pygame.K_RETURN] == True:
                        if int(balance.get("Coins")) >= int(selected_rod[2]):
                            balance["Coins"] -= int(selected_rod[2])
                            dict.clear(current_rod)
                            current_rod[selected_rod[0]] = [selected_rod[1], int(selected_rod[1]), int(selected_rod[4])]
                            draw_text(f"You bought a {selected_rod[0]}!", text_font, (255, 254, 255), 260, 15)
                            pygame.display.update()
                            time.sleep(1)
                            return balance, current_rod
                        else:
                            draw_text(f"Not enough money!", text_font, (255, 254, 255), 300, 17)
                            pygame.display.update()
                            time.sleep(1)
                            break
            except IndexError:
                pass

def show_help(screen):
    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))
    text_font = pygame.font.Font(os.path.join("textures", "pixellari.ttf"),16)
    pygame.event.clear()
    while True:
        pygame.display.update()
        event = pygame.event.wait()
        if event.type == MOUSEBUTTONDOWN:
            break
        pygame.draw.rect(screen, (0, 0, 0), (310, 65, 110, 36))
        pygame.draw.line(screen, (0, 0, 0), (325, 65), (325, 120))
        draw_text(f"Click here to", text_font, (255, 254, 255), 312, 69)
        draw_text(f"view your fish", text_font, (255, 254, 255), 313, 83)

        pygame.draw.rect(screen, (0, 0, 0), (190, 350, 103, 36))
        pygame.draw.line(screen, (0, 0, 0), (190, 355), (175, 355))
        draw_text(f"Click here to", text_font, (255, 254, 255), 192, 354)
        draw_text(f"sell your fish", text_font, (255, 254, 255), 194, 368)

        pygame.draw.rect(screen, (0, 0, 0), (190, 10, 123, 36))
        pygame.draw.line(screen, (0, 0, 0), (190, 15), (175, 15))
        draw_text(f"Click here to", text_font, (255, 254, 255), 192, 14)
        draw_text(f"buy fishing rods", text_font, (255, 254, 255), 193, 28)

if __name__ == "__main__":
    print("You ran functions.py, please run game.py")
