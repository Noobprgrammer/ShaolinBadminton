##Checking if connectd
import pygame
import sys
import random
import math

def resizeObject(originObject, scaledFactor):
    scaledObject = pygame.transform.scale_by(originObject, scaledFactor)
    return scaledObject


class Raindrop:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = random.randint(0, screen_width)
        self.y = random.randint(-100, 0)
        self.length = random.randint(5, 15)
        self.speed = random.uniform(10, 20)
        self.color = (200, 230, 255, random.randint(100, 200))
        self.thickness = random.randint(1, 2)
        
    def update(self, wind_force):
        self.y += self.speed
        self.x += wind_force * 0.5  # Rain is less affected by wind than leaves
        
        if self.y > self.screen_height:
            self.reset()
            
    def reset(self):
        self.x = random.randint(0, self.screen_width)
        self.y = random.randint(-100, -10)
        self.length = random.randint(5, 15)
        self.speed = random.uniform(10, 20)
        
    def draw(self, screen):
        end_y = self.y + self.length
        rain_surface = pygame.Surface((self.thickness, self.length), pygame.SRCALPHA)
        rain_surface.fill(self.color)
        screen.blit(rain_surface, (self.x, self.y))

class LightningFlash:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.active = False
        self.duration = 0
        self.max_duration = 5  # Frames
        self.intensity = 0
        
    def trigger(self):
        self.active = True
        self.duration = 0
        self.intensity = random.randint(20, 50)
        
    def update(self):
        if self.active:
            self.duration += 1
            if self.duration >= self.max_duration:
                self.active = False
                
    def draw(self, screen):
        if self.active:
            lightning_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            lightning_surface.fill((255, 255, 255, self.intensity))
            screen.blit(lightning_surface, (0, 0))

class Leaf:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Randomly position leaves across the top of the screen
        self.x = random.randint(0, screen_width)
        self.y = random.randint(-100, 0)
        
        # Random size between 5-15 pixels
        self.size = random.randint(10, 25)
        
        # Different colors for leaves (green shades)
        self.colors = [
            (0, 100, 0),      # dark green
            (34, 139, 34),    # forest green
            (0, 128, 0),      # green
            (50, 205, 50),    # lime green
            (144, 238, 144),  # light green
            (60, 179, 113),   # medium sea green
            (46, 139, 87),    # sea green
            (32, 178, 170),   # light sea green
            (0, 250, 154),    # medium spring green
            (85, 107, 47)     # dark olive green
        ]
        self.color = random.choice(self.colors)
        
        # Speed and movement variables
        self.speed_y = random.uniform(1, 3)
        self.speed_x = random.uniform(-1, 1)
        self.angle = 0
        self.rotation_speed = random.uniform(-3, 3)
        
        # Create a more leaf-like shape
        variation = random.uniform(0.8, 1.2)  # Random variation factor
        self.orig_points = [
            (0, -self.size//2 * variation),                    # Top point
            (self.size//4 * variation, -self.size//4 * variation),         # Upper right curve
            (self.size//2 * variation, 0),                     # Right point
            (self.size//4 * variation, self.size//4 * variation),          # Lower right curve
            (0, self.size*3//4 * variation),                   # Bottom point (extended for stem)
            (-self.size//4 * variation, self.size//4 * variation),         # Lower left curve
            (-self.size//2 * variation, 0),                    # Left point
            (-self.size//4 * variation, -self.size//4 * variation)         # Upper left curve
        ]
        self.points = self.orig_points.copy()
        
        # Wind effect parameters
        self.wind_strength = 0
        self.wave_offset = random.uniform(0, 2 * math.pi)
        
    def update(self, wind_force):
        # Apply gravity and wind
        self.y += self.speed_y
        self.x += self.speed_x + wind_force * math.sin(self.wave_offset + pygame.time.get_ticks() * 0.001)
        
        # Rotate the leaf
        self.angle += self.rotation_speed
        self.points = []
        for x, y in self.orig_points:
            new_x = x * math.cos(math.radians(self.angle)) - y * math.sin(math.radians(self.angle))
            new_y = x * math.sin(math.radians(self.angle)) + y * math.cos(math.radians(self.angle))
            self.points.append((new_x + self.x, new_y + self.y))
        
        # Reset if leaf goes off screen
        if self.y > self.screen_height or self.x < -50 or self.x > self.screen_width + 50:
            self.reset()
    
    def reset(self):
        self.x = random.randint(0, self.screen_width)
        self.y = random.randint(-100, -10)
        self.speed_y = random.uniform(1, 3)
        self.speed_x = random.uniform(-1, 1)
        self.rotation_speed = random.uniform(-3, 3)
        self.color = random.choice(self.colors)
        self.wave_offset = random.uniform(0, 2 * math.pi)
    
    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.points)

class WindParticle:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)
        self.length = random.randint(5, 20)
        self.speed = random.uniform(3, 7)
        self.color = (255, 255, 255, random.randint(20, 80))  # White with transparency
        self.lifetime = random.uniform(0.5, 2.0)
        self.birth_time = pygame.time.get_ticks() / 1000  # Convert to seconds
    
    def update(self):
        self.x += self.speed
        
        # Check if particle is off screen or if lifetime is over
        current_time = pygame.time.get_ticks() / 1000
        if self.x > self.screen_width or current_time - self.birth_time > self.lifetime:
            self.reset()
    
    def reset(self):
        self.x = random.randint(-50, 0)
        self.y = random.randint(0, self.screen_height)
        self.length = random.randint(5, 20)
        self.speed = random.uniform(3, 7)
        self.color = (255, 255, 255, random.randint(20, 80))
        self.lifetime = random.uniform(0.5, 2.0)
        self.birth_time = pygame.time.get_ticks() / 1000
    
    def draw(self, screen):
        # Draw a line to represent wind particle
        end_x = self.x + self.length
        # Make a surface for the semi-transparent line
        line_surface = pygame.Surface((self.length, 1), pygame.SRCALPHA)
        pygame.draw.line(line_surface, self.color, (0, 0), (self.length, 0), 1)
        screen.blit(line_surface, (self.x, self.y))

class DayNightCycle:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.time = 0  # 0 = noon, 0.5 = midnight, 1 = noon again
        self.cycle_duration = 60000  # 60 seconds for a full day/night cycle
        self.start_time = pygame.time.get_ticks()
        
    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed = (current_time - self.start_time) % self.cycle_duration
        self.time = elapsed / self.cycle_duration
        
    def get_overlay_color(self):
        # Calculate overlay color based on time of day
        # Near noon (0 or 1): No overlay
        # Near dawn/dusk (0.25, 0.75): Orange/pink overlay
        # Near midnight (0.5): Dark blue overlay
        
        # Normalize time to range 0-0.5 (noon to midnight to noon)
        normalized_time = self.time if self.time <= 0.5 else 1 - self.time
        
        # Calculate color and alpha based on time
        if normalized_time < 0.1:  # Near noon
            return (0, 0, 0, 0)  # Transparent (no overlay)
        elif normalized_time < 0.25:  # Approaching dusk
            # Transition from transparent to orange
            progress = (normalized_time - 0.1) / 0.15
            r = int(255 * progress)
            g = int(100 * progress)
            b = 0
            a = int(100 * progress)
            return (r, g, b, a)
        else:  # Night
            # Transition from orange to dark blue
            progress = (normalized_time - 0.25) / 0.25
            r = int(255 * (1 - progress))
            g = int(100 * (1 - progress))
            b = int(150 * progress)
            a = int(100 + 100 * progress)
            return (r, g, b, a)
    
    def draw(self, screen):
        color = self.get_overlay_color()
        if color[3] > 0:  # If there's any opacity
            overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            overlay.fill(color)
            screen.blit(overlay, (0, 0))

# Main game code
pygame.init()
# Set up the display
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
background_color = (0, 128, 255)  # RGB => blue
pygame.display.set_caption("My First Pygame Program with Weather Effects")

# Load images
background = pygame.image.load("C:\\Users\\xxiao\\APU\\Y2 SEM2\\ISE\\ISE Code\\Project\\BadmintonCourt1.jpeg")
character = pygame.image.load("C:\\Users\\xxiao\\APU\\Y2 SEM2\\ISE\\ISE Code\\Project\\Character1.png")
UpdatedBackground = pygame.transform.scale(background, (screen_width, screen_height))
Updatedcharacter = resizeObject(character, 0.2)

charRectBlock = Updatedcharacter.get_rect()
charRectBlock.center = (400, 500)

# Weather system
weather_state = "sunny"  # Can be "sunny", "windy", "rainy", "stormy"
weather_change_timer = pygame.time.get_ticks()
weather_duration = random.randint(10000, 30000)  # 10-30 seconds per weather state

# Create leaves, wind particles, and raindrops
num_leaves = 30
leaves = [Leaf(screen_width, screen_height) for _ in range(num_leaves)]

num_wind_particles = 20
wind_particles = [WindParticle(screen_width, screen_height) for _ in range(num_wind_particles)]

num_raindrops = 200
raindrops = [Raindrop(screen_width, screen_height) for _ in range(num_raindrops)]

# Create lightning flash effect
lightning = LightningFlash(screen_width, screen_height)
next_lightning = pygame.time.get_ticks() + random.randint(5000, 10000)

# Create day/night cycle
day_night_cycle = DayNightCycle(screen_width, screen_height)

# Wind variables
wind_force = 0.5
wind_changing = False
wind_target = 0.5
wind_change_speed = 0.01
last_wind_change = pygame.time.get_ticks()

# Sound effects (commented out, uncomment if you have the sound files)
# pygame.mixer.init()
# wind_sound = pygame.mixer.Sound("wind.wav")
# rain_sound = pygame.mixer.Sound("rain.wav")
# thunder_sound = pygame.mixer.Sound("thunder.wav")

clock = pygame.time.Clock()
# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        charRectBlock.x -= 5
    if keys[pygame.K_RIGHT]:
        charRectBlock.x += 5
    if keys[pygame.K_UP]:
        charRectBlock.y -= 5
    if keys[pygame.K_DOWN]:
        charRectBlock.y += 5
    
    # Toggle weather manually with number keys
    if keys[pygame.K_1]:
        weather_state = "sunny"
    if keys[pygame.K_2]:
        weather_state = "windy"
    if keys[pygame.K_3]:
        weather_state = "rainy"
    if keys[pygame.K_4]:
        weather_state = "stormy"

    # Update day/night cycle
    day_night_cycle.update()
    
    # Check for weather changes
    current_time = pygame.time.get_ticks()
    if current_time - weather_change_timer > weather_duration:
        # Randomly change weather
        weather_state = random.choice(["sunny", "windy", "rainy", "stormy"])
        weather_change_timer = current_time
        weather_duration = random.randint(10000, 30000)  # 10-30 seconds

    # Update wind based on weather
    if weather_state == "sunny":
        wind_target = random.uniform(-0.3, 0.3)
    elif weather_state == "windy":
        wind_target = random.uniform(-2.0, 2.0)
    elif weather_state == "rainy":
        wind_target = random.uniform(-0.8, 0.8)
    elif weather_state == "stormy":
        wind_target = random.uniform(-3.0, 3.0)
    
    # Gradually change wind to target
    if abs(wind_force - wind_target) < wind_change_speed:
        wind_force = wind_target
    else:
        if wind_force < wind_target:
            wind_force += wind_change_speed
        else:
            wind_force -= wind_change_speed
    
    # Update lightning for stormy weather
    if weather_state == "stormy":
        lightning.update()
        if current_time > next_lightning and not lightning.active:
            lightning.trigger()
            next_lightning = current_time + random.randint(2000, 8000)
            # Uncomment if you have the sound file
            # thunder_sound.play()

    # Update visual elements based on current weather
    visible_leaves = num_leaves  # Default number
    visible_wind = 0
    visible_rain = 0
    
    if weather_state == "sunny":
        visible_leaves = max(5, int(num_leaves * 0.3))
        visible_wind = int(num_wind_particles * 0.2)
        visible_rain = 0
    elif weather_state == "windy":
        visible_leaves = num_leaves
        visible_wind = num_wind_particles
        visible_rain = 0
    elif weather_state == "rainy":
        visible_leaves = max(5, int(num_leaves * 0.5))
        visible_wind = int(num_wind_particles * 0.5)
        visible_rain = int(num_raindrops * 0.7)
    elif weather_state == "stormy":
        visible_leaves = num_leaves
        visible_wind = num_wind_particles
        visible_rain = num_raindrops

    # Update particles based on visibility
    for i, leaf in enumerate(leaves):
        if i < visible_leaves:
            leaf.update(wind_force)
    
    for i, particle in enumerate(wind_particles):
        if i < visible_wind:
            particle.update()
    
    for i, raindrop in enumerate(raindrops):
        if i < visible_rain:
            raindrop.update(wind_force)

    # Draw everything
    screen.fill(background_color)
    screen.blit(UpdatedBackground, (0, 0))
    
    # Apply day/night cycle effect
    day_night_cycle.draw(screen)
    
    # Draw weather effects based on current state
    if weather_state in ["windy", "stormy"]:
        # Draw semi-transparent overlay to darken background when wind is strong
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(abs(wind_force) * 15)))
        screen.blit(overlay, (0, 0))
    
    # Draw wind particles if applicable
    for i, particle in enumerate(wind_particles):
        if i < visible_wind:
            particle.draw(screen)
    
    # Draw leaves if applicable
    for i, leaf in enumerate(leaves):
        if i < visible_leaves:
            leaf.draw(screen)
    
    # Draw rain if applicable
    for i, raindrop in enumerate(raindrops):
        if i < visible_rain:
            raindrop.draw(screen)
    
    # Draw lightning flash if active
    if weather_state == "stormy":
        lightning.draw(screen)
    
    # Draw character on top
    screen.blit(Updatedcharacter, charRectBlock)
    
    # Draw weather info
    font = pygame.font.Font(None, 36)
    weather_text = font.render(f"Weather: {weather_state.capitalize()}", True, (255, 255, 255))
    screen.blit(weather_text, (10, 10))
    
    # Update the screen
    pygame.display.flip()
    clock.tick(60)  # Limit to 60 FPS

print("closing...")
pygame.quit()
sys.exit()