import pygame
import sys
import random

# --- 1. INITIALIZATION & SETUP ---
pygame.init()
pygame.font.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Khartoum: The Silent Road")

CLOCK = pygame.time.Clock()
FPS = 60

# --- 2. COLOR DESIGN (Cinematic & Grim) ---
CHARCOAL    = (15, 15, 18)
SILHOUETTE  = (28, 26, 28)
DUST_GOLD   = (210, 180, 140)
NIGHT_BLUE  = (20, 24, 38)
TEXT_WHITE  = (240, 240, 245)
BEAM_YELLOW = (255, 240, 150, 60)  # RGBA: The 4th number adds transparency!
CRIMSON     = (200, 35, 45)
EMERALD     = (45, 180, 105)

# --- 3. FONTS ---
font_title = pygame.font.SysFont("Courier New", 36, bold=True)
font_body  = pygame.font.SysFont("Arial", 20)
font_ui    = pygame.font.SysFont("Courier New", 16, bold=True)

# --- 4. GAME STATE ENGINE ---
# Scenes: TITLE, ACT_1, ACT_1_END, ACT_2, ACT_3, GAME_OVER, VICTORY
scene = "TITLE"
alert_level = 0.0
max_alert = 100.0
input_cooldown = 0

# Player Mechanics
player_x = 60
player_y = 480
player_speed = 3
is_hiding = False

# Act 1: Militia Searchlight Mechanics
searchlight_x = 300
searchlight_direction = 1
searchlight_speed = 4

# Act 3: Patrol Truck & Sweeping Headlights
truck_beam_angle = 0
beam_sweep_dir = 1

# Ambient Dust Particles for Atmosphere
particles = [{"x": random.randint(0, 1000), "y": random.randint(0, 700), "speed": random.uniform(0.5, 1.5)} for _ in range(40)]

# --- 5. SYSTEM HELPER FUNCTIONS ---
def draw_background_elements(color):
    """Draws ruins, crumbling walls, and atmospheric dust particles."""
    screen.fill(color)
    
    # Draw environmental background silhouettes
    pygame.draw.rect(screen, SILHOUETTE, (0, 180, 180, 350))
    pygame.draw.rect(screen, SILHOUETTE, (320, 220, 240, 310))
    pygame.draw.rect(screen, SILHOUETTE, (700, 150, 350, 380))
    pygame.draw.rect(screen, (10, 9, 12), (0, 520, SCREEN_WIDTH, 180)) # Ground plane
    
    # Render moving dust particles
    for p in particles:
        p["x"] -= p["speed"]
        if p["x"] < 0:
            p["x"] = SCREEN_WIDTH
            p["y"] = random.randint(0, 600)
        pygame.draw.circle(screen, (80, 75, 70), (int(p["x"]), int(p["y"])), 2)

def draw_hud():
    """Draws a functional visibility meter and objective header."""
    # Label
    lbl = font_ui.render("DETECTION RISK PROFILE", True, TEXT_WHITE)
    screen.blit(lbl, (40, 25))
    # Outer Bar
    pygame.draw.rect(screen, TEXT_WHITE, (40, 50, 250, 18), 2)
    # Filling Meter dynamically
    if alert_level > 0:
        bar_color = CRIMSON if alert_level > 60 else DUST_GOLD
        pygame.draw.rect(screen, bar_color, (43, 53, int((alert_level / max_alert) * 244), 13))

def draw_dialogue(lines):
    """Renders typewriter-style narrative interfaces at the base of the frame."""
    box = pygame.Rect(40, 550, 920, 120)
    pygame.draw.rect(screen, CHARCOAL, box, border_radius=6)
    pygame.draw.rect(screen, (40, 40, 45), box, 2, border_radius=6)
    
    y = 565
    for line in lines:
        surf = font_body.render(line, True, TEXT_WHITE)
        screen.blit(surf, (70, y))
        y += 28
        
    prompt = font_ui.render("[ PRESS SPACEBAR ]", True, CRIMSON)
    screen.blit(prompt, (800, 635))

# --- 6. CORE GAME LOOP ---
running = True
while running:
    if input_cooldown > 0:
        input_cooldown -= 1

    # Check for core window events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    # Handle Scene Changes with Spacebar Cooldowns
    if keys[pygame.K_SPACE] and input_cooldown == 0:
        input_cooldown = 25
        if scene == "TITLE":
            scene = "ACT_1"
            player_x = 60
            alert_level = 0
        elif scene == "ACT_1" and player_x >= 920:
            scene = "ACT_1_END"
        elif scene == "ACT_1_END":
            scene = "ACT_2"
        elif scene == "ACT_3" and player_x >= 920:
            scene = "VICTORY"
        elif scene == "GAME_OVER":
            scene = "TITLE"
            alert_level = 0

    # Fail Condition Trigger
    if alert_level >= max_alert:
        scene = "GAME_OVER"

    # --- SCENE RENDERING PIPELINE ---
    
    if scene == "TITLE":
        screen.fill(CHARCOAL)
        title_text = font_title.render("KHARTOUM: THE SILENT ROAD", True, TEXT_WHITE)
        desc_1 = font_body.render("Escape the patrol lines under the cover of shadow.", True, DUST_GOLD)
        desc_2 = font_body.render("Controls: [LEFT/RIGHT ARROWS] to Move | Hold [DOWN ARROW] to Hide.", True, TEXT_WHITE)
        prompt = font_ui.render("PRESS SPACEBAR TO INITIATE ESCAPE", True, CRIMSON)
        
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 220))
        screen.blit(desc_1, (SCREEN_WIDTH//2 - desc_1.get_width()//2, 300))
        screen.blit(desc_2, (SCREEN_WIDTH//2 - desc_2.get_width()//2, 350))
        screen.blit(prompt, (SCREEN_WIDTH//2 - prompt.get_width()//2, 480))

    elif scene == "ACT_1":
        draw_background_elements(NIGHT_BLUE)
        
        # Mechanics: Searchlight movement logic
        searchlight_x += searchlight_speed * searchlight_direction
        if searchlight_x > 850 or searchlight_x < 250:
            searchlight_direction *= -1

        # Transparent Surface Setup for the searchlight cone
        light_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(light_surface, BEAM_YELLOW, [(500, 0), (searchlight_x - 80, 530), (searchlight_x + 80, 530)])
        screen.blit(light_surface, (0, 0))

        # Input Parsing & Movement
        if keys[pygame.K_DOWN]:
            is_hiding = True
            if alert_level > 0: alert_level -= 0.4
        else:
            is_hiding = False
            if keys[pygame.K_RIGHT]: player_x += player_speed
            if keys[pygame.K_LEFT]: player_x -= player_speed

        # Collision Check: Is player standing in the light cone beams?
        if not is_hiding and (searchlight_x - 70 < player_x < searchlight_x + 70):
            alert_level += 1.2
            pygame.draw.rect(screen, CRIMSON, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 3) # Flash red indicator
            
        # Draw Player
        if is_hiding:
            pygame.draw.ellipse(screen, (15, 15, 15), (player_x, player_y + 25, 26, 15))
        else:
            pygame.draw.rect(screen, TEXT_WHITE, (player_x, player_y, 20, 40), border_radius=3)

        draw_hud()
        
        if player_x < 850:
            draw_dialogue([
                "Act I: Leaving the District.",
                "An RSF checkpoint watchtower is sweeping the main crossroads ahead.",
                "Hold [DOWN ARROW] to blend into the rubble when the beam passes over you!"
            ])
        else:
            draw_dialogue([
                "You successfully slipped past the checkpoint perimeter box.",
                "The shadows of the back streets offer brief safety.",
                "Advance forward to look for an exit corridor."
            ])

    elif scene == "ACT_1_END":
        screen.fill(CHARCOAL)
        draw_dialogue([
            "You manage to connect with a local emergency volunteer group over text.",
            "They inform you that the last safe route across the checkpoint line is closing.",
            "An open path remains through an old industrial depot, but patrols are closing in.",
        ])

    elif scene == "ACT_2":
        screen.fill(CHARCOAL)
        title_c = font_title.render("DECISION HUB: THE RIVER FORK", True, CRIMSON)
        screen.blit(title_c, (SCREEN_WIDTH//2 - title_c.get_width()//2, 120))
        
        # Left Fork UI Box
        pygame.draw.rect(screen, SILHOUETTE, (80, 240, 380, 240), border_radius=6)
        pygame.draw.rect(screen, DUST_GOLD, (80, 240, 380, 240), 2, border_radius=6)
        t_a1 = font_ui.render("ROUTE A: THE EMBANKMENT WALKS", True, DUST_GOLD)
        t_a2 = font_body.render("Sneak through low mud ditches.", True, TEXT_WHITE)
        t_a3 = font_body.render("Modifies: Harder visibility, slow speed.", True, TEXT_WHITE)
        t_a4 = font_ui.render("[ PRESS 'A' KEY ]", True, TEXT_WHITE)
        screen.blit(t_a1, (110, 270)); screen.blit(t_a2, (110, 320)); screen.blit(t_a3, (110, 360)); screen.blit(t_a4, (110, 420))
        
        # Right Fork UI Box
        pygame.draw.rect(screen, SILHOUETTE, (540, 240, 380, 240), border_radius=6)
        pygame.draw.rect(screen, CRIMSON, (540, 240, 380, 240), 2, border_radius=6)
        t_b1 = font_ui.render("ROUTE B: THE FREIGHT TERMINAL", True, CRIMSON)
        t_b2 = font_body.render("Sprint past open cargo structures.", True, TEXT_WHITE)
        t_b3 = font_body.render("Modifies: Maximum running speed allowed.", True, TEXT_WHITE)
        t_b4 = font_ui.render("[ PRESS 'B' KEY ]", True, TEXT_WHITE)
        screen.blit(t_b1, (570, 270)); screen.blit(t_b2, (570, 320)); screen.blit(t_b3, (570, 360)); screen.blit(t_b4, (570, 420))
        
        if keys[pygame.K_a]:
            player_speed = 2
            alert_level = max(0, alert_level - 15)  # Safe route benefit
            player_x = 50
            scene = "ACT_3"
        if keys[pygame.K_b]:
            player_speed = 5
            alert_level = min(90, alert_level + 15) # Dangerous route cost
            player_x = 50
            scene = "ACT_3"

    elif scene == "ACT_3":
        draw_background_elements(DUST_AMBER)
        
        # Mechanics: Complex moving headlight beam loop
        truck_beam_angle += 0.04 * beam_sweep_dir
        if truck_beam_angle > 1.2 or truck_beam_angle < -0.2:
            beam_sweep_dir *= -1
            
        # Form dynamic geometric sweeping light polygons using trigonometry scales
        beam_target_x1 = 400 + (truck_beam_angle * 300)
        beam_target_x2 = 600 + (truck_beam_angle * 300)
        
        light_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(light_surface, BEAM_YELLOW, [(0, 100), (beam_target_x1, 520), (beam_target_x2, 520)])
        screen.blit(light_surface, (0, 0))
        
        # Stationary Mounted Patrol Truck Shape
        pygame.draw.rect(screen, SILHOUETTE, (0, 60, 120, 70), border_radius=4)
        pygame.draw.circle(screen, CRIMSON, (100, 80), 4) # Engine run notification
        
        # Input Actions
        if keys[pygame.K_DOWN]:
            is_hiding = True
            if alert_level > 0: alert_level -= 0.3
        else:
            is_hiding = False
            if keys[pygame.K_RIGHT]: player_x += player_speed
            if keys[pygame.K_LEFT]: player_x -= player_speed

        # Structural Detection Checking
        if not is_hiding and (beam_target_x1 - 30 < player_x < beam_target_x2 + 30):
            alert_level += 1.8
            pygame.draw.rect(screen, CRIMSON, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 4)

        # Draw Player
        if is_hiding:
            pygame.draw.ellipse(screen, (20, 18, 15), (player_x, player_y + 25, 26, 15))
        else:
            pygame.draw.rect(screen, TEXT_WHITE, (player_x, player_y, 20, 40), border_radius=3)
            
        draw_hud()
        draw_dialogue([
            "Act III: The Final Dash.",
            "A patrol vehicle down the highway is actively washing the terrain with high beams.",
            "Reach the eastern edge of the screen layout to clear the safe zone perimeter!"
        ])

    elif scene == "GAME_OVER":
        screen.fill((10, 5, 5))
        g_txt = font_title.render("DETECTION ARCHIVE: INTERCEPTED", True, CRIMSON)
        sub_g = font_body.render("Your profile was logged by a roving patrol sweep.", True, TEXT_WHITE)
        p_g   = font_ui.render("PRESS SPACEBAR TO REBOOT PROTOCOL SYSTEMS AND RETRY", True, DUST_GOLD)
        
        screen.blit(g_txt, (SCREEN_WIDTH//2 - g_txt.get_width()//2, 240))
        screen.blit(sub_g, (SCREEN_WIDTH//2 - sub_g.get_width()//2, 320))
        screen.blit(p_g, (SCREEN_WIDTH//2 - p_g.get_width()//2, 450))

    elif scene == "VICTORY":
        screen.fill(CHARCOAL)
        v_txt = font_title.render("SAFE AREA REACHED: JOURNEY RESOLVED", True, EMERALD)
        sub_v = font_body.render("You successfully crossed out of the conflict lines into a civilian corridor.", True, TEXT_WHITE)
        credit = font_ui.render("Thank you for playing. Final Project submission complete.", True, DUST_GOLD)
        
        screen.blit(v_txt, (SCREEN_WIDTH//2 - v_txt.get_width()//2, 240))
        screen.blit(sub_v, (SCREEN_WIDTH//2 - sub_v.get_width()//2, 320))
        screen.blit(credit, (SCREEN_WIDTH//2 - credit.get_width()//2, 450))

    pygame.display.flip()
    CLOCK.tick(FPS)

pygame.quit()
sys.exit()