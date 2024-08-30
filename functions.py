import pygame
from pygame.locals import *
import os
import time
import random

pygame.init()
clock = pygame.time.Clock()

sand = pygame.image.load(os.path.join("textures", "images", "_sand.png"))
rod_store = pygame.image.load(os.path.join("textures", "images", "_rod_store.png"))
dock = pygame.image.load(os.path.join("textures", "images", "_dock.png"))
bucket = pygame.image.load(os.path.join("textures", "images", "_bucket.png"))
bobber = pygame.image.load(os.path.join("textures", "images", "_bobber.png"))

sand_image = sand.get_rect(topleft=(-6, 0))
shop_image = rod_store.get_rect(center=(120, 110))
dock_image = dock.get_rect(center=(355, 365))
bucket_image = bucket.get_rect(center=(475, 410))

def refresh_window(window, balance, current_rod, circle_x, circle_y, radius):

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        window.blit(img, (x, y))
    text_font = pygame.font.Font(os.path.join("textures", "pixellari.ttf"),16)

    window.blit(sand, (sand_image))
    window.blit(rod_store, (shop_image))
    window.blit(dock, (dock_image))
    window.blit(bucket, (bucket_image))
    fisherman = pygame.image.load(os.path.join("textures", "images", "_fisherman_fishing.png"))
    line_x = 440
    line_y = 339
    pygame.draw.rect(window, (255, 255, 255), (0, 0, 24, 24))
    draw_text("?", text_font, (255, 0, 0), 8, 5)
    
    if circle_x and circle_y != 0:
        if circle_x < 350 and circle_y > 220:
            fisherman = pygame.image.load(os.path.join("textures", "fisherman_sprite", "fisherman_cast", "fisherman_max_left.png"))
            line_x = 417
            line_y = 345
        elif circle_x > 560 and circle_y > 220:
            fisherman = pygame.image.load(os.path.join("textures", "fisherman_sprite", "fisherman_cast", "fisherman_max_right.png"))
            line_x = 464
            line_y = 345
        elif circle_x < 390:
            fisherman = pygame.image.load(os.path.join("textures", "fisherman_sprite", "fisherman_cast", "fisherman_left.png"))
            line_x = 436
            line_y = 339
        elif circle_x > 480:
            fisherman = pygame.image.load(os.path.join("textures", "fisherman_sprite", "fisherman_cast", "fisherman_right.png"))
            line_x = 443
            line_y = 339
             
        pygame.draw.circle(window, (255, 255, 255), (circle_x, circle_y), radius, 2)
        pygame.draw.line(window, (0, 0, 0), (line_x, line_y), (circle_x, circle_y))

    fisherman_image = fisherman.get_rect(topleft=(400, 325))
    window.blit(fisherman, (fisherman_image))    

    draw_text(f"Balance: ${balance['Coins']}", text_font, (255, 254, 255), 660, 15)
    draw_text(f"{next(iter(current_rod))}: {round(int(next(iter(current_rod.values()))[0]))} / {next(iter(current_rod.values()))[1]}", text_font, (255, 254, 255), 620, 470)
    pygame.display.flip()
    clock.tick(60)

def catch_fish(current_rod, inventory, fish_list, window, balance):
    
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

        def update(self, speed):
            window.blit(dock, (dock_image))
            window.blit(bucket, (bucket_image))
            draw_text(f"Balance: ${balance['Coins']}", text_font, (255, 254, 255), 660, 15)
            draw_text(f"{next(iter(current_rod))}: {round(int(next(iter(current_rod.values()))[0]))} / {next(iter(current_rod.values()))[1]}", text_font, (255, 254, 255), 620, 470)
            self.current_sprite += speed
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
            self.image = self.sprites[int(self.current_sprite)]

    moving_sprites = pygame.sprite.Group()
    water = Water(0, 0)
    moving_sprites.add(water)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    bobber_image = bobber.get_rect(center=(mouse_x, mouse_y))
    circle_x = mouse_x
    circle_y = mouse_y

    while True:
        if int(next(iter(current_rod.values()))[0]) <= 0:
            draw_text("Fishing rod is broken", text_font, (255, 254, 255), 320, 15)
            pygame.display.update()
            time.sleep(1)
            break

        else:
            pygame.draw.line(window, (0, 0, 0), (440, 339), (mouse_x, mouse_y))
            window.blit(bobber, (bobber_image))
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
                    pass 
                
            fish = selected_fish[0]
            weight = round(random.uniform(int(selected_fish[1]), int(selected_fish[2])), 1)
            price = weight * int(selected_fish[3])
            rarity = selected_fish[4]
            radius = (100 - int(rarity)) / 2
            moving_sprites.draw(window)
            moving_sprites.update(1)
            time.sleep(1)
            refresh_window(window, balance, current_rod, 0, 0, 0)

            if random.randint(1, 100) <= next(iter(current_rod.values()))[2]:
                fishing_passed = True
                for i in range(round(weight / 2) + 1):
                    direction_x = random.randint(1, 3) - 2
                    direction_y = random.randint(1, 3) - 2
                    for i in range(round(weight) * 25):             
                        if circle_x > 725:
                            if fishing_passed:
                                refresh_window(window, balance, current_rod, circle_x, circle_y, radius)
                            direction_x = -1 - random.randint(0, 1)
                            circle_x += direction_x
                            choice = random.randint(1, 2)
                            if choice == 1:
                                direction_y += 1 + random.randint(0, 1)
                            else:
                                direction_y -= 1 - random.randint(0, 1)                           
                            
                        elif circle_x < 330:
                            if fishing_passed:
                                refresh_window(window, balance, current_rod, circle_x, circle_y, radius)
                            direction_x = 1 + random.randint(0, 1)
                            circle_x += direction_x
                            choice = random.randint(1, 2)
                            if choice == 1:
                                direction_y += 1 + random.randint(0, 1)
                            else:
                                direction_y -= 1 - random.randint(0, 1)

                        elif circle_y > 280:
                            if fishing_passed:
                                refresh_window(window, balance, current_rod, circle_x, circle_y, radius)
                            direction_y = -1 - random.randint(0, 1)
                            circle_y += direction_y
                            choice = random.randint(1, 2)
                            if choice == 1:
                                direction_x += 1 + random.randint(0, 1)
                            else:
                                direction_x -= 1 - random.randint(0, 1)
                            
                        elif circle_y < 85:
                            if fishing_passed:
                                refresh_window(window, balance, current_rod, circle_x, circle_y, radius)
                            direction_y = 1 + random.randint(0, 1)
                            circle_y += direction_y
                            choice = random.randint(1, 2)
                            if choice == 1:
                                direction_x += 1 + random.randint(0, 1)
                            else:
                                direction_x -= 1 - random.randint(0, 1)
     
                        else:
                            if fishing_passed:
                                refresh_window(window, balance, current_rod, circle_x, circle_y, radius)
                            if direction_x == 0:
                                choice = random.randint(1, 2)
                                if choice == 1:
                                    direction_x += 1
                                else:
                                    direction_x -= 1

                            if direction_y == 0:
                                choice = random.randint(1, 2)
                                if choice == 1:
                                    direction_y += 1 + random.randint(0, 1)
                                else:
                                    direction_y -= 1 - random.randint(0, 1)

                            circle_x += direction_x
                            circle_y += direction_y

                        pygame.event.clear()
                        current_mouse_x, current_mouse_y = pygame.mouse.get_pos()
                        if current_mouse_x + radius > circle_x and current_mouse_x - radius < circle_x:
                            if current_mouse_y + radius > circle_y and current_mouse_y - radius < circle_y:
                                moving_sprites.update(0.03)
                                moving_sprites.draw(window)
                                pygame.draw.circle(window, (255, 255, 255), (circle_x, circle_y), radius, 2)
                                refresh_window(window, balance, current_rod, circle_x, circle_y, radius)
                                moving_sprites.update(0.015)
                                time.sleep(0.015)
                            else:
                                fishing_passed = False
                                break
                        else:
                            fishing_passed = False
                            break

                if fishing_passed == True:
                    if fish in inventory:
                        inventory[fish][0] += weight
                        inventory[fish][1] += price
                    else:
                        inventory[fish] = [weight, price]
                    next(iter(current_rod.values()))[0] = int(next(iter(current_rod.values()))[0]) - weight
                    moving_sprites.draw(window)
                    draw_text(f"You cought a {weight}kg {fish}", text_font, (255, 254, 255), 350, 15)

                    try:
                        display_fish = pygame.image.load(os.path.join("textures", "fish_images", f"_{fish.lower()}.png"))
                        display_fish_image = display_fish.get_rect(center=(330, 22))
                        window.blit(display_fish, (display_fish_image))
                    except FileNotFoundError:
                        display_blank = pygame.image.load(os.path.join("textures", "fish_images", "_blank.png"))
                        display_blank_image = display_blank.get_rect(center=(330, 22))
                        window.blit(display_blank, (display_blank_image))
                    refresh_window(window, balance, current_rod, circle_x, circle_y, radius)
                    pygame.display.update()
                    time.sleep(1)
                    return current_rod, inventory, fish_list
                    
                else:
                    break
            else:
                pass

def show_inventory(inventory, window):

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        window.blit(img, (x, y))
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
            pygame.draw.rect(window, (0, 0, 0), (595, 5, 200, 17))
            draw_text("Your fish:", text_font, (255, 254, 255), 600, 5)

            for key, value in inventory.items():
                text_y += 15
                rect_y += 15
                pygame.draw.rect(window, (0, 0, 0), (595, rect_y, 200, 15))
                draw_text(f"{key} {round(value[0], 1)}kg (${round(value[1])})", text_font, (255, 254, 255), 625, text_y)

                try:
                    display_fish = pygame.image.load(os.path.join("textures", "fish_images", f"_{key.lower()}.png"))
                    display_fish_image = display_fish.get_rect(center=(610, text_y + 6))
                    window.blit(display_fish, (display_fish_image))
                except FileNotFoundError:
                    display_blank = pygame.image.load(os.path.join("textures", "fish_images", "_blank.png"))
                    display_blank_image = display_blank.get_rect(center=(610, text_y + 6))
                    window.blit(display_blank, (display_blank_image))

            if event.type == MOUSEBUTTONDOWN:
                break

            elif event.type == pygame.QUIT:
                pygame.quit()

            pygame.display.update()

def sell(balance, inventory, window):

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        window.blit(img, (x, y))
    text_font = pygame.font.Font(os.path.join("textures", "pixellari.ttf"),16)

    if len(inventory) == 0:
        draw_text("You have no fish to sell", text_font, (255, 254, 255), 320, 15)
        pygame.display.update()
        time.sleep(1)

    else:
        for value in inventory.values():
            balance["Coins"] += round(value[1])
        dict.clear(inventory)
        draw_text(f"All fish sold!", text_font, (255, 254, 255), 365, 15)
        pygame.display.update()
        time.sleep(1)
    return balance, inventory

def shop(balance, current_rod, rods_list, window):

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        window.blit(img, (x, y))
    text_font = pygame.font.Font(os.path.join("textures", "pixellari.ttf"),16)

    selected_rod = []
    for value in balance.values():
        pygame.draw.rect(window, (0, 0, 0), (580, 5, 215, 17))
        draw_text(f"Balance: ${value}", text_font, (255, 254, 255), 585, 5)
    text_y = 5
    rect_y = 5

    for rod in rods_list:
        text_y += 15
        rect_y += 15
        pygame.draw.rect(window, (0, 0, 0), (580, rect_y, 215, 17))
        draw_text(f"{rod[3]} - {rod[0]}: (${rod[2]})", text_font, (255, 254, 255), 585, text_y)
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
                    pygame.draw.rect(window, (0, 0, 0), (580, rect_y + 17, 215, 51))
                    draw_text(f"Selected rod - {selected_rod[0]}", text_font, (255, 254, 255), 585, text_y + 17)
                    draw_text(f"Durability: {selected_rod[1]}     Luck: {selected_rod[4]}", text_font, (255, 254, 255), 585, text_y + 34)
                    draw_text(f"Press Enter to purchase", text_font, (255, 254, 255), 585, text_y + 51)
            elif event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == MOUSEBUTTONDOWN:
                break

        except IndexError:
            try:
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == KEYDOWN:
                    if key[pygame.K_RETURN] == True:
                        if int(balance.get("Coins")) >= int(selected_rod[2]):
                            balance["Coins"] -= int(selected_rod[2])
                            dict.clear(current_rod)
                            current_rod[selected_rod[0]] = [selected_rod[1], int(selected_rod[1]), int(selected_rod[4])]
                            draw_text(f"You bought a {selected_rod[0]}!", text_font, (255, 254, 255), 300, 15)
                            pygame.display.update()
                            time.sleep(1)
                            return balance, current_rod
                        else:
                            draw_text("Not enough money!", text_font, (255, 254, 255), 300, 17)
                            pygame.display.update()
                            time.sleep(1)
                            break
            except IndexError:
                pass

def show_help(window):

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        window.blit(img, (x, y))
    text_font = pygame.font.Font(os.path.join("textures", "pixellari.ttf"),16)
    
    pygame.event.clear()
    while True:
        pygame.display.update()
        event = pygame.event.wait()
        if event.type == MOUSEBUTTONDOWN:
            break
        elif event.type == pygame.QUIT:
                pygame.quit()
        else:
            pygame.draw.rect(window, (0, 0, 0), (455, 450, 110, 36))
            pygame.draw.line(window, (0, 0, 0), (475, 450), (475, 425))
            draw_text(f"Click here to", text_font, (255, 254, 255), 458, 454)
            draw_text(f"view your fish", text_font, (255, 254, 255), 459, 468)

            pygame.draw.rect(window, (0, 0, 0), (280, 285, 103, 36))
            pygame.draw.line(window, (0, 0, 0), (300, 351), (300, 290))
            draw_text(f"Click here to", text_font, (255, 254, 255), 283, 289)
            draw_text(f"sell your fish", text_font, (255, 254, 255), 284, 303)

            pygame.draw.rect(window, (0, 0, 0), (230, 50, 123, 36))
            pygame.draw.line(window, (0, 0, 0), (208, 59), (230, 59))
            draw_text(f"Click here to", text_font, (255, 254, 255), 232, 54)
            draw_text(f"buy fishing rods", text_font, (255, 254, 255), 233, 68)

            pygame.draw.rect(window, (0, 0, 0), (550, 200, 228, 68))
            pygame.draw.line(window, (0, 0, 0), (565, 200), (565, 290))
            draw_text(f"Click the water to start fishing,", text_font, (255, 254, 255), 554, 204)
            draw_text(f"keep your cursor within the", text_font, (255, 254, 255), 556, 219)
            draw_text(f"white circle until the fish gets", text_font, (255, 254, 255), 555, 234)
            draw_text(f"tired out. Good luck!", text_font, (255, 254, 255), 555, 249)

if __name__ == "__main__":
    os.system("cls")
    print("You ran functions.py, please run game.py")
