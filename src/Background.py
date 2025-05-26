import pygame
import sys
import os
import math
import random 

# Initialize Pygame
pygame.init()

# Get script directory and build asset paths dynamically
scriptDir = os.path.dirname(os.path.abspath(__file__))
assetBackground = os.path.join(scriptDir, "..", "Assests", "Background", "Background1")
assetEffects = os.path.join(scriptDir, "..", "Assests", "Effects", "Assets")

# Set up the display
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Game Window")

## Background 1
# Asset paths - Now using dynamic paths like the game.py
BACKGROUND_PATH = os.path.join(assetBackground, "Background1.jpg")
TREE1_PATH = os.path.join(assetEffects, "Tree1.png")   
TREE2_PATH = os.path.join(assetEffects, "Tree2.png")   
BIRD_PATH = os.path.join(assetEffects, "Bird2.png") 
CLOUD1_PATH = os.path.join(assetEffects, "Cloud1.png")
CLOUD2_PATH = os.path.join(assetEffects, "Cloud2.png")
CLOUD3_PATH = os.path.join(assetEffects, "Cloud3.png")
CLOUD4_PATH = os.path.join(assetEffects, "Cloud4.png")
SUN_PATH = os.path.join(assetEffects, "Sun.png")
TEMPLE_PATH = os.path.join(assetEffects, "Temple.png")
LATERN1_PATH = os.path.join(assetEffects, "GardenLamp.png")

def load_and_scale_image(path, width=None, height=None, scale_factor=None):
    try:
        image = pygame.image.load(path).convert_alpha()
        if scale_factor:
            original_width, original_height = image.get_size()
            new_width = int(original_width * scale_factor)
            new_height = int(original_height * scale_factor)
            image = pygame.transform.scale(image, (new_width, new_height))
        elif width and height:
            image = pygame.transform.scale(image, (width, height))
        return image
    except pygame.error as e:
        print(f"Could not load image {path}: {e}")
        return None

# Load all assets
background = load_and_scale_image(BACKGROUND_PATH, screen_width, screen_height)
tree1_large = load_and_scale_image(TREE1_PATH, scale_factor=1.8)
tree2_large = load_and_scale_image(TREE2_PATH, scale_factor=1.6)
bird1 = load_and_scale_image(BIRD_PATH, scale_factor=0.8)
bird2 = load_and_scale_image(BIRD_PATH, scale_factor=0.6)
bird3 = load_and_scale_image(BIRD_PATH, scale_factor=0.7)
bird4 = load_and_scale_image(BIRD_PATH, scale_factor=0.5)
sun = load_and_scale_image(SUN_PATH, scale_factor=0.4)
cloud2 = load_and_scale_image(CLOUD2_PATH, scale_factor=0.5)
cloud5 = load_and_scale_image(CLOUD1_PATH, scale_factor=0.3)
temple = load_and_scale_image(TEMPLE_PATH, scale_factor=0.4)

# Load lanterns and garden lamps
garden_lamp = load_and_scale_image(LATERN1_PATH, scale_factor=0.3)

if bird4:
    bird4 = pygame.transform.flip(bird4, True, False)

# Asset positions
asset_positions = {
    'tree1_large_left': (-50, screen_height - 520),
    'tree2_large_right': (screen_width - 200, screen_height - 500),
    'bird1': (100, 100),
    'bird2': (400, 80),
    'bird3': (650, 130),
    'bird4': (900, 110),
    'cloud2': (500, 10),
    'cloud5': (150, 50),
}

# Temple and lantern positions
if temple:
    temple_rect = temple.get_rect(center=(screen_width // 2, screen_height // 2 - 80))
    
    # Calculate lantern positions on temple roof
    temple_center_x = temple_rect.centerx
    temple_top_y = temple_rect.top
    
    # Position garden lamps beside the temple
    garden_lamp_left_pos = (temple_rect.left - 150, temple_rect.bottom - 160)
    garden_lamp_right_pos = (temple_rect.right - 20, temple_rect.bottom - 160)

# Bird movement variables
bird1_x = asset_positions['bird1'][0]
bird2_x = asset_positions['bird2'][0]
bird3_x = asset_positions['bird3'][0]
bird4_x = asset_positions['bird4'][0]
bird_speed1 = 0.7
bird_speed2 = 0.5
bird_speed3 = 0.3
bird_speed4 = -0.4

# Cloud movement variables
cloud2_x = asset_positions['cloud2'][0]
cloud5_x = asset_positions['cloud5'][0]
cloud_speed2 = 0.1
cloud_speed5 = 0.09

sun_cycle_duration = 250
sun_start_time = pygame.time.get_ticks()

def get_sun_position(current_time):
    """Calculate sun position for realistic sunrise/sunset motion"""
    elapsed = (current_time - sun_start_time) % (sun_cycle_duration * 100)
    progress = (elapsed / (sun_cycle_duration * 100))
    
    angle = progress * math.pi
    center_x = screen_width * (1 - progress)
    
    arc_height = 200
    min_y = 50
    max_y = min_y + arc_height
    
    sun_y = max_y - (arc_height * math.sin(angle))
    
    return center_x, sun_y, progress

def get_sky_lighting(progress):
    """Calculate sky lighting overlay based on sun position"""
    if progress <= 0.1:
        darkness = 150
    elif progress <= 0.3:
        darkness = int(150 * (0.3 - progress) / 0.2)
    elif progress <= 0.7:
        darkness = 0
    elif progress <= 0.9:
        darkness = int(150 * (progress - 0.7) / 0.2)
    else:
        darkness = 150
    
    return darkness

def should_lights_be_on(progress):
    """Determine if lights should be on based on sun position"""
    # Lights are on during dark periods (before sunrise and after sunset)
    return progress <= 0.2 or progress >= 0.8

def draw_light_glow(screen, position, radius, color, alpha):
    glow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)

    for i in range(radius, 0, -2):  # Tighter spacing for stronger glow
        current_alpha = int(alpha * (i / radius) * 2)  # Boost intensity multiplier
        current_alpha = min(current_alpha, 255)  # Clamp max alpha
        current_color = (*color, current_alpha)
        pygame.draw.circle(glow_surface, current_color, (radius, radius), i)
    
    screen.blit(glow_surface, (position[0] - radius, position[1] - radius))


def apply_sky_lighting(screen, darkness_level):
    """Apply lighting overlay to simulate day/night cycle"""
    if darkness_level > 0:
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(darkness_level)
        overlay.fill((20, 20, 40))
        screen.blit(overlay, (0, 0))

# Load main menu assets
main_menu_bg = pygame.image.load(os.path.join(scriptDir, "..", "Assests", "Background", "MainMenu", "mainMenu.webp"))
main_menu_bg = pygame.transform.scale(main_menu_bg, (screen_width, screen_height))

menu_cloud1 = pygame.transform.scale(pygame.image.load(os.path.join(scriptDir, "..", "Assests", "Background", "MainMenu", "cloud2.png")).convert_alpha(),(150, 80))
menu_cloud2 = pygame.transform.scale(pygame.image.load(os.path.join(scriptDir, "..", "Assests", "Background", "MainMenu", "cloud2.png")).convert_alpha(),(200, 80))
menu_cloud1_x, menu_cloud1_y = 200, 100
menu_cloud2_x, menu_cloud2_y = 50, 20
menu_cloud1_speed = 0.3
menu_cloud2_speed = 0.2

menu_grass_image_original = pygame.image.load(os.path.join(scriptDir, "..", "Assests", "Background", "MainMenu", "grass.png")).convert_alpha()

menu_grass_data = [
    {"x": 100, "y": 770, "scale": 1.8, "angle": 0, "sway_speed": 0.015},
    {"x": 250, "y": 850, "scale": 1.7, "angle": 0, "sway_speed": 0.013},
    {"x": 900, "y": 740, "scale": 1.7, "angle": 0, "sway_speed": 0.017},
]

# Load Background2 scene assets
background2 = pygame.image.load(os.path.join(scriptDir, "..", "Assests", "Background", "Background2", "Background2.jpg"))
background2 = pygame.transform.scale(background2, (screen_width, screen_height))

lantern = pygame.image.load(os.path.join(scriptDir, "..", "Assests", "Background", "Background2", "lantern.png")).convert_alpha()
lantern = pygame.transform.scale(lantern, (60, 80))

lake = pygame.image.load(os.path.join(scriptDir, "..", "Assests", "Background", "Background2", "lakePool.png")).convert_alpha()
lake = pygame.transform.scale(lake, (250, 140))
lake_x, lake_y = 750, 560

fish_image = pygame.image.load(os.path.join(scriptDir, "..", "Assests", "Background", "Background2", "fish.png")).convert_alpha()
fish_image = pygame.transform.scale(fish_image, (50, 30))

grass_image_original = pygame.image.load(os.path.join(scriptDir, "..", "Assests", "Background", "Background2", "grass.png")).convert_alpha()

tree_image_original = pygame.image.load(os.path.join(scriptDir, "..", "Assests", "Background", "Background2", "tree.png")).convert_alpha()

cloud1 = pygame.transform.scale(pygame.image.load(os.path.join(scriptDir, "..", "Assests", "Background", "Background2", "cloud2.png")).convert_alpha(),(200, 100))
scene_cloud2 = pygame.transform.scale(pygame.image.load(os.path.join(scriptDir, "..", "Assests", "Background", "Background2", "cloud2.png")).convert_alpha(),(250, 120))
cloud1_x, cloud1_y = 300, 40
scene_cloud2_x, scene_cloud2_y = 200, 160
cloud1_speed = 0.3
scene_cloud2_speed = 0.2

tree_configs = [
    {"x": -250, "y": 230, "scale": 1.6, "speed": 0.011},
    {"x": 40, "y": 350, "scale": 1.1, "speed": 0.012},
    {"x": -70, "y": 300, "scale": 1.3, "speed": 0.009},
    {"x": -90, "y": 360, "scale": 1.1, "speed": 0.010}
]
tree_data = []
for config in tree_configs:
    scaled = pygame.transform.scale(tree_image_original, (int(400 * config["scale"]), int(300 * config["scale"])))
    tree_data.append({"image": scaled, "x": config["x"], "y": config["y"], "angle": 0, "sway_speed": config["speed"]})

grass_patches = [
    {"tree_index": 0, "offset_x": -10, "width": 150, "height": 110},
    {"tree_index": 0, "offset_x": 20, "width": 180, "height": 100},
    {"tree_index": 1, "offset_x": 0, "width": 170, "height": 105},
    {"tree_index": 2, "offset_x": -15, "width": 180, "height": 120},
    {"tree_index": 2, "offset_x": 10, "width": 170, "height": 115},
    {"tree_index": 3, "offset_x": 5, "width": 145, "height": 90}
]

right_lantern_base_x = 540
left_lantern_base_x = 380
lantern_y = 420
swing_angle = 20

fish_list = []
for i in range(3):
    fish_list.append({
        "origin_x": 800 + i * 40,
        "origin_y": 630,
        "angle": random.uniform(0, math.pi),
        "radius": 70,
        "speed": 0.03 + i * 0.01,
        "direction": 1 if i % 2 == 0 else -1
    })


clock = pygame.time.Clock()

# Main loop
running = True
current_scene = "menu"

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and current_scene == "menu":
                current_scene = "scene1"

    screen.fill((0, 0, 0))

    if current_scene == "menu":
        screen.blit(main_menu_bg, (0, 0))

        # Animate clouds
        menu_cloud1_x += menu_cloud1_speed
        menu_cloud2_x += menu_cloud2_speed
        if menu_cloud1_x > screen_width:
            menu_cloud1_x = -200
        if menu_cloud2_x > screen_width:
            menu_cloud2_x = -250
        screen.blit(menu_cloud1, (menu_cloud1_x, menu_cloud1_y))
        screen.blit(menu_cloud2, (menu_cloud2_x, menu_cloud2_y))

        # Animate grass
        for g in menu_grass_data:
            g["angle"] += g["sway_speed"]
            sway = math.sin(g["angle"]) * 3
            scaled = pygame.transform.scale(menu_grass_image_original, (int(120 * g["scale"]), int(80 * g["scale"])))
            rotated = pygame.transform.rotate(scaled, sway)
            rect = rotated.get_rect(midbottom=(g["x"], g["y"]))
            screen.blit(rotated, rect.topleft)

        # Trees
        # for tree in menu_tree_data:
        #     tree["angle"] += tree["sway_speed"]
        #     sway = math.sin(tree["angle"]) * 2
        #     rotated = pygame.transform.rotate(tree["image"], sway)
        #     rect = rotated.get_rect(midbottom=(tree["x"] + tree["image"].get_width() // 2,
        #                                        tree["y"] + tree["image"].get_height()))
        #     screen.blit(rotated, rect.topleft)

        # Title and instruction
        title_font = pygame.font.SysFont("arial", 48, bold=True)
        instruction_font = pygame.font.SysFont("arial", 32, bold=True)
        title_text = title_font.render("Welcome to Shaolin Badminton", True, (255, 255, 255))
        instruction_text = instruction_font.render("Press ENTER to Start", True, (255, 255, 255))
        screen.blit(title_text, title_text.get_rect(center=(screen_width // 2, screen_height // 2 + 60)))
        screen.blit(instruction_text, instruction_text.get_rect(center=(screen_width // 2, screen_height // 2 + 110)))

    elif current_scene == "scene1":
        screen.blit(background2, (0, 0))

        # Clouds
        cloud1_x += cloud1_speed
        scene_cloud2_x += scene_cloud2_speed
        if cloud1_x > screen_width:
            cloud1_x = -200
        if scene_cloud2_x > screen_width:
            scene_cloud2_x = -250
        screen.blit(cloud1, (cloud1_x, cloud1_y))
        screen.blit(scene_cloud2, (scene_cloud2_x, scene_cloud2_y))

        # Trees
        for tree in tree_data:
            tree["angle"] += tree["sway_speed"]
            sway = math.sin(tree["angle"]) * 2
            rotated = pygame.transform.rotate(tree["image"], sway)
            rect = rotated.get_rect(midbottom=(tree["x"] + tree["image"].get_width() // 2,
                                               tree["y"] + tree["image"].get_height()))
            screen.blit(rotated, rect.topleft)

        # Grass
        for patch in grass_patches:
            tree = tree_data[patch["tree_index"]]
            sway = math.sin(tree["angle"]) * 2
            rotated = pygame.transform.rotate(tree["image"], sway)
            rect = rotated.get_rect(midbottom=(tree["x"] + tree["image"].get_width() // 2,
                                               tree["y"] + tree["image"].get_height()))
            grass_img = pygame.transform.scale(grass_image_original, (patch["width"], patch["height"]))
            grass_rect = grass_img.get_rect(midbottom=(rect.centerx + patch["offset_x"], rect.bottom))
            screen.blit(grass_img, grass_rect.topleft)

        # Lake
        screen.blit(lake, (lake_x, lake_y))

        # Lanterns
        swing_angle += 0.05
        swing_offset = math.sin(swing_angle) * 10
        screen.blit(lantern, (left_lantern_base_x - swing_offset, lantern_y))
        screen.blit(lantern, (right_lantern_base_x + swing_offset, lantern_y))

        # Fish
        for f in fish_list:
            f["angle"] += f["speed"]
            if f["angle"] > math.pi:
                f["angle"] = 0
                f["direction"] *= -1
                f["origin_x"] += 3 * f["direction"]
            fx = f["origin_x"] + math.cos(f["angle"]) * f["radius"] * f["direction"]
            fy = f["origin_y"] - math.sin(f["angle"]) * f["radius"]
            fish_draw = pygame.transform.flip(fish_image, True, False) if f["direction"] == -1 else fish_image
            screen.blit(fish_draw, (fx, fy))

    pygame.display.flip()

pygame.quit()
sys.exit()
