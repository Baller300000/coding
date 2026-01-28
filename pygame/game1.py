import pygame
import sys
import math
import random

pygame.init()

# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WORLD_WIDTH = 2400
WORLD_HEIGHT = 1800
fullscreen = False
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game - Press ESC to Restart, P to Pause, F for Fullscreen")
camera_x = 0
camera_y = 0

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

player_img = pygame.image.load('assets/player.gif')
player_img = pygame.transform.scale(player_img, (24, 24))

enemy_img = pygame.image.load('assets/enemy.gif')
enemy_img = pygame.transform.scale(enemy_img, (24, 24))

healer_img = pygame.image.load('assets/healer.gif')
healer_img = pygame.transform.scale(healer_img, (24, 24))

defender_img = pygame.image.load('assets/defender.gif')
defender_img = pygame.transform.scale(defender_img, (24, 24))

win_img = pygame.image.load('assets/win.gif')
win_img = pygame.transform.scale(win_img, (24, 24))

ver_wall_img = pygame.image.load('assets/ver_wall.gif')
ver_wall_img = pygame.transform.scale(ver_wall_img, (20, 100))

hor_wall_img = pygame.image.load('assets/hor_wall.gif')
hor_wall_img = pygame.transform.scale(hor_wall_img, (100, 20))

# Sprite classes
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.original_image = image
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.velocity_x = 0
        self.velocity_y = 0
        self.visible = True
        self.rotation = 0

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
    
    def set_rotation(self, angle):
        """Rotate the sprite and update collision rect and mask"""
        self.rotation = angle
        center = self.rect.center
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=center)
        self.mask = pygame.mask.from_surface(self.image)

    def collide(self, other):
        if self.rect.colliderect(other.rect):
            # Use mask collision for pixel-perfect detection
            offset = (other.rect.x - self.rect.x, other.rect.y - self.rect.y)
            try:
                if self.mask.overlap(other.mask, offset):
                    # Calculate overlap on each side
                    overlap_left = self.rect.right - other.rect.left
                    overlap_right = other.rect.right - self.rect.left
                    overlap_top = self.rect.bottom - other.rect.top
                    overlap_bottom = other.rect.bottom - self.rect.top
                    
                    # Find the smallest overlap to determine collision side
                    min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)
                    
                    if min_overlap == overlap_left:  # Hit from left
                        self.rect.right = other.rect.left
                        self.velocity_x = 0
                    elif min_overlap == overlap_right:  # Hit from right
                        self.rect.left = other.rect.right
                        self.velocity_x = 0
                    elif min_overlap == overlap_top:  # Hit from top
                        self.rect.bottom = other.rect.top
                        self.velocity_y = 0
                    elif min_overlap == overlap_bottom:  # Hit from bottom
                        self.rect.top = other.rect.bottom
                        self.velocity_y = 0
            except:
                pass

    def is_touching(self, other):
        if self.rect.colliderect(other.rect):
            offset = (other.rect.x - self.rect.x, other.rect.y - self.rect.y)
            try:
                return self.mask.overlap(other.mask, offset)
            except:
                return True
        return False

    def draw(self, surface):
        if self.visible:
            surface.blit(self.image, self.rect)


class Enemy(GameSprite):
    def __init__(self, x, y, image, speed=1):
        super().__init__(x, y, image)
        self.speed = speed
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.direction_timer = random.randint(60, 120)

    def update(self):
        self.direction_timer -= 1
        if self.direction_timer <= 0:
            self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            self.direction_timer = random.randint(60, 120)
        
        self.velocity_x = self.direction[0] * self.speed
        self.velocity_y = self.direction[1] * self.speed
        
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        
        # Bounce off walls
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.direction = (-self.direction[0], self.direction[1])
        if self.rect.top <= 50 or self.rect.bottom >= SCREEN_HEIGHT:
            self.direction = (self.direction[0], -self.direction[1])
        
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(50, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))


class Follower(Enemy):
    """Chases the player directly"""
    def __init__(self, x, y, image, speed=1):
        super().__init__(x, y, image, speed)
        self.ai_type = "Follower"
    
    def update(self):
        # Chase player
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            self.velocity_x = (dx / distance) * self.speed
            self.velocity_y = (dy / distance) * self.speed
        
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        
        # Bounce off screen edges
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.velocity_x *= -1
        if self.rect.top <= 50 or self.rect.bottom >= SCREEN_HEIGHT:
            self.velocity_y *= -1
        
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(50, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))


class Sitter(Enemy):
    """Stays mostly in place, moves slowly"""
    def __init__(self, x, y, image, speed=1):
        super().__init__(x, y, image, speed * 0.3)
        self.ai_type = "Sitter"
        self.patrol_center = (x, y)
        self.patrol_range = 50
    
    def update(self):
        self.direction_timer -= 1
        if self.direction_timer <= 0:
            self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            self.direction_timer = random.randint(90, 180)
        
        self.velocity_x = self.direction[0] * self.speed
        self.velocity_y = self.direction[1] * self.speed
        
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        
        # Stay near patrol center
        if abs(self.rect.centerx - self.patrol_center[0]) > self.patrol_range:
            self.rect.centerx = self.patrol_center[0]
        if abs(self.rect.centery - self.patrol_center[1]) > self.patrol_range:
            self.rect.centery = self.patrol_center[1]


class Bouncer(Enemy):
    """Bounces around randomly (original behavior)"""
    def __init__(self, x, y, image, speed=1):
        super().__init__(x, y, image, speed)
        self.ai_type = "Bouncer"
    
    def update(self):
        self.direction_timer -= 1
        if self.direction_timer <= 0:
            self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            self.direction_timer = random.randint(60, 120)
        
        self.velocity_x = self.direction[0] * self.speed
        self.velocity_y = self.direction[1] * self.speed
        
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        
        # Bounce off walls
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.direction = (-self.direction[0], self.direction[1])
        if self.rect.top <= 50 or self.rect.bottom >= SCREEN_HEIGHT:
            self.direction = (self.direction[0], -self.direction[1])
        
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(50, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))


class Teamer(Enemy):
    """Works with nearby enemies to surround the player"""
    def __init__(self, x, y, image, speed=1):
        super().__init__(x, y, image, speed)
        self.ai_type = "Teamer"
    
    def update(self):
        # Chase player like Follower, but coordinate with teammates
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            self.velocity_x = (dx / distance) * self.speed
            self.velocity_y = (dy / distance) * self.speed
        
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        
        # Bounce off screen edges
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.velocity_x *= -1
        if self.rect.top <= 50 or self.rect.bottom >= SCREEN_HEIGHT:
            self.velocity_y *= -1
        
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(50, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))


class Healer(GameSprite):
    """Allied character that follows the player and restores health"""
    def __init__(self, x, y, image, speed=1):
        super().__init__(x, y, image)
        self.speed = speed * 0.7  # Slower than player
        self.healing_range = 80
        self.heal_cooldown = 0
        self.heal_frequency = 120  # Heal every 2 seconds
        self.character_type = "Healer"
    
    def update(self):
        # Follow player at a distance
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 50:  # Don't get too close
            self.velocity_x = (dx / distance) * self.speed
            self.velocity_y = (dy / distance) * self.speed
        else:
            self.velocity_x = 0
            self.velocity_y = 0
        
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        
        # Keep within world bounds
        self.rect.x = max(0, min(self.rect.x, WORLD_WIDTH - self.rect.width))
        self.rect.y = max(50, min(self.rect.y, WORLD_HEIGHT - self.rect.height))
        
        # Healing logic
        self.heal_cooldown -= 1
        if self.heal_cooldown <= 0 and distance < self.healing_range:
            # Heal the player
            game_state.lives = min(game_state.lives + 1, 5)  # Max 5 lives
            game_state.score += 10
            self.heal_cooldown = self.heal_frequency


class Defender(GameSprite):
    """Allied character that blocks enemies and protects the player"""
    def __init__(self, x, y, image, speed=1):
        super().__init__(x, y, image)
        self.speed = speed * 0.8
        self.protection_range = 100
        self.shield_cooldown = 0
        self.character_type = "Defender"
    
    def update(self):
        # Position near player to intercept enemies
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 80:  # Keep a medium distance
            self.velocity_x = (dx / distance) * self.speed
            self.velocity_y = (dy / distance) * self.speed
        else:
            self.velocity_x = 0
            self.velocity_y = 0
        
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        
        # Keep within world bounds
        self.rect.x = max(0, min(self.rect.x, WORLD_WIDTH - self.rect.width))
        self.rect.y = max(50, min(self.rect.y, WORLD_HEIGHT - self.rect.height))
        
        # Collision with walls
        for wall in walls:
            self.collide(wall)


class GameState:
    def __init__(self):
        self.level = 1
        self.score = 0
        self.time_elapsed = 0
        self.game_over = False
        self.game_won = False
        self.paused = False
        self.player_moved = False
        self.win_timer = 0
        self.high_score = 0
        self.best_time = float('inf')
        self.lives = 3
        self.enemy_catch_count = 0
        self.power_ups = []
        self.invincible_timer = 0
        self.speed_boost_timer = 0
        self.allies = []
        self.colors = {}
        self.reset_level()
    
    def get_level_colors(self):
        """Get random color scheme based on current level"""
        random.seed(self.level * 42)
        
        # Generate random but aesthetically pleasing colors
        bg_brightness = random.randint(220, 255)
        bg = (
            min(bg_brightness, 255),
            min(bg_brightness + random.randint(-20, 20), 255),
            min(bg_brightness + random.randint(-20, 20), 255)
        )
        
        primary = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )
        
        secondary = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )
        
        random.seed()
        
        return {'bg': bg, 'primary': primary, 'secondary': secondary}
    
    def reset_level(self):
        self.time_elapsed = 0
        self.game_over = False
        self.game_won = False
        self.player_moved = False
        self.win_timer = 0
        self.invincible_timer = 0
        self.speed_boost_timer = 0
        self.allies = []
        self.setup_level()
    
    def setup_level(self):
        global player, enemies, walls, win
        
        player = GameSprite(WORLD_WIDTH // 4, WORLD_HEIGHT // 4, player_img)
        
        # Spawn win at random location, at least 256 pixels away from player
        valid_spawn = False
        while not valid_spawn:
            win_x = random.randint(100, WORLD_WIDTH - 100)
            win_y = random.randint(100, WORLD_HEIGHT - 100)
            distance = math.sqrt((win_x - player.rect.centerx)**2 + (win_y - player.rect.centery)**2)
            if distance >= 256:
                valid_spawn = True
        
        win = GameSprite(win_x, win_y, win_img)
        
        # Create enemies with increasing difficulty
        enemies = []
        enemy_count = min(20, 8 + self.level * 2)
        ai_types = [Follower, Bouncer, Sitter, Teamer]
        
        for i in range(enemy_count):
            x = random.randint(100, WORLD_WIDTH - 100)
            y = random.randint(100, WORLD_HEIGHT - 100)
            speed = 3 * 0.85
            ai_class = ai_types[i % len(ai_types)]
            enemies.append(ai_class(x, y, enemy_img, speed))
        
        # Generate procedural walls based on level seed
        walls = []
        random.seed(self.level * 12345)
        
        wall_count = 80 + self.level * 8
        for i in range(wall_count):
            x = random.randint(100, WORLD_WIDTH - 100)
            y = random.randint(100, WORLD_HEIGHT - 100)
            wall_type = random.choice([ver_wall_img, hor_wall_img])
            rotation = random.choice([0, 45, 90, 135])
            
            wall = GameSprite(x, y, wall_type)
            wall.set_rotation(rotation)
            walls.append(wall)
        
        # Spawn power-ups
        self.power_ups = []
        power_up_count = 2 + self.level
        for i in range(power_up_count):
            pu_x = random.randint(200, WORLD_WIDTH - 200)
            pu_y = random.randint(200, WORLD_HEIGHT - 200)
            pu_type = random.choice(['invincible', 'speed_boost'])
            self.power_ups.append({'x': pu_x, 'y': pu_y, 'type': pu_type, 'active': True})
        
        # Spawn allied characters (Healer and Defender)
        self.allies = []
        
        # Spawn Healer
        healer_x = random.randint(WORLD_WIDTH // 4, WORLD_WIDTH // 2)
        healer_y = random.randint(WORLD_HEIGHT // 4, WORLD_HEIGHT // 2)
        self.allies.append(Healer(healer_x, healer_y, healer_img, speed=3 * 0.85))
        
        # Spawn Defender
        defender_x = random.randint(WORLD_WIDTH // 2, 3 * WORLD_WIDTH // 4)
        defender_y = random.randint(WORLD_HEIGHT // 4, WORLD_HEIGHT // 2)
        self.allies.append(Defender(defender_x, defender_y, defender_img, speed=3 * 0.85))
        
        random.seed()


class PowerUp:
    """Power-up system"""
    INVINCIBLE = 'invincible'
    SPEED_BOOST = 'speed_boost'
    INVINCIBLE_DURATION = 300  # 5 seconds at 60 FPS
    SPEED_BOOST_DURATION = 240  # 4 seconds at 60 FPS
    SPEED_MULTIPLIER = 1.5


font_large = pygame.font.SysFont(None, 72)
font_medium = pygame.font.SysFont(None, 48)
font_small = pygame.font.SysFont(None, 32)

game_state = GameState()
player = game_state.player = GameSprite(25, 75, player_img)
enemies = game_state.enemies = []
walls = game_state.walls = []
game_state.setup_level()

clock = pygame.time.Clock()

def tint_image(image, color):
    """Apply color tint to an image"""
    tinted = image.convert().copy()
    # Use a more effective tinting method
    # Create a colored surface and blend it over the image
    tint_surface = pygame.Surface(tinted.get_size())
    tint_surface.fill(color)
    tint_surface.set_alpha(128)  # 50% opacity for the tint
    tinted.blit(tint_surface, (0, 0))
    return tinted

def draw_text(text, font, color, pos):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)

def draw_ui():
    draw_text(f"Level: {game_state.level}", font_small, BLACK, (10, 10))
    draw_text(f"Score: {game_state.score}", font_small, BLACK, (10, 40))
    draw_text(f"Lives: {game_state.lives}", font_small, BLACK, (10, 70))
    draw_text(f"Time: {game_state.time_elapsed // 60}s", font_small, BLACK, (SCREEN_WIDTH - 200, 10))
    draw_text(f"High Score: {game_state.high_score}", font_small, BLACK, (SCREEN_WIDTH - 250, 40))
    
    # Draw ally status
    draw_text(f"Allies: {len(game_state.allies)}", font_small, GREEN, (10, 100))
    for i, ally in enumerate(game_state.allies):
        ally_name = ally.character_type if hasattr(ally, 'character_type') else 'Unknown'
        draw_text(f"  - {ally_name}", font_small, GREEN, (20, 125 + i * 25))
    
    # Draw power-up status
    if game_state.invincible_timer > 0:
        draw_text("INVINCIBLE!", font_small, YELLOW, (SCREEN_WIDTH // 2 - 100, 10))
    if game_state.speed_boost_timer > 0:
        draw_text("SPEED BOOST!", font_small, BLUE, (SCREEN_WIDTH // 2 - 120, 40))
    
    if game_state.paused:
        draw_text("PAUSED - Press P to Resume", font_medium, RED, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2))

def draw_end_screen():
    if game_state.game_over:
        draw_text("YOU LOST!", font_large, RED, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50))
        draw_text("Press ESC to Restart", font_small, BLACK, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50))
    elif game_state.game_won:
        draw_text("YOU WON!", font_large, GREEN, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50))
        draw_text(f"Time: {game_state.time_elapsed // 60}s", font_small, BLACK, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        draw_text("Press ESC for Next Level", font_small, BLACK, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 50))


# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_state.game_over or game_state.game_won:
                    if game_state.game_won:
                        game_state.level += 1
                    game_state.reset_level()
            if event.key == pygame.K_p:
                game_state.paused = not game_state.paused
            if event.key == pygame.K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            if event.key == pygame.K_r:
                game_state.reset_level()


    if not game_state.paused:
        keys = pygame.key.get_pressed()

        # initial speed
        player_speed = 3
        if game_state.speed_boost_timer > 0:
            player_speed = 3 * PowerUp.SPEED_MULTIPLIER
        
        player.velocity_x = 0
        player.velocity_y = 0

        # player movement
        if keys[pygame.K_UP]:
            player.velocity_y = -player_speed
            game_state.player_moved = True
        if keys[pygame.K_DOWN]:
            player.velocity_y = player_speed
            game_state.player_moved = True
        if keys[pygame.K_LEFT]:
            player.velocity_x = -player_speed
            game_state.player_moved = True
        if keys[pygame.K_RIGHT]:
            player.velocity_x = player_speed
            game_state.player_moved = True

        # Update player position
        player.update()

        # anti-off-screen
        if player.rect.right >= WORLD_WIDTH:
            player.rect.right = WORLD_WIDTH
        if player.rect.left <= 0:
            player.rect.left = 0
        if player.rect.top <= 50:
            player.rect.top = 50
        if player.rect.bottom >= WORLD_HEIGHT:
            player.rect.bottom = WORLD_HEIGHT

        # collision with walls
        for wall in walls:
            player.collide(wall)

        # Check power-up collisions
        for pu in game_state.power_ups:
            if pu['active']:
                distance = math.sqrt((pu['x'] - player.rect.centerx)**2 + (pu['y'] - player.rect.centery)**2)
                if distance < 30:
                    pu['active'] = False
                    if pu['type'] == 'invincible':
                        game_state.invincible_timer = PowerUp.INVINCIBLE_DURATION
                        game_state.score += 50
                    elif pu['type'] == 'speed_boost':
                        game_state.speed_boost_timer = PowerUp.SPEED_BOOST_DURATION
                        game_state.score += 25

        # Update timers
        if game_state.invincible_timer > 0:
            game_state.invincible_timer -= 1
        if game_state.speed_boost_timer > 0:
            game_state.speed_boost_timer -= 1

        # Update enemies only after player moves
        if game_state.player_moved:
            for enemy in enemies:
                enemy.update()
                # Collision with walls
                for wall in walls:
                    enemy.collide(wall)
            
            # Update allies
            for ally in game_state.allies:
                ally.update()
        
        # Update camera to follow player
        camera_x = player.rect.centerx - SCREEN_WIDTH // 2
        camera_y = player.rect.centery - SCREEN_HEIGHT // 2
        camera_x = max(0, min(camera_x, WORLD_WIDTH - SCREEN_WIDTH))
        camera_y = max(0, min(camera_y, WORLD_HEIGHT - SCREEN_HEIGHT))

        # win/lose functions
        if not game_state.game_over and not game_state.game_won:
            enemy_collision = any(player.is_touching(enemy) for enemy in enemies)
            if enemy_collision and game_state.invincible_timer <= 0:
                game_state.lives -= 1
                if game_state.lives <= 0:
                    game_state.game_over = True
                    if game_state.score > game_state.high_score:
                        game_state.high_score = game_state.score
                else:
                    # Reset position and invincibility briefly
                    player.rect.center = (WORLD_WIDTH // 4, WORLD_HEIGHT // 4)
                    game_state.invincible_timer = 120
            elif player.is_touching(win):
                game_state.game_won = True
                game_state.score += 100 + (game_state.level * 50)
                if game_state.time_elapsed < game_state.best_time:
                    game_state.best_time = game_state.time_elapsed
                if game_state.score > game_state.high_score:
                    game_state.high_score = game_state.score
                game_state.win_timer = 180
        
        # Auto advance level after winning
        if game_state.game_won and game_state.win_timer > 0:
            game_state.win_timer -= 1
            if game_state.win_timer == 0:
                game_state.level += 1
                game_state.reset_level()
        
        # Time tracking
        game_state.time_elapsed += 1

    # Draw everything
    colors = game_state.get_level_colors()
    screen.fill(colors['bg'])
    
    # Draw walls with camera offset
    for wall in walls:
        screen_x = wall.rect.x - camera_x
        screen_y = wall.rect.y - camera_y
        if -100 < screen_x < SCREEN_WIDTH + 100 and -100 < screen_y < SCREEN_HEIGHT + 100:
            tinted_wall = tint_image(wall.image, colors['primary'])
            screen.blit(tinted_wall, (screen_x, screen_y))
    
    # Draw power-ups with camera offset
    for pu in game_state.power_ups:
        if pu['active']:
            screen_x = pu['x'] - camera_x
            screen_y = pu['y'] - camera_y
            if -50 < screen_x < SCREEN_WIDTH + 50 and -50 < screen_y < SCREEN_HEIGHT + 50:
                color = YELLOW if pu['type'] == 'invincible' else BLUE
                pygame.draw.circle(screen, color, (int(screen_x), int(screen_y)), 8)
    
    # Draw enemies with camera offset
    for enemy in enemies:
        screen_x = enemy.rect.x - camera_x
        screen_y = enemy.rect.y - camera_y
        if -50 < screen_x < SCREEN_WIDTH + 50 and -50 < screen_y < SCREEN_HEIGHT + 50:
            tinted_enemy = tint_image(enemy.image, colors['secondary'])
            screen.blit(tinted_enemy, (screen_x, screen_y))
    
    # Draw allies with camera offset
    for ally in game_state.allies:
        screen_x = ally.rect.x - camera_x
        screen_y = ally.rect.y - camera_y
        if -50 < screen_x < SCREEN_WIDTH + 50 and -50 < screen_y < SCREEN_HEIGHT + 50:
            # Draw allies with a different tint - use green for visual distinction
            screen.blit(ally.image, (screen_x, screen_y))
            # Draw a green border/indicator to show they're allies
            pygame.draw.rect(screen, GREEN, (int(screen_x) - 2, int(screen_y) - 2, ally.rect.width + 4, ally.rect.height + 4), 2)
    
    # Draw player with camera offset (flash if invincible)
    screen_x = player.rect.x - camera_x
    screen_y = player.rect.y - camera_y
    if player.visible:
        if game_state.invincible_timer > 0 and (game_state.invincible_timer // 10) % 2 == 0:
            # Flash effect when invincible
            pass
        else:
            tinted_player = tint_image(player.image, colors['primary'])
            screen.blit(tinted_player, (screen_x, screen_y))

    draw_ui()
    draw_end_screen()

    pygame.display.flip()
    clock.tick(60)