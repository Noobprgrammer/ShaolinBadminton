import pygame
import sys
import random
import math
import time
import os

pygame.mixer.init()

scriptDir = os.path.dirname(os.path.abspath(__file__))
assetWalk = os.path.join(scriptDir,"..","Assests","Character","Character 1 Walk")
assetJump = os.path.join(scriptDir,"..","Assests","Character","Character 1 Jump")
assetHit = os.path.join(scriptDir,"..","Assests","Character","Character 1 Hit")
assetIdle = os.path.join(scriptDir,"..","Assests","Character","Character 1 Idle")
assetEffect = os.path.join(scriptDir,"..","Assests","Effects","Sound")
asset = os.path.join(scriptDir,"..","Assests")

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 900
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Badminton")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
LIGHT_GRAY = (200, 200, 200)

# Player properties
PLAYER_SIZE = 130
PLAYER_SIZE_X = 100
PLAYER_SPEED = 5
JUMP_STRENGTH = -15
PLAYER_GRAVITY = 1

# Animation properties
WALK_FRAME_RATE = 8  # Frames to wait between animation updates
JUMP_FRAME_RATE = 6  # Faster for jump animation

# --- Player 1 Animation ---
player1_walk_animation_index = 0
player1_jump_animation_index = 0
player1_hit_animation_index = 0
player1_is_jumping = False
player1_is_hitting = False
player1_animation_state = "idle"  # "idle", "walk_left", "walk_right", "jump", "hit"
player1_frame_counter = 0

# Create simple colored rectangles as fallback for missing assets
def create_fallback_frames():
    """Create simple colored rectangles as fallback sprites"""
    frames = []
    colors = [(100, 150, 255), (120, 170, 255), (140, 190, 255), (160, 210, 255), (180, 230, 255)]
    for i, color in enumerate(colors):
        surface = pygame.Surface((PLAYER_SIZE_X, PLAYER_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(surface, color, (0, 0, PLAYER_SIZE_X, PLAYER_SIZE))
        pygame.draw.rect(surface, BLACK, (0, 0, PLAYER_SIZE_X, PLAYER_SIZE), 2)
        frames.append(surface)
    return frames

try:
    player1_walk_right_frames = [pygame.transform.scale(pygame.image.load(os.path.join(assetWalk, "CharacterWalk1.png")).convert_alpha(), (PLAYER_SIZE_X, PLAYER_SIZE)),
                                pygame.transform.scale(pygame.image.load(os.path.join(assetWalk, "CharacterWalk2.png")).convert_alpha(), (PLAYER_SIZE_X, PLAYER_SIZE)),
                                pygame.transform.scale(pygame.image.load(os.path.join(assetWalk, "CharacterWalk3.png")).convert_alpha(), (PLAYER_SIZE_X, PLAYER_SIZE)),
                                pygame.transform.scale(pygame.image.load(os.path.join(assetWalk, "CharacterWalk4.png")).convert_alpha(), (PLAYER_SIZE_X, PLAYER_SIZE)),
                                pygame.transform.scale(pygame.image.load(os.path.join(assetWalk, "CharacterWalk5.png")).convert_alpha(), (PLAYER_SIZE_X, PLAYER_SIZE)),
                                ]
    player1_walk_left_frames = [pygame.transform.scale(pygame.image.load(os.path.join(assetWalk, "CharacterWalk5.png")).convert_alpha(), (PLAYER_SIZE_X, PLAYER_SIZE)),
                                 pygame.transform.scale(pygame.image.load(os.path.join(assetWalk, "CharacterWalk4.png")).convert_alpha(), (PLAYER_SIZE_X, PLAYER_SIZE)),
                                 pygame.transform.scale(pygame.image.load(os.path.join(assetWalk, "CharacterWalk3.png")).convert_alpha(), (PLAYER_SIZE_X,PLAYER_SIZE)),
                                 pygame.transform.scale(pygame.image.load(os.path.join(assetWalk, "CharacterWalk2.png")).convert_alpha(), (PLAYER_SIZE_X,PLAYER_SIZE)),
                                 pygame.transform.scale(pygame.image.load(os.path.join(assetWalk, "CharacterWalk1.png")).convert_alpha(), (PLAYER_SIZE_X,PLAYER_SIZE)),
                                 ]
    player1_jump_frames = [pygame.transform.scale(pygame.image.load(os.path.join(assetJump, f"Character 1 Jump {i+1}.png")).convert_alpha(), (PLAYER_SIZE_X, PLAYER_SIZE)) for i in range(4,9)]
    player1_hit_frames = [pygame.transform.scale(pygame.image.load(os.path.join(assetHit, f"Character 1 Hit {i+1}.png")).convert_alpha(), (PLAYER_SIZE_X, PLAYER_SIZE)) for i in range(2,7)]
    player1_idle_frame = player1_walk_right_frames[0]  # Use first walk frame as idle
except pygame.error as e:
    print(f"Error loading Player 1 image: {e}")
    print("Using fallback sprites...")
    player1_walk_right_frames = create_fallback_frames()
    player1_walk_left_frames = [pygame.transform.flip(frame, True, False) for frame in player1_walk_right_frames]
    player1_jump_frames = create_fallback_frames()
    player1_hit_frames = create_fallback_frames()
    player1_idle_frame = player1_walk_right_frames[0]

try:
    walkSound = pygame.mixer.Sound(os.path.join(assetEffect, "Run.wav"))
    jumpSound = pygame.mixer.Sound(os.path.join(assetEffect, "Boy_Jump.mp3"))
    nomralSound = pygame.mixer.Sound(os.path.join(assetEffect, "NormalPlaying.wav"))
    smashSound = pygame.mixer.Sound(os.path.join(assetEffect, "Smash.mp3"))
except pygame.error as e:
    print(f"Error loading sound files: {e}")

# --- Player 2 Animation ---
player2_walk_animation_index = 0
player2_jump_animation_index = 0
player2_hit_animation_index = 0
player2_is_jumping = False
player2_is_hitting = False
player2_animation_state = "idle"
player2_frame_counter = 0

try:
    player2_walk_right_frames = [pygame.transform.flip(frame, True, False) for frame in player1_walk_right_frames]
    player2_walk_left_frames = [pygame.transform.flip(frame, True, False) for frame in player1_walk_left_frames]
    player2_jump_frames = [pygame.transform.flip(frame, True, False) for frame in player1_jump_frames]
    player2_hit_frames = [pygame.transform.flip(frame, True, False) for frame in player1_hit_frames]
    player2_idle_frame = player2_walk_right_frames[0]
except pygame.error as e:
    print(f"Error loading Player 2 image: {e}")
    # Create different colored sprites for player 2
    fallback_frames = create_fallback_frames()
    player2_walk_right_frames = []
    for frame in fallback_frames:
        new_frame = pygame.Surface((PLAYER_SIZE_X, PLAYER_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(new_frame, (255, 150, 100), (0, 0, PLAYER_SIZE_X, PLAYER_SIZE))
        pygame.draw.rect(new_frame, BLACK, (0, 0, PLAYER_SIZE_X, PLAYER_SIZE), 2)
        player2_walk_right_frames.append(new_frame)
    player2_walk_left_frames = [pygame.transform.flip(frame, True, False) for frame in player2_walk_right_frames]
    player2_jump_frames = player2_walk_right_frames.copy()
    player2_hit_frames = player2_walk_right_frames.copy()
    player2_idle_frame = player2_walk_right_frames[0]

def play_sound_effect(action):
    if action == "walk":
        walkSound.play()
    elif action == "jump":
        jumpSound.play()
    elif action == "normalHit":
        nomralSound.play()
    elif action == "smash":
        smashSound.play()


# Create shuttle sprite fallback
def create_shuttle_sprite():
    """Create a simple shuttle sprite"""
    surface = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.circle(surface, WHITE, (15, 15), 12)
    pygame.draw.circle(surface, BLACK, (15, 15), 12, 2)
    # Add feathers
    for i in range(6):
        angle = i * 60
        x = 15 + math.cos(math.radians(angle)) * 8
        y = 15 + math.sin(math.radians(angle)) * 8
        pygame.draw.line(surface, BLACK, (15, 15), (x, y), 2)
    return surface

try:
    shuttle_image = pygame.image.load(os.path.join(asset, "badminton-shuttle_1.png")).convert_alpha()
    SHUTTLE_IMAGE_SIZE = (30, 30)
    shuttle_image = pygame.transform.scale(shuttle_image, SHUTTLE_IMAGE_SIZE)
    SHUTTLE_RADIUS = SHUTTLE_IMAGE_SIZE[0] // 2
except pygame.error as e:
    print(f"Error loading shuttle image: {e}")
    print("Using fallback shuttle sprite...")
    shuttle_image = create_shuttle_sprite()
    SHUTTLE_IMAGE_SIZE = (30, 30)
    SHUTTLE_RADIUS = SHUTTLE_IMAGE_SIZE[0] // 2

# Shuttle properties
shuttle = {'pos': [0, 0], 'vel': [0, 0], 'is_real': True}
SHUTTLE_SPEED_X_BASE = 7
SHUTTLE_SPEED_Y_INIT_BASE = -10
SHUTTLE_GRAVITY = 0.5
SHUTTLE_FRICTION_X = 0.98
SERVE_POWER_MULTIPLIER = 2.0
MAX_SERVE_CHARGE_FRAMES = 120
last_hit_by = 0

# Hit modifiers
SLOW_HIT_MODIFIER_X = 1
SLOW_HIT_MODIFIER_Y = 1
HARD_HIT_MODIFIER_X = 1.5
HARD_HIT_MODIFIER_Y = 1.5
#FAKE_SHUTTLE_COUNT = 2
SPECIAL_HIT_COOLDOWN_FRAMES = 180
WINNING_SCORE = 20
HIT_ANIMATION_DURATION = 20  # Frames for hit animation

# Game state
player1_pos = [100, HEIGHT - PLAYER_SIZE - 50]
player2_pos = [WIDTH - 100 - PLAYER_SIZE, HEIGHT - PLAYER_SIZE - 50]
player1_vel_y = 0
player2_vel_y = 0
player1_on_ground = True
player2_on_ground = True

shuttle = {'pos': [0, 0], 'vel': [0, 0], 'color': GREEN, 'is_real': True}
shuttle_in_play = False
server = 1
serving = True
charge_start_time = 0
charge_power = 0
game_over = False
winner = None

special_hit_cooldown_p1 = 0
special_hit_cooldown_p2 = 0
player1_hit_timer = 0
player2_hit_timer = 0

score1 = 0
score2 = 0
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)
small_font = pygame.font.Font(None, 24)

SHADOW_COLOR = (100, 100, 100)
SHADOW_OFFSET_X = 2

def update_player_animation(player):
    """Update animation state and frame counters for a player"""
    global player1_frame_counter, player2_frame_counter
    global player1_walk_animation_index, player1_jump_animation_index, player1_hit_animation_index
    global player2_walk_animation_index, player2_jump_animation_index, player2_hit_animation_index
    
    if player == 1:
        player1_frame_counter += 1
        
        if player1_animation_state == "walk_left" or player1_animation_state == "walk_right":
            if player1_frame_counter >= WALK_FRAME_RATE:
                player1_frame_counter = 0
                player1_walk_animation_index = (player1_walk_animation_index + 1) % len(player1_walk_right_frames)
        elif player1_animation_state == "jump":
            if player1_frame_counter >= JUMP_FRAME_RATE:
                player1_frame_counter = 0
                if player1_jump_animation_index < len(player1_jump_frames) - 1:
                    player1_jump_animation_index += 1
        elif player1_animation_state == "hit":
            if player1_frame_counter >= JUMP_FRAME_RATE:  # Use same rate as jump
                player1_frame_counter = 0
                if player1_hit_animation_index < len(player1_hit_frames) - 1:
                    player1_hit_animation_index += 1
                    
    elif player == 2:
        player2_frame_counter += 1
        
        if player2_animation_state == "walk_left" or player2_animation_state == "walk_right":
            if player2_frame_counter >= WALK_FRAME_RATE:
                player2_frame_counter = 0
                player2_walk_animation_index = (player2_walk_animation_index + 1) % len(player2_walk_right_frames)
        elif player2_animation_state == "jump":
            if player2_frame_counter >= JUMP_FRAME_RATE:
                player2_frame_counter = 0
                if player2_jump_animation_index < len(player2_jump_frames) - 1:
                    player2_jump_animation_index += 1
        elif player2_animation_state == "hit":
            if player2_frame_counter >= JUMP_FRAME_RATE:
                player2_frame_counter = 0
                if player2_hit_animation_index < len(player2_hit_frames) - 1:
                    player2_hit_animation_index += 1
        

def draw_player(surface, player):
    """Draw player with current animation frame"""
    if player == 1:
        x, y = int(player1_pos[0]), int(player1_pos[1])
        
        if player1_animation_state == "walk_right":
            frame = player1_walk_right_frames[player1_walk_animation_index]
        elif player1_animation_state == "walk_left":
            frame = player1_walk_left_frames[player1_walk_animation_index]
        elif player1_animation_state == "jump":
            frame = player1_jump_frames[player1_jump_animation_index]
        elif player1_animation_state == "hit":
            frame = player1_hit_frames[player1_hit_animation_index]
        else:  # idle
            frame = player1_idle_frame
            
        surface.blit(frame, (x, y))
        
    elif player == 2:
        x, y = int(player2_pos[0]), int(player2_pos[1])
        
        if player2_animation_state == "walk_right":
            frame = player2_walk_right_frames[player2_walk_animation_index]
        elif player2_animation_state == "walk_left":
            frame = player2_walk_left_frames[player2_walk_animation_index]
        elif player2_animation_state == "jump":
            frame = player2_jump_frames[player2_jump_animation_index]
        elif player2_animation_state == "hit":
            frame = player2_hit_frames[player2_hit_animation_index]
        else:  # idle
            frame = player2_idle_frame
            
        surface.blit(frame, (x, y))

def set_player_animation_state(player, state):
    """Set animation state and reset relevant counters"""
    global player1_animation_state, player2_animation_state
    global player1_walk_animation_index, player1_jump_animation_index, player1_hit_animation_index
    global player2_walk_animation_index, player2_jump_animation_index, player2_hit_animation_index
    global player1_frame_counter, player2_frame_counter
    
    if player == 1:
        if player1_animation_state != state:
            player1_animation_state = state
            player1_frame_counter = 0
            if state == "jump":
                player1_jump_animation_index = 0
            elif state == "hit":
                player1_hit_animation_index = 0
            elif state in ["walk_left", "walk_right"]:
                player1_walk_animation_index = 0
                
    elif player == 2:
        if player2_animation_state != state:
            player2_animation_state = state
            player2_frame_counter = 0
            if state == "jump":
                player2_jump_animation_index = 0
            elif state == "hit":
                player2_hit_animation_index = 0
            elif state in ["walk_left", "walk_right"]:
                player2_walk_animation_index = 0

def draw_shuttle(sh):
    image_to_draw = shuttle_image
    angle = math.degrees(math.atan2(sh['vel'][1], sh['vel'][0]))
    rotated_image = pygame.transform.rotate(image_to_draw, -angle)
    rotated_rect = rotated_image.get_rect(center=(int(sh['pos'][0]), int(sh['pos'][1])))
    pos = rotated_rect.topleft
    screen.blit(rotated_image, pos)

    if sh.get('is_real', False):
        shadow_x = int(sh['pos'][0]) + SHADOW_OFFSET_X
        shadow_y = HEIGHT - 50
        shadow_radius = max(2, int(SHUTTLE_RADIUS * (0.5 + 0.5 * (1 - sh['pos'][1] / HEIGHT))))
        pygame.draw.circle(screen, SHADOW_COLOR, (shadow_x, shadow_y), shadow_radius)

def display_score():
    score_text = font.render(f"Player 1: {score1}   Player 2: {score2}", True, BLACK)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

def display_cooldowns():
    if special_hit_cooldown_p1 > 0:
        cooldown_text_p1 = small_font.render(f"P1 Special CD: {special_hit_cooldown_p1 // 60 + 1}", True, BLACK)
        screen.blit(cooldown_text_p1, (10, 10))
    if special_hit_cooldown_p2 > 0:
        cooldown_text_p2 = small_font.render(f"P2 Special CD: {special_hit_cooldown_p2 // 60 + 1}", True, BLACK)
        screen.blit(cooldown_text_p2, (WIDTH - cooldown_text_p2.get_width() - 10, 10))

def draw_serve_power(player):
    if serving and ((server == 1 and player == 1) or (server == 2 and player == 2)):
        bar_width = 100
        bar_height = 10
        top_offset = 30

        if player == 1:
            bar_x = 50
            bar_y = top_offset
        else:
            bar_x = WIDTH - 50 - bar_width
            bar_y = top_offset

        pygame.draw.rect(screen, LIGHT_GRAY, (bar_x, bar_y, bar_width, bar_height))
        power_fill_width = bar_width * (charge_power / MAX_SERVE_CHARGE_FRAMES)
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, power_fill_width, bar_height))

def reset_game():
    global player1_pos, player2_pos, player1_vel_y, player2_vel_y
    global player1_on_ground, player2_on_ground, shuttle
    global shuttle_in_play, server, serving, charge_power, game_over, winner
    global special_hit_cooldown_p1, special_hit_cooldown_p2, score1, score2
    global player1_animation_state, player2_animation_state
    global player1_is_jumping, player2_is_jumping, player1_hit_timer, player2_hit_timer

    player1_pos = [100, HEIGHT - PLAYER_SIZE - 50]
    player2_pos = [WIDTH - 100 - PLAYER_SIZE, HEIGHT - PLAYER_SIZE - 50]
    player1_vel_y = 0
    player2_vel_y = 0
    player1_on_ground = True
    player2_on_ground = True
    shuttle = {'pos': [0, 0], 'vel': [0, 0], 'color': GREEN, 'is_real': True}
    shuttle_in_play = False
    server = 1
    serving = True
    charge_power = 0
    game_over = False
    winner = None
    special_hit_cooldown_p1 = 0
    special_hit_cooldown_p2 = 0
    score1 = 0
    score2 = 0
    player1_animation_state = "idle"
    player2_animation_state = "idle"
    player1_is_jumping = False
    player2_is_jumping = False
    player1_hit_timer = 0
    player2_hit_timer = 0

def reset_shuttle(serving_player):
    global shuttle, shuttle_in_play, serving, charge_power
    shuttle_in_play = False
    serving = True
    shuttle = {'pos': [0, 0], 'vel': [0, 0], 'color': GREEN, 'is_real': True}
    charge_power = 0

def start_serve(power):
    global shuttle, shuttle_in_play, serving
    shuttle_in_play = True
    serving = False
    power_ratio = min(1.0, power / MAX_SERVE_CHARGE_FRAMES)
    serve_force_x = SHUTTLE_SPEED_X_BASE * 0.8 * (1 + power_ratio * SERVE_POWER_MULTIPLIER)
    serve_force_y = SHUTTLE_SPEED_Y_INIT_BASE * 0.8 * (1 + power_ratio * SERVE_POWER_MULTIPLIER)
    shuttle['vel'] = [serve_force_x * (1 if server == 1 else -1), serve_force_y]

def check_collision(player_rect, shuttle_circle):
    px, py = player_rect.center
    sx, sy = shuttle_circle
    distance_squared = (px - sx)**2 + (py - sy)**2
    radii_sum_squared = (PLAYER_SIZE // 2 + SHUTTLE_RADIUS)**2
    return distance_squared <= radii_sum_squared

def display_game_over():
    game_over_text = large_font.render("Game Over", True, BLACK)
    winner_text = font.render(f"Player {winner} Wins!", True, BLACK)
    play_again_button = font.render("Play Again (SPACE)", True, BLACK)
    quit_button = font.render("Quit (ESC)", True, BLACK)

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))
    screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 4 + 80))
    screen.blit(play_again_button, (WIDTH // 2 - play_again_button.get_width() // 2, HEIGHT // 2 + 50))
    screen.blit(quit_button, (WIDTH // 2 - quit_button.get_width() // 2, HEIGHT // 2 + 100))

def handle_game_over_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                reset_game()
                return True
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    return False

def game_start_screen():
    start_screen_active = True
    while start_screen_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start_screen_active = False

        screen.fill(WHITE)
        title_text = large_font.render("2D Badminton", True, BLACK)
        instructions_text = font.render("Press ENTER to Start", True, BLACK)
        controls_text1 = small_font.render("Player 1: A/D to move, W to jump, S to serve, Q/E/R to hit", True, BLACK)
        controls_text2 = small_font.render("Player 2: Left/Right to move, Up to jump, Down to serve, </>/? to hit", True, BLACK)
        
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
        screen.blit(instructions_text, (WIDTH // 2 - instructions_text.get_width() // 2, HEIGHT // 3 + 100))
        screen.blit(controls_text1, (WIDTH // 2 - controls_text1.get_width() // 2, HEIGHT // 2 + 50))
        screen.blit(controls_text2, (WIDTH // 2 - controls_text2.get_width() // 2, HEIGHT // 2 + 80))
        pygame.display.flip()

def trigger_hit_animation(player):
    """Trigger hit animation for a player"""
    global player1_hit_timer, player2_hit_timer
    if player == 1:
        set_player_animation_state(1, "hit")
        player1_hit_timer = HIT_ANIMATION_DURATION
    elif player == 2:
        set_player_animation_state(2, "hit")
        player2_hit_timer = HIT_ANIMATION_DURATION

def draw_court():
    """Draw the badminton court"""
    # Court floor
    pygame.draw.rect(screen, LIGHT_GRAY, (0, HEIGHT - 50, WIDTH, 50))
    
    # Net
    net_x = WIDTH // 2
    pygame.draw.rect(screen, BLACK, (net_x - 5, HEIGHT // 2, 10, HEIGHT // 2 - 50))
    
    # Court lines
    pygame.draw.line(screen, BLACK, (0, HEIGHT - 50), (WIDTH, HEIGHT - 50), 3)
    pygame.draw.line(screen, BLACK, (net_x, HEIGHT - 50), (net_x, HEIGHT - 30), 3)

game_start_screen()

running = True
charging_serve = False
clock = pygame.time.Clock()

while running:
    if not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and player1_on_ground:
                    player1_vel_y = JUMP_STRENGTH
                    player1_on_ground = False
                    player1_is_jumping = True
                    play_sound_effect("jump")
                    set_player_animation_state(1, "jump")
                if event.key == pygame.K_UP and player2_on_ground:
                    player2_vel_y = JUMP_STRENGTH
                    player2_on_ground = False
                    player2_is_jumping = True
                    play_sound_effect("jump")
                    set_player_animation_state(2, "jump")
                if serving:
                    if server == 1 and event.key == pygame.K_s:
                        charging_serve = True
                        charge_start_time = pygame.time.get_ticks()
                    elif server == 2 and event.key == pygame.K_DOWN:
                        charging_serve = True
                        charge_start_time = pygame.time.get_ticks()
            elif event.type == pygame.KEYUP:
                if serving and charging_serve:
                    if server == 1 and event.key == pygame.K_s:
                        start_serve(charge_power)
                        play_sound_effect("smash")
                        trigger_hit_animation(1)
                        charging_serve = False
                        charge_power = 0
                    elif server == 2 and event.key == pygame.K_DOWN:
                        start_serve(charge_power)
                        play_sound_effect("smash")
                        trigger_hit_animation(2)
                        charging_serve = False
                        charge_power = 0

        keys = pygame.key.get_pressed()

        # Update hit timers
        if player1_hit_timer > 0:
            player1_hit_timer -= 1
            if player1_hit_timer <= 0:
                set_player_animation_state(1, "idle")
        
        if player2_hit_timer > 0:
            player2_hit_timer -= 1
            if player2_hit_timer <= 0:
                set_player_animation_state(2, "idle")

        # Player 1 movement and animation (only if not hitting)
        if player1_hit_timer <= 0:
            if player1_is_jumping:
                # Keep jump animation state
                pass
            elif keys[pygame.K_a]:
                player1_pos[0] -= PLAYER_SPEED
                play_sound_effect("walk")
                set_player_animation_state(1, "walk_left")
            elif keys[pygame.K_d]:
                player1_pos[0] += PLAYER_SPEED
                play_sound_effect("walk")
                set_player_animation_state(1, "walk_right")
            elif keys[pygame.K_q]:
                play_sound_effect("normalHit")
                trigger_hit_animation(1)
            elif keys[pygame.K_e]:
                play_sound_effect("smash")
                trigger_hit_animation(1)
            else:
                if not player1_is_jumping:
                    set_player_animation_state(1, "idle")

        # Player 2 movement and animation (only if not hitting)
        if player2_hit_timer <= 0:
            if player2_is_jumping:
                # Keep jump animation state
                pass
            elif keys[pygame.K_LEFT]:
                player2_pos[0] -= PLAYER_SPEED
                play_sound_effect("walk")
                set_player_animation_state(2, "walk_left")
            elif keys[pygame.K_RIGHT]:
                player2_pos[0] += PLAYER_SPEED
                play_sound_effect("walk")
                set_player_animation_state(2, "walk_right")
            elif keys[pygame.K_COMMA]:
                play_sound_effect("normalHit")
                trigger_hit_animation(2)
            elif keys[pygame.K_PERIOD]:
                play_sound_effect("smash")
                trigger_hit_animation(2)
            else:
                if not player2_is_jumping:
                    set_player_animation_state(2, "idle")

        # Boundary constraints
        player1_pos[0] = max(0, min(player1_pos[0], WIDTH // 2 - PLAYER_SIZE_X))
        player2_pos[0] = max(WIDTH // 2 + 1, min(player2_pos[0], WIDTH - PLAYER_SIZE_X))

        # Apply gravity to players
        player1_vel_y += PLAYER_GRAVITY
        player1_pos[1] += player1_vel_y
        player2_vel_y += PLAYER_GRAVITY
        player2_pos[1] += player2_vel_y

        # Ground collision for players
        if player1_pos[1] >= HEIGHT - PLAYER_SIZE - 50:
            player1_pos[1] = HEIGHT - PLAYER_SIZE - 50
            player1_vel_y = 0
            player1_on_ground = True
            if player1_is_jumping:
                player1_is_jumping = False
                if player1_hit_timer <= 0:
                    set_player_animation_state(1, "idle")
                    
        if player2_pos[1] >= HEIGHT - PLAYER_SIZE - 50:
            player2_pos[1] = HEIGHT - PLAYER_SIZE - 50
            player2_vel_y = 0
            player2_on_ground = True
            if player2_is_jumping:
                player2_is_jumping = False
                if player2_hit_timer <= 0:
                    set_player_animation_state(2, "idle")

        # Cooldown updates
        if special_hit_cooldown_p1 > 0:
            special_hit_cooldown_p1 -= 1
        if special_hit_cooldown_p2 > 0:
            special_hit_cooldown_p2 -= 1

        # Handle real shuttle movement
        if shuttle_in_play:
            shuttle['vel'][1] += SHUTTLE_GRAVITY
            shuttle['pos'][0] += shuttle['vel'][0]
            shuttle['pos'][1] += shuttle['vel'][1]
            shuttle['vel'][0] *= SHUTTLE_FRICTION_X
            net_x = WIDTH // 2
            shuttle_x = shuttle['pos'][0]
            shuttle_y = shuttle['pos'][1]

            # Net collision
            if (net_x - SHUTTLE_RADIUS < shuttle_x < net_x + SHUTTLE_RADIUS and HEIGHT // 2 < shuttle_y < HEIGHT - 50):
                if last_hit_by == 1:
                    score2 += 1
                    server = 1
                elif last_hit_by == 2:
                    score1 += 1
                    server = 2
                reset_shuttle(server)
                continue

            # Shuttle floor collision (scoring)
            if shuttle['pos'][1] > HEIGHT-50:
                if shuttle['pos'][0] < WIDTH // 2:
                    score2 += 1
                    server = 1
                else:
                    score1 += 1
                    server = 2
                reset_shuttle(server)
            # Shuttle ceiling collision
            if shuttle['pos'][1] < 0:
                shuttle['vel'][1] *= -1
                shuttle['pos'][1] = 0

            # Shuttle wall collision
            if shuttle['pos'][0] < 0:
                shuttle['pos'][0] = 0
                shuttle['vel'][0] *= -1
            elif shuttle['pos'][0] > WIDTH:
                shuttle['pos'][0] = WIDTH
                shuttle['vel'][0] *= -1
        elif serving:
            if server == 1:
                shuttle['pos'] = [player1_pos[0] + PLAYER_SIZE_X // 2, player1_pos[1] - SHUTTLE_RADIUS * 2]
            else:
                shuttle['pos'] = [player2_pos[0] + PLAYER_SIZE_X // 2, player2_pos[1] - SHUTTLE_RADIUS * 2]
            if charging_serve:
                charge_power = min(MAX_SERVE_CHARGE_FRAMES, charge_power + 1)
            else:
                charge_power = 0

        # Player-shuttle collision (REAL SHUTTLE ONLY)
        player1_rect = pygame.Rect(player1_pos[0], player1_pos[1], PLAYER_SIZE_X, PLAYER_SIZE)
        player2_rect = pygame.Rect(player2_pos[0], player2_pos[1], PLAYER_SIZE_X, PLAYER_SIZE)
        shuttle_circle_rect = shuttle_image.get_rect(center=(int(shuttle['pos'][0]), int(shuttle['pos'][1])))

        hit_p1 = False
        hit_p2 = False

        # Player 1 collision and hitting
        if shuttle_in_play and player1_rect.colliderect(shuttle_circle_rect):
            if keys[pygame.K_q] or keys[pygame.K_e]:
                hit_p1 = True
                last_hit_by = 1
                play_sound_effect("smash")
                trigger_hit_animation(1)
                
                # Base hit
                shuttle['vel'][1] = -abs(shuttle['vel'][1])
                shuttle['vel'][0] = abs(SHUTTLE_SPEED_X_BASE)

                # Hit modifiers
                if keys[pygame.K_q]:  # Slow hit
                    shuttle['vel'][0] *= SLOW_HIT_MODIFIER_X
                    shuttle['vel'][1] *= SLOW_HIT_MODIFIER_Y
                elif keys[pygame.K_e]:  # Hard hit
                    shuttle['vel'][0] *= HARD_HIT_MODIFIER_X
                    shuttle['vel'][1] *= HARD_HIT_MODIFIER_Y

        # Player 2 collision and hitting
        if shuttle_in_play and player2_rect.colliderect(shuttle_circle_rect):
            if keys[pygame.K_COMMA] or keys[pygame.K_PERIOD]:
                hit_p2 = True
                last_hit_by = 2
                play_sound_effect("smash")
                trigger_hit_animation(2)
                
                # Base hit
                shuttle['vel'][1] = -abs(shuttle['vel'][1])
                shuttle['vel'][0] = -abs(SHUTTLE_SPEED_X_BASE)

                # Hit modifiers
                if keys[pygame.K_COMMA]:  # Slow hit
                    shuttle['vel'][0] *= SLOW_HIT_MODIFIER_X
                    shuttle['vel'][1] *= SLOW_HIT_MODIFIER_Y
                elif keys[pygame.K_PERIOD]:  # Hard hit
                    shuttle['vel'][0] *= HARD_HIT_MODIFIER_X
                    shuttle['vel'][1] *= HARD_HIT_MODIFIER_Y
                elif keys[pygame.K_SLASH] and special_hit_cooldown_p2 <= 0:  # Special hit (fake shuttles)
                    special_hit_cooldown_p2 = SPECIAL_HIT_COOLDOWN_FRAMES
                    # Create fake shuttles

        # Update animations
        update_player_animation(1)
        update_player_animation(2)

        # Check win condition
        if score1 >= WINNING_SCORE:
            game_over = True
            winner = 1
        elif score2 >= WINNING_SCORE:
            game_over = True
            winner = 2

        # Drawing
        screen.fill(WHITE)
        draw_court()
        
        # Draw players
        draw_player(screen, 1)
        draw_player(screen, 2)
        
        # Draw shuttle
        if shuttle_in_play or serving:
            draw_shuttle(shuttle)
        
        # Draw fake shuttles
        
        # Draw UI
        display_score()
        display_cooldowns()
        draw_serve_power(1)
        draw_serve_power(2)
        
        # Clean up fake shuttles that are off screen

    else:
        # Game over screen
        screen.fill(WHITE)
        display_game_over()
        if handle_game_over_input():
            continue

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()