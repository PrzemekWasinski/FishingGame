# Fishing Game in Python
This is a fishing game I made in Python using Pygame during my first year at Univeristy, it has features such as catching/selling fish, money, buying different fishing rods with different benefits and fishing rod durability.

To try this game clone this repository or download the zip and run `FishingGame.exe`

# Fishing
Click on the water to begin fishing...

![fishing_screenshot](https://github.com/user-attachments/assets/090ddabe-5fe6-49f4-b5af-a0c2fcdf5afe)

When you hook onto a fish a circle will show up on the water, the circle radius is determined by the rarity of the fish. Keep your cursor within the circle while it moves around the water to catch the fish, the duration of this minigame is determined by the weight of the fish as bigger fish will have more energy.

# Adding your own fish and fishing rods
You can also add new fish and new fishing rods into the game by simply adding a new line in either `fish.csv` or `rods.csv` while following the parameters at the top of the file. Both `.csv` files can be found in the `databases` directory.

![fish_csv](https://github.com/user-attachments/assets/69cd9d5f-dcfd-4a4c-af22-743526fef008) ![rods_csv](https://github.com/user-attachments/assets/f2bb1bbe-416f-4441-9dd1-ae87d1d8a39d)

When adding a new fish inside `fish.csv` it will also need a 30x15 `.png` image inside `/textures/fish_images`, if you do not want to add an image just type in `"_blank.png"` in the image parameter.
