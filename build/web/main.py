import pygame
import os
import asyncio
from os.path import join
from random import randint, uniform
import json
import requests

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.Vector2()
        self.speed = 300
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400
        self.mask = pygame.mask.from_surface(self.image)

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction.length() > 0 else self.direction
        
        # Keep player within screen bounds
        new_pos = self.rect.center + self.direction * self.speed * dt
        self.rect.center = (
            max(self.rect.width//2, min(WINDOW_WIDTH - self.rect.width//2, new_pos[0])),
            max(self.rect.height//2, min(WINDOW_HEIGHT - self.rect.height//2, new_pos[1]))
        )

        if keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            if laser_sound:
                laser_sound.play()

        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(midbottom=pos)

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.original_surf = surf
        self.image = surf
        self.rect = self.image.get_rect(center=pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 10000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 500)
        self.rotation_speed = randint(40, 80)
        self.rotation = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.rect.center = (
            self.rect.centerx + self.direction.x * self.speed * dt,
            self.rect.centery + self.direction.y * self.speed * dt
        )
        
        if (self.rect.top > WINDOW_HEIGHT or 
            pygame.time.get_ticks() - self.start_time >= self.lifetime):
            self.kill()
            
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        if explosion_sound:
            explosion_sound.play()

    def update(self, dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()

def collisions():
    global game_state
    
    # Player-meteor collision
    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, False, pygame.sprite.collide_mask)
    if collision_sprites:
        AnimatedExplosion(explosion_frames, player.rect.center, all_sprites)
        game_state = 'game_over'
        return

    # Laser-meteor collision
    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites:
            laser.kill()
            for sprite in collided_sprites:
                AnimatedExplosion(explosion_frames, sprite.rect.center, all_sprites)

def get_current_score():
    return (pygame.time.get_ticks() - game_start_time) // 100

def display_score():
    score = get_current_score()
    text_surf = font.render(str(score), True, (240, 240, 240))
    text_rect = text_surf.get_rect(midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, (240, 240, 240), text_rect.inflate(20, 10).move(0, -8), 5, 10)

def draw_text(text, font, color, surface, x, y, center=False):
    textobj = font.render(text, True, color)
    if center:
        textrect = textobj.get_rect(center=(x, y))
    else:
        textrect = textobj.get_rect(topleft=(x, y))
    surface.blit(textobj, textrect)
    return textrect

def draw_button(surface, text, font, color, bg_color, x, y, width, height):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, bg_color, button_rect)
    pygame.draw.rect(surface, color, button_rect, 2)
    
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=button_rect.center)
    surface.blit(text_surf, text_rect)
    
    return button_rect

# GitHub Gist configuration
GIST_ID = "dbbb7b95e20b9119cd4ece2664932aaa" 
API_TOKEN = os.environ.get('GITHUB_TOKEN', '')  # Set GITHUB_TOKEN in environment variables

def load_leaderboard():
    try:
        # Try local file first
        with open('leaderboard.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # File doesn't exist or is empty - return empty list
        pass
    except:
        # Other error - continue to web fallback
        pass
        
    # Web: Load from GitHub Gist
    try:
        url = f"https://api.github.com/gists/{GIST_ID}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            content = response.json()['files']['space-shooter-scores.json']['content']
            scores = json.loads(content)
            # Also save locally for future use
            try:
                with open('leaderboard.json', 'w') as f:
                    json.dump(scores, f)
            except:
                pass
            return scores
    except:
        # Fallback if network fails
        pass
    
    # Final fallback - return empty list
    return []

def save_leaderboard(scores):
    try:
        # Try local file first
        with open('leaderboard.json', 'w') as f:
            json.dump(scores, f, indent=2)
    except:
        # Local save failed - continue to web save
        pass
        
    # Web: Save to GitHub Gist
    try:
        if API_TOKEN:  # Only try web save if token is available
            url = f"https://api.github.com/gists/{GIST_ID}"
            data = {
                "files": {
                    "space-shooter-scores.json": {
                        "content": json.dumps(scores, indent=2)
                    }
                }
            }
            response = requests.patch(url, json=data, headers={
                "Authorization": f"token {API_TOKEN}",
                "Accept": "application/vnd.github.v3+json"
            }, timeout=5)
            # Don't raise exception if web save fails - local save is good enough
    except:
        pass  # Silently fail if network issues - local save should be sufficien
