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
pygame.display.set_caption("My Game Window")

# Asset paths - Update these paths to match your actual file locations
BACKGROUND_PATH = r"C:\\Users\\xxiao\\OneDrive - Asia Pacific University\\ShaolinBadminton\\Assests\\Background\\Background1\\Background1.jpg"
TREE1_PATH = r"C:\\Users\\xxiao\\OneDrive - Asia Pacific University\\ShaolinBadminton\\Assests\\Effects\\Assets\\Tree1.png"   
TREE2_PATH = r"C:\\Users\\xxiao\\OneDrive - Asia Pacific University\\ShaolinBadminton\\Assests\\Effects\\Assets\\Tree2.png"   
BIRD_PATH = r"C:\\Users\\xxiao\\OneDrive - Asia Pacific University\\ShaolinBadminton\\Assests\\Effects\\Assets\\Bird2.png" 
CLOUD1_PATH = r"C:\\Users\\xxiao\\OneDrive - Asia Pacific University\\ShaolinBadminton\\Assests\\Effects\\Assets\\Cloud1.png"
CLOUD2_PATH = r"C:\\Users\\xxiao\\OneDrive - Asia Pacific University\\ShaolinBadminton\\Assests\\Effects\\Assets\\Cloud2.png"
CLOUD3_PATH = r"C:\\Users\\xxiao\\OneDrive - Asia Pacific University\\ShaolinBadminton\\Assests\\Effects\\Assets\\Cloud3.png"
CLOUD4_PATH = r"C:\\Users\\xxiao\\OneDrive - Asia Pacific University\\ShaolinBadminton\\Assests\\Effects\\Assets\\Cloud4.png"
SUN_PATH = r"C:\\Users\\xxiao\\OneDrive - Asia Pacific University\\ShaolinBadminton\\Assests\\Effects\\Assets\\Sun.png"
TEMPLE_PATH = r"C:\\Users\\xxiao\\OneDrive - Asia Pacific University\\ShaolinBadminton\\Assests\\Effects\\Assets\\Temple.png"
LATERN1_PATH = r"C:\\Users\\xxiao\\OneDrive - Asia Pacific University\\ShaolinBadminton\\Assests\\Effects\\Assets\\GardenLamp.png"

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

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = pygame.time.get_ticks()

    # Draw background
    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill((135, 206, 235))

    # Calculate sun position and lighting
    sun_x, sun_y, sun_progress = get_sun_position(current_time)
    lights_on = should_lights_be_on(sun_progress)
    
    # Draw sun
    if sun:
        rotation_angle = (current_time * 0.05) % 360
        rotated_sun = pygame.transform.rotate(sun, -rotation_angle)
        sun_rect = rotated_sun.get_rect(center=(sun_x, sun_y))
        
        if sun_y < screen_height - 100:
            screen.blit(rotated_sun, sun_rect.topleft)

    # Draw clouds
    if cloud2:
        cloud2_x += cloud_speed2
        if cloud2_x > screen_width + 200:
            cloud2_x = -200
        screen.blit(cloud2, (cloud2_x, asset_positions['cloud2'][1]))

    if cloud5:
        cloud5_x += cloud_speed5
        if cloud5_x > screen_width + 200:
            cloud5_x = -200
        screen.blit(cloud5, (cloud5_x, asset_positions['cloud5'][1]))

    # Draw temple
    if temple:
        screen.blit(temple, temple_rect.topleft)

    # Draw garden lamps with lighting effects
    if garden_lamp and temple:
        # Draw light glow first (behind the lamps)
        # Calculate alpha based on time of day (0 to 100)
        if sun_progress <= 0.2:
            glow_alpha = int(100 * (1 - sun_progress / 0.2))  # Full at night, fades at sunrise
        elif sun_progress >= 0.8:
            glow_alpha = int(100 * ((sun_progress - 0.8) / 0.2))  # Fades in at sunset
        else:
            glow_alpha = 0  # Daytime

        # Offsets to adjust glow position
        glow_offset_x = 90   # Rightward adjustment
        glow_offset_y = 30   # Downward adjustment
        strong_glow_radius = 80       # Bigger glow
        strong_glow_alpha = 255      # Stronger brightness (0–255)

        if glow_alpha > 0:
            draw_light_glow(screen, 
                (garden_lamp_left_pos[0] + glow_offset_x, garden_lamp_left_pos[1] + glow_offset_y),
                40, (255, 255, 200), glow_alpha)
            
            draw_light_glow(screen, 
                (garden_lamp_right_pos[0] + glow_offset_x, garden_lamp_right_pos[1] + glow_offset_y),
                40, (255, 255, 200), glow_alpha)


        
        # Draw the garden lamps
        screen.blit(garden_lamp, garden_lamp_left_pos)
        screen.blit(garden_lamp, garden_lamp_right_pos)

    # Draw trees
    if tree1_large:
        screen.blit(tree1_large, asset_positions['tree1_large_left'])
    if tree2_large:
        screen.blit(tree2_large, asset_positions['tree2_large_right'])

    # Draw birds with movement
    if bird1:
        bird1_x += bird_speed1
        if bird1_x > screen_width + 100:
            bird1_x = -100
        screen.blit(bird1, (bird1_x, asset_positions['bird1'][1]))

    if bird2:
        bird2_x += bird_speed2
        if bird2_x > screen_width + 100:
            bird2_x = -100
        screen.blit(bird2, (bird2_x, asset_positions['bird2'][1]))

    if bird3:
        bird3_x += bird_speed3
        if bird3_x > screen_width + 100:
            bird3_x = -100
        screen.blit(bird3, (bird3_x, asset_positions['bird3'][1]))

    if bird4:
        bird4_x += bird_speed4
        if bird4_x < -100:
            bird4_x = screen_width + 100
        screen.blit(bird4, (bird4_x, asset_positions['bird4'][1]))

    # Apply day/night lighting overlay
    darkness_level = get_sky_lighting(sun_progress)
    apply_sky_lighting(screen, darkness_level)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()