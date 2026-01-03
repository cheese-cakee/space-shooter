import pygame
import os
import asyncio
from os.path import join
from random import randint, uniform
import json

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
<<<<<<< HEAD
    pygame.draw.rect(surface, bg_color, button_rect)  # ✅ FIXED: was 'react'
=======
    pygame.draw.rect(surface, bg_color, button_rect)
>>>>>>> 31e0b4bf8c684f32eb8e54a6676876b7ac9f12c0
    pygame.draw.rect(surface, color, button_rect, 2)
    
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=button_rect.center)
    surface.blit(text_surf, text_rect)
    
    return button_rect

def load_leaderboard():
    try:
        # Load from local file
        with open('leaderboard.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # File doesn't exist or is empty - return empty list
        return []

def save_leaderboard(scores):
    try:
        # Save to local file
        with open('leaderboard.json', 'w') as f:
            json.dump(scores, f, indent=2)
    except:
        pass  # Silently fail if save fails

def update_leaderboard(score):
    leaderboard = load_leaderboard()
    leaderboard.append(score)
    leaderboard.sort(reverse=True)
    leaderboard = leaderboard[:10]
    save_leaderboard(leaderboard)
    return leaderboard

async def main_menu():
    global game_state
    menu_running = True
    
    while menu_running:
        display_surface.fill('#1a1a2e')
        
        draw_text('SPACE SHOOTER', title_font, (240, 240, 240), display_surface, 
                 WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 150, center=True)
        
        draw_text('Survive the meteor storm!', font, (180, 180, 180), display_surface, 
                 WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 100, center=True)
        
        mx, my = pygame.mouse.get_pos()
        
        button_start = draw_button(display_surface, 'START GAME', font, (240, 240, 240), 
                                 (60, 60, 60), WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 20, 200, 50)
        
        button_leaderboard = draw_button(display_surface, 'LEADERBOARD', font, (240, 240, 240), 
                                       (60, 60, 60), WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 50, 200, 50)
        
        button_quit = draw_button(display_surface, 'QUIT', font, (240, 240, 240), 
                                (60, 60, 60), WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 120, 200, 50)
        
        draw_text('Arrow Keys: Move  |  Space: Shoot', small_font, (150, 150, 150), 
                 display_surface, WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50, center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Signal to quit
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_start.collidepoint(mx, my):
                    menu_running = False
                    game_state = 'playing'
                elif button_leaderboard.collidepoint(mx, my):
                    await show_leaderboard()
                elif button_quit.collidepoint(mx, my):
                    return False  # Signal to quit

        pygame.display.update()
        await asyncio.sleep(0)  # Essential for web deployment
    
    return True

async def game_over_screen():
    global game_state
    over_running = True
    final_score = get_current_score()
    
    leaderboard = update_leaderboard(final_score)
    is_high_score = len(leaderboard) > 0 and final_score == leaderboard[0]
    
    while over_running:
        display_surface.fill('#2e1a1a')
        
        draw_text('GAME OVER', title_font, (240, 100, 100), display_surface, 
                 WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 150, center=True)
        
        draw_text(f'Final Score: {final_score}', font, (240, 240, 240), display_surface, 
                 WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 80, center=True)
        
        if is_high_score:
            draw_text('NEW HIGH SCORE!', font, (255, 215, 0), display_surface, 
                     WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 40, center=True)
        
        mx, my = pygame.mouse.get_pos()
        
        button_restart = draw_button(display_surface, 'PLAY AGAIN', font, (240, 240, 240), 
                                   (60, 60, 60), WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 20, 200, 50)
        
        button_menu = draw_button(display_surface, 'MAIN MENU', font, (240, 240, 240), 
                                (60, 60, 60), WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 90, 200, 50)
        
        button_quit = draw_button(display_surface, 'QUIT', font, (240, 240, 240), 
                                (60, 60, 60), WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 160, 200, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_restart.collidepoint(mx, my):
                    over_running = False
                    reset_game()
                    game_state = 'playing'
                elif button_menu.collidepoint(mx, my):
                    over_running = False
                    game_state = 'menu'
                elif button_quit.collidepoint(mx, my):
                    return False

        pygame.display.update()
        await asyncio.sleep(0)
    
    return True

async def show_leaderboard():
    leaderboard_running = True
    leaderboard = load_leaderboard()
    
    while leaderboard_running:
        display_surface.fill('#1a2e1a')
        
        draw_text('LEADERBOARD', title_font, (100, 240, 100), display_surface, 
                 WINDOW_WIDTH / 2, 100, center=True)
        
        # Draw leaderboard box
        box_rect = pygame.Rect(WINDOW_WIDTH // 2 - 200, 160, 400, 350)
        pygame.draw.rect(display_surface, (40, 40, 40), box_rect)
        pygame.draw.rect(display_surface, (100, 240, 100), box_rect, 3)
        
        if leaderboard:
            y_offset = 200
            for i, score in enumerate(leaderboard[:10]):
                rank_text = f"{i + 1:2d}.  {score:6d}"
                color = (255, 215, 0) if i == 0 else (240, 240, 240) if i < 3 else (180, 180, 180)
                draw_text(rank_text, font, color, display_surface, 
                         WINDOW_WIDTH / 2, y_offset, center=True)
                y_offset += 35
        else:
            draw_text('No scores yet!', font, (180, 180, 180), display_surface, 
                     WINDOW_WIDTH / 2, 335, center=True)
        
        mx, my = pygame.mouse.get_pos()
        
        button_back = draw_button(display_surface, 'BACK', font, (240, 240, 240), 
                                 (60, 60, 60), WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT - 100, 150, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_back.collidepoint(mx, my):
                    leaderboard_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    leaderboard_running = False

        pygame.display.update()
        await asyncio.sleep(0)

def reset_game():
    global all_sprites, meteor_sprites, laser_sprites, player, game_start_time
    
    all_sprites.empty()
    meteor_sprites.empty()
    laser_sprites.empty()
    
    for i in range(20):
        Star(all_sprites, star_surf)
    
    player = Player(all_sprites)
    game_start_time = pygame.time.get_ticks()

def load_assets():
    global star_surf, meteor_surf, laser_surf, font, title_font, small_font
    global explosion_frames, laser_sound, explosion_sound, game_music
    
    try:
        star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
        meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
        laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
        
        font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 30)
        title_font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 48)
        small_font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 20)
        
        explosion_frames = [pygame.image.load(join('images', 'explosion', f'{i}.png')).convert_alpha() 
                           for i in range(21)]
        
        try:
            laser_sound = pygame.mixer.Sound(join('audio', 'laser.wav'))
            laser_sound.set_volume(0.5)
            explosion_sound = pygame.mixer.Sound(join('audio', 'explosion.wav'))
            game_music = pygame.mixer.Sound(join('audio', 'game_music.wav'))
            game_music.set_volume(0.4)
            game_music.play(loops=-1)
        except:
            # Fallback for web deployment without audio
            laser_sound = None
            explosion_sound = None
            game_music = None
            
    except Exception as e:
        # Fallback surfaces for web deployment
        star_surf = pygame.Surface((8, 8))
        star_surf.fill((255, 255, 255))
        meteor_surf = pygame.Surface((32, 32))
        meteor_surf.fill((139, 69, 19))
        laser_surf = pygame.Surface((4, 20))
        laser_surf.fill((0, 255, 0))
        
        font = pygame.font.Font(None, 30)
        title_font = pygame.font.Font(None, 48)
        small_font = pygame.font.Font(None, 20)
        
        explosion_frame = pygame.Surface((32, 32))
        explosion_frame.fill((255, 0, 0))
        explosion_frames = [explosion_frame] * 21
        
        laser_sound = None
        explosion_sound = None
        game_music = None

async def main():
    global display_surface, clock, all_sprites, meteor_sprites, laser_sprites
    global player, game_state, game_start_time, meteor_event, WINDOW_WIDTH, WINDOW_HEIGHT
    
    # Initialize Pygame
    pygame.init()
    WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
    display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Space Shooter')
    clock = pygame.time.Clock()
    
    # Load assets
    load_assets()
    
    # Initialize sprite groups
    all_sprites = pygame.sprite.Group()
    meteor_sprites = pygame.sprite.Group()
    laser_sprites = pygame.sprite.Group()
    
    # Initialize game
    reset_game()
    
    # Game variables
    game_state = 'menu'
    game_start_time = pygame.time.get_ticks()
    
    # Create meteor spawn event
    meteor_event = pygame.event.custom_type()
    pygame.time.set_timer(meteor_event, 500)
    
    # Main game loop
    running = True
    while running:
        dt = clock.tick(60) / 1000
        
        if game_state == 'menu':
            if not await main_menu():
                break
            if game_state == 'playing':
                reset_game()
                # Restart music when starting game
                if game_music:
                    game_music.play(loops=-1)
                
        elif game_state == 'playing':
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == meteor_event:
                    x = randint(0, WINDOW_WIDTH)
                    y = randint(-200, -100)
                    Meteor(meteor_surf, (x, y), (all_sprites, meteor_sprites))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_state = 'menu'
                        # Stop music when going to menu
                        if game_music:
                            game_music.stop()

            # Update game
            all_sprites.update(dt)
            collisions()

            # Draw game
            display_surface.fill('#3a2e3f')
            all_sprites.draw(display_surface)
            display_score()
            
            draw_text('ESC: Menu', small_font, (150, 150, 150), display_surface, 10, 10)
            
            pygame.display.update()
            
        elif game_state == 'game_over':
            if not await game_over_screen():
                break
        
        await asyncio.sleep(0)  # Essential for web deployment

    pygame.quit()

# Run the game
if __name__ == "__main__":
    asyncio.run(main())
