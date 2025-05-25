import pygame
import sys
import os
import math

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# Asset paths - Update these paths to match your actual file locations
# BACKGROUND_PATH = r"C:\\Users\\xxiao\\OneDrive - Asia Pacific University\\ShaolinBadminton\\Assests\\Background\\Background1\\Background1.jpg"
# TREE1_PATH = r"C:\\Users\\xxiao\\OneDrive - Asia Pacific University\\ShaolinBadminton\\Assests\\Effects\\Assets\\Tree1.png"   
# TREE2_PATH = r"C:\\Users\\xxiao\\OneDrive - Asia Pacific University\\ShaolinBadminton\\Assests\\Effects\\Assets\\Tree2.png"   
# BIRD_PATH = r"C:\\Users\\xxiao\\OneDrive - Asia Pacific University\\ShaolinBadminton\\Assests\\Effects\\Assets\\Bird2.png" 
# CLOUD1_PATH = r"C:\\Users\\xxiao\\OneDrive - Asia Pacific University\\ShaolinBadminton\\Assests\\Effects\\Assets\\Cloud1.png"
# CLOUD2_PATH = r"C:\\Users\\xxiao\\OneDrive - Asia Pacific University\\ShaolinBadminton\\Assests\\Effects\\Assets\\Cloud2.png"
# CLOUD3_PATH = r"C:\\Users\\xxiao\\OneDrive - Asia Pacific University\\ShaolinBadminton\\Assests\\Effects\\Assets\\Cloud3.png"
# CLOUD4_PATH = r"C:\\Users\\xxiao\\OneDrive - Asia Pacific University\\ShaolinBadminton\\Assests\\Effects\\Assets\\Cloud4.png"
# SUN_PATH = r"C:\\Users\\xxiao\\OneDrive - Asia Pacific University\\ShaolinBadminton\\Assests\\Effects\\Assets\\Sun.png"
# TEMPLE_PATH = r"C:\\Users\\xxiao\\OneDrive - Asia Pacific University\\ShaolinBadminton\\Assests\\Effects\\Assets\\Temple.png"
# LATERN1_PATH = r"C:\\Users\\xxiao\\OneDrive - Asia Pacific University\\ShaolinBadminton\\Assests\\Effects\\Assets\\GardenLamp.png"

# Asset directory setup
scriptDir = os.path.dirname(os.path.abspath(__file__))
background = os.path.join(scriptDir, "..", "Background")

# Asset paths
BACKGROUND_PATH = os.path.join(background, "Background", "Background1", "Background1.jpg")
MENU_CLOUD1_PATH = os.path.join(background, "Effects", "Assets", "Cloud1.png")
MENU_CLOUD2_PATH = os.path.join(background, "Effects", "Assets", "Cloud2.png")
MENU_GRASS_PATH = os.path.join(background, "Effects", "Assets", "Tree2.png")
TREE1_PATH = os.path.join(background, "Effects", "Assets", "Tree1.png")
TREE2_PATH = os.path.join(background, "Effects", "Assets", "Tree2.png")
BIRD_PATH = os.path.join(background, "Effects", "Assets", "Bird2.png")
CLOUD3_PATH = os.path.join(background, "Effects", "Assets", "Cloud3.png")
CLOUD4_PATH = os.path.join(background, "Effects", "Assets", "Cloud4.png")
SUN_PATH = os.path.join(background, "Effects", "Assets", "Sun.png")
TEMPLE_PATH = os.path.join(background, "Effects", "Assets", "Temple.png")
LATERN1_PATH = os.path.join(background, "Effects", "Assets", "GardenLamp.png")

# Load menu background
main_menu_bg = pygame.image.load(BACKGROUND_PATH)
main_menu_bg = pygame.transform.scale(main_menu_bg, (screen_width, screen_height))

# Load menu clouds
def load_scaled_image(path, width, height):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, (width, height))

menu_cloud1 = load_scaled_image(MENU_CLOUD1_PATH, 150, 80)
menu_cloud2 = load_scaled_image(MENU_CLOUD2_PATH, 200, 80)
menu_cloud1_x, menu_cloud1_y = 200, 100
menu_cloud2_x, menu_cloud2_y = 50, 20
menu_cloud1_speed = 0.3
menu_cloud2_speed = 0.2

# Load menu grass
grass_image_original = pygame.image.load(MENU_GRASS_PATH).convert_alpha()
menu_grass_data = [
    {"x": 100, "y": 770, "scale": 1.8, "angle": 0, "sway_speed": 0.015},
    {"x": 250, "y": 850, "scale": 1.7, "angle": 0, "sway_speed": 0.013},
    {"x": 900, "y": 740, "scale": 1.7, "angle": 0, "sway_speed": 0.017},
]

# Load menu trees
tree_image_original = pygame.image.load(TREE2_PATH).convert_alpha()
menu_tree_configs = [
    {"x": 100, "y": 500, "scale": 1.2, "speed": 0.009},
    {"x": 300, "y": 520, "scale": 1.0, "speed": 0.010},
    {"x": 800, "y": 510, "scale": 1.1, "speed": 0.008},
]
menu_tree_data = []
for config in menu_tree_configs:
    scaled = pygame.transform.scale(
        tree_image_original,
        (int(400 * config["scale"]), int(300 * config["scale"]))
    )
    menu_tree_data.append({
        "image": scaled,
        "x": config["x"],
        "y": config["y"],
        "angle": 0,
        "sway_speed": config["speed"]
    })

# Scene control
current_scene = "menu"

# Main loop
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            current_scene = "scene1"

    screen.fill((0, 0, 0))

    if current_scene == "menu":
        screen.blit(main_menu_bg, (0, 0))

        # Clouds
        menu_cloud1_x += menu_cloud1_speed
        menu_cloud2_x += menu_cloud2_speed
        if menu_cloud1_x > screen_width:
            menu_cloud1_x = -200
        if menu_cloud2_x > screen_width:
            menu_cloud2_x = -250
        screen.blit(menu_cloud1, (menu_cloud1_x, menu_cloud1_y))
        screen.blit(menu_cloud2, (menu_cloud2_x, menu_cloud2_y))

        # Trees
        for tree in menu_tree_data:
            tree["angle"] += tree["sway_speed"]
            sway = math.sin(tree["angle"]) * 2
            rotated = pygame.transform.rotate(tree["image"], sway)
            rect = rotated.get_rect(midbottom=(tree["x"] + tree["image"].get_width() // 2,
                                               tree["y"] + tree["image"].get_height()))
            screen.blit(rotated, rect.topleft)

        # Grass
        for g in menu_grass_data:
            g["angle"] += g["sway_speed"]
            sway = math.sin(g["angle"]) * 3
            scaled = pygame.transform.scale(grass_image_original, (int(120 * g["scale"]), int(80 * g["scale"])))
            rotated = pygame.transform.rotate(scaled, sway)
            rect = rotated.get_rect(midbottom=(g["x"], g["y"]))
            screen.blit(rotated, rect.topleft)

        # Menu text
        title_font = pygame.font.SysFont("arial", 48, bold=True)
        instruction_font = pygame.font.SysFont("arial", 32, bold=True)
        title_text = title_font.render("Welcome to Shaolin Badminton", True, (255, 255, 255))
        instruction_text = instruction_font.render("Press ENTER to Start", True, (255, 255, 255))
        screen.blit(title_text, title_text.get_rect(center=(screen_width // 2, screen_height // 2 + 60)))
        screen.blit(instruction_text, instruction_text.get_rect(center=(screen_width // 2, screen_height // 2 + 110)))

    elif current_scene == "scene1":
        screen.fill((50, 50, 50))
        scene_font = pygame.font.SysFont("arial", 36, bold=True)
        scene_text = scene_font.render("Scene 1 - Gameplay Screen Placeholder", True, (255, 255, 0))
        screen.blit(scene_text, scene_text.get_rect(center=(screen_width // 2, screen_height // 2)))

    pygame.display.flip()

pygame.quit()
sys.exit()