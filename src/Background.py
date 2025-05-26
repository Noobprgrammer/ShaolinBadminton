import pygame
import sys
import os
import math
import random 

# Initialize Pygame with proper mixer setup
pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.init()

# Get script directory and build asset paths dynamically
scriptDir = os.path.dirname(os.path.abspath(__file__))

# Try both "Assets" and "Assests" spellings
assets_folder = None
for folder_name in ["Assets", "Assests"]:
    test_path = os.path.join(scriptDir, "..", folder_name)
    if os.path.exists(test_path):
        assets_folder = test_path
        break

if not assets_folder:
    print("Warning: Neither 'Assets' nor 'Assests' folder found!")
    assets_folder = os.path.join(scriptDir, "..", "Assets")

assetBackground = os.path.join(assets_folder, "Background", "Background1")
assetEffects = os.path.join(assets_folder, "Effects", "Assets")
assetSound = os.path.join(assets_folder, "Sound")

# Set up the display
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Shaolin Badminton - Enhanced")

def init_background_music():
    """Initialize and start playing background music for the main menu"""
    try:
        # Check if pygame mixer is available
        if not pygame.mixer.get_init():
            print("Mixer not initialized, initializing now...")
            pygame.mixer.init()
        
        # Try multiple file formats and paths
        music_files = ["BackgroundMusic.mp3", "BackgroundMusic.ogg", "BackgroundMusic.wav"]
        music_path = None
        
        print(f"Looking for music in: {assetSound}")
        
        if os.path.exists(assetSound):
            print(f"Sound directory exists. Files: {os.listdir(assetSound)}")
            for filename in music_files:
                test_path = os.path.join(assetSound, filename)
                if os.path.exists(test_path):
                    music_path = test_path
                    print(f"Found music file: {music_path}")
                    break
        else:
            print(f"Sound directory doesn't exist: {assetSound}")
            return False
        
        if not music_path:
            print(f"No music file found. Looked for: {music_files}")
            return False
        
        # Load and play the background music
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.3)  # Lower volume
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely
        
        print("Background music started successfully")
        return True
        
    except pygame.error as e:
        print(f"Pygame error loading background music: {e}")
        print("Tip: Try converting your music to .ogg format for better compatibility")
        return False
    except Exception as e:
        print(f"Unexpected error loading background music: {e}")
        return False

def stop_background_music():
    """Stop the background music"""
    pygame.mixer.music.stop()

def set_music_volume(volume):
    """Set the music volume (0.0 to 1.0)"""
    pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))

def pause_music():
    """Pause the background music"""
    pygame.mixer.music.pause()

def unpause_music():
    """Resume the background music"""
    pygame.mixer.music.unpause()

def toggle_music():
    """Toggle music on/off"""
    if pygame.mixer.music.get_busy():
        pause_music()
        return False
    else:
        unpause_music()
        return True

# Initialize music
music_initialized = init_background_music()
music_playing = music_initialized

## Background 1 Assets
# Asset paths
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

# Load all assets for Background1
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

# Tree swaying variables for Background1
tree1_sway_angle = 0
tree2_sway_angle = 0
tree1_sway_speed = 0.008
tree2_sway_speed = 0.010

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
    return progress <= 0.2 or progress >= 0.8

def draw_light_glow(screen, position, radius, color, alpha):
    glow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)

    for i in range(radius, 0, -2):
        current_alpha = int(alpha * (i / radius) * 2)
        current_alpha = min(current_alpha, 255)
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
try:
    main_menu_bg = pygame.image.load(os.path.join(assets_folder, "Background", "MainMenu", "mainMenu.webp"))
    main_menu_bg = pygame.transform.scale(main_menu_bg, (screen_width, screen_height))
except:
    # Fallback if main menu background doesn't exist
    main_menu_bg = pygame.Surface((screen_width, screen_height))
    main_menu_bg.fill((50, 100, 150))

try:
    menu_cloud1 = pygame.transform.scale(pygame.image.load(os.path.join(assets_folder, "Background", "MainMenu", "cloud2.png")).convert_alpha(),(150, 80))
    menu_cloud2 = pygame.transform.scale(pygame.image.load(os.path.join(assets_folder, "Background", "MainMenu", "cloud2.png")).convert_alpha(),(200, 80))
except:
    menu_cloud1 = pygame.Surface((150, 80), pygame.SRCALPHA)
    menu_cloud2 = pygame.Surface((200, 80), pygame.SRCALPHA)
    menu_cloud1.fill((255, 255, 255, 100))
    menu_cloud2.fill((255, 255, 255, 100))

menu_cloud1_x, menu_cloud1_y = 200, 100
menu_cloud2_x, menu_cloud2_y = 50, 20
menu_cloud1_speed = 0.3
menu_cloud2_speed = 0.2

try:
    menu_grass_image_original = pygame.image.load(os.path.join(assets_folder, "Background", "MainMenu", "grass.png")).convert_alpha()
except:
    menu_grass_image_original = None

menu_grass_data = [
    {"x": 100, "y": 770, "scale": 1.8, "angle": 0, "sway_speed": 0.015},
    {"x": 250, "y": 850, "scale": 1.7, "angle": 0, "sway_speed": 0.013},
    {"x": 900, "y": 740, "scale": 1.7, "angle": 0, "sway_speed": 0.017},
]

# Load Background2 scene assets
try:
    background2 = pygame.image.load(os.path.join(assets_folder, "Background", "Background2", "Background2.jpg"))
    background2 = pygame.transform.scale(background2, (screen_width, screen_height))
except:
    background2 = pygame.Surface((screen_width, screen_height))
    background2.fill((30, 80, 120))

try:
    lantern = pygame.image.load(os.path.join(assets_folder, "Background", "Background2", "lantern.png")).convert_alpha()
    lantern = pygame.transform.scale(lantern, (60, 80))
except:
    lantern = None

try:
    lake = pygame.image.load(os.path.join(assets_folder, "Background", "Background2", "lakePool.png")).convert_alpha()
    lake = pygame.transform.scale(lake, (250, 140))
except:
    lake = None

lake_x, lake_y = 750, 560

try:
    fish_image = pygame.image.load(os.path.join(assets_folder, "Background", "Background2", "fish.png")).convert_alpha()
    fish_image = pygame.transform.scale(fish_image, (50, 30))
except:
    fish_image = None

try:
    grass_image_original = pygame.image.load(os.path.join(assets_folder, "Background", "Background2", "grass.png")).convert_alpha()
except:
    grass_image_original = None

try:
    tree_image_original = pygame.image.load(os.path.join(assets_folder, "Background", "Background2", "tree.png")).convert_alpha()
except:
    tree_image_original = None

try:
    cloud1 = pygame.transform.scale(pygame.image.load(os.path.join(assets_folder, "Background", "Background2", "cloud2.png")).convert_alpha(),(200, 100))
    scene_cloud2 = pygame.transform.scale(pygame.image.load(os.path.join(assets_folder, "Background", "Background2", "cloud2.png")).convert_alpha(),(250, 120))
except:
    cloud1 = pygame.Surface((200, 100), pygame.SRCALPHA)
    scene_cloud2 = pygame.Surface((250, 120), pygame.SRCALPHA)
    cloud1.fill((255, 255, 255, 100))
    scene_cloud2.fill((255, 255, 255, 100))

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
if tree_image_original:
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
if fish_image:
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
current_volume = 0.3

print("\n=== GAME CONTROLS ===")
print("ENTER: Switch scenes")
print("M: Toggle music on/off")
print("+/=: Volume up")
print("-: Volume down")
print("ESC: Quit game")
print("====================\n")

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RETURN:
                if current_scene == "menu":
                    current_scene = "background1"
                elif current_scene == "background1":
                    current_scene = "background2"
                elif current_scene == "background2":
                    current_scene = "menu"
            elif event.key == pygame.K_m:
                music_playing = toggle_music()
                print(f"Music {'resumed' if music_playing else 'paused'}")
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                current_volume = min(1.0, current_volume + 0.1)
                set_music_volume(current_volume)
                print(f"Volume: {current_volume:.1f}")
            elif event.key == pygame.K_MINUS:
                current_volume = max(0.0, current_volume - 0.1)
                set_music_volume(current_volume)
                print(f"Volume: {current_volume:.1f}")

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
        if menu_grass_image_original:
            for g in menu_grass_data:
                g["angle"] += g["sway_speed"]
                sway = math.sin(g["angle"]) * 3
                scaled = pygame.transform.scale(menu_grass_image_original, (int(120 * g["scale"]), int(80 * g["scale"])))
                rotated = pygame.transform.rotate(scaled, sway)
                rect = rotated.get_rect(midbottom=(g["x"], g["y"]))
                screen.blit(rotated, rect.topleft)

        # Title and instructions
        title_font = pygame.font.SysFont("arial", 48, bold=True)
        instruction_font = pygame.font.SysFont("arial", 28, bold=True)
        small_font = pygame.font.SysFont("arial", 20)
        
        title_text = title_font.render("Shaolin Badminton", True, (255, 255, 255))
        instruction_text = instruction_font.render("Press ENTER to Start", True, (255, 255, 255))
        controls_text = small_font.render("Controls: M=Music, +/- =Volume, ESC=Quit", True, (200, 200, 200))
        
        screen.blit(title_text, title_text.get_rect(center=(screen_width // 2, screen_height // 2 + 60)))
        screen.blit(instruction_text, instruction_text.get_rect(center=(screen_width // 2, screen_height // 2 + 110)))
        screen.blit(controls_text, controls_text.get_rect(center=(screen_width // 2, screen_height // 2 + 150)))

        # Music status
        music_status = "♪ ON" if music_playing else "♪ OFF"
        status_text = small_font.render(f"Music: {music_status} | Volume: {current_volume:.1f}", True, (255, 255, 0))
        screen.blit(status_text, (10, 10))

    elif current_scene == "background1":
        # Render Background1 - Temple scene with sun cycle
        if background:
            screen.blit(background, (0, 0))

        # Sun animation
        current_time = pygame.time.get_ticks()
        sun_x, sun_y, progress = get_sun_position(current_time)
        
        # Draw sun
        if sun:
            sun_rect = sun.get_rect(center=(sun_x, sun_y))
            screen.blit(sun, sun_rect)

        # Animate clouds
        cloud2_x += cloud_speed2
        cloud5_x += cloud_speed5
        if cloud2_x > screen_width + 100:
            cloud2_x = -100
        if cloud5_x > screen_width + 100:
            cloud5_x = -100

        if cloud2:
            screen.blit(cloud2, (cloud2_x, asset_positions['cloud2'][1]))
        if cloud5:
            screen.blit(cloud5, (cloud5_x, asset_positions['cloud5'][1]))

        # Animate and draw trees with swaying motion
        tree1_sway_angle += tree1_sway_speed
        tree2_sway_angle += tree2_sway_speed
        
        if tree1_large:
            tree1_sway = math.sin(tree1_sway_angle) * 3
            rotated_tree1 = pygame.transform.rotate(tree1_large, tree1_sway)
            tree1_rect = rotated_tree1.get_rect()
            tree1_rect.midbottom = (asset_positions['tree1_large_left'][0] + tree1_large.get_width() // 2,
                                   asset_positions['tree1_large_left'][1] + tree1_large.get_height())
            screen.blit(rotated_tree1, tree1_rect.topleft)
        
        if tree2_large:
            tree2_sway = math.sin(tree2_sway_angle) * 2.5
            rotated_tree2 = pygame.transform.rotate(tree2_large, tree2_sway)
            tree2_rect = rotated_tree2.get_rect()
            tree2_rect.midbottom = (asset_positions['tree2_large_right'][0] + tree2_large.get_width() // 2,
                                   asset_positions['tree2_large_right'][1] + tree2_large.get_height())
            screen.blit(rotated_tree2, tree2_rect.topleft)

        # Draw temple
        if temple:
            screen.blit(temple, temple_rect)

        # Draw garden lamps
        if garden_lamp:
            screen.blit(garden_lamp, garden_lamp_left_pos)
            screen.blit(garden_lamp, garden_lamp_right_pos)

        # Light effects for garden lamps (if it's dark)
        lights_on = should_lights_be_on(progress)
        if lights_on and garden_lamp:
            lamp_light_pos_left = (garden_lamp_left_pos[0] + garden_lamp.get_width() // 2, 
                                 garden_lamp_left_pos[1] + 10)
            lamp_light_pos_right = (garden_lamp_right_pos[0] + garden_lamp.get_width() // 2, 
                                  garden_lamp_right_pos[1] + 10)
            draw_light_glow(screen, lamp_light_pos_left, 50, (255, 200, 100), 80)
            draw_light_glow(screen, lamp_light_pos_right, 50, (255, 200, 100), 80)

        # Animate birds
        bird1_x += bird_speed1
        bird2_x += bird_speed2
        bird3_x += bird_speed3
        bird4_x += bird_speed4

        if bird1_x > screen_width + 50:
            bird1_x = -50
        if bird2_x > screen_width + 50:
            bird2_x = -50
        if bird3_x > screen_width + 50:
            bird3_x = -50
        if bird4_x < -50:
            bird4_x = screen_width + 50

        # Draw birds
        if bird1:
            screen.blit(bird1, (bird1_x, asset_positions['bird1'][1]))
        if bird2:
            screen.blit(bird2, (bird2_x, asset_positions['bird2'][1]))
        if bird3:
            screen.blit(bird3, (bird3_x, asset_positions['bird3'][1]))
        if bird4:
            screen.blit(bird4, (bird4_x, asset_positions['bird4'][1]))

        # Apply lighting overlay
        darkness = get_sky_lighting(progress)
        apply_sky_lighting(screen, darkness)

        # Instructions
        instruction_font = pygame.font.SysFont("arial", 24, bold=True)
        instruction_text = instruction_font.render("Temple Scene - Press ENTER for Lake Scene", True, (255, 255, 255))
        screen.blit(instruction_text, (10, 10))

    elif current_scene == "background2":
        # Render Background2 - Lake scene
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
        if grass_image_original:
            for patch in grass_patches:
                if patch["tree_index"] < len(tree_data):
                    tree = tree_data[patch["tree_index"]]
                    sway = math.sin(tree["angle"]) * 2
                    rotated = pygame.transform.rotate(tree["image"], sway)
                    rect = rotated.get_rect(midbottom=(tree["x"] + tree["image"].get_width() // 2,
                                                       tree["y"] + tree["image"].get_height()))
                    grass_img = pygame.transform.scale(grass_image_original, (patch["width"], patch["height"]))
                    grass_rect = grass_img.get_rect(midbottom=(rect.centerx + patch["offset_x"], rect.bottom))
                    screen.blit(grass_img, grass_rect.topleft)

        # Lake
        if lake:
            screen.blit(lake, (lake_x, lake_y))

        # Lanterns
        if lantern:
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

        # Instructions
        instruction_font = pygame.font.SysFont("arial", 24, bold=True)
        instruction_text = instruction_font.render("Press ENTER to Return to Menu", True, (255, 255, 255))
        screen.blit(instruction_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()