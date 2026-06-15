import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Animated Story")

CLOCK = pygame.time.Clock()
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 235)

character_x = 50
character_y = 400
character_speed = 3

# --- MAIN GAME LOOP ---
running = True
while running:
    # A. Handle Events (Inputs, closing the window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # B. Update Positions (The "Animation" Logic)
    character_x += character_speed
    
    # Reset position if it walks off screen (like a looping movie)
    if character_x > SCREEN_WIDTH:
        character_x = -50 

    # C. Drawing the Scene
    screen.fill(SKY_BLUE)  # Background color
    
    # Draw a ground line
    pygame.draw.rect(screen, (34, 139, 34), (0, 450, SCREEN_WIDTH, 150))
    
    # Draw a simple character (a yellow circle for now!)
    # In a real project, you can replace this with pygame.image.load('hero.png')
    pygame.draw.circle(screen, (255, 223, 0), (character_x, character_y), 30)

    # D. Flip the display to show the new frame
    pygame.display.flip()

    # E. Cap the frame rate at 60 FPS
    CLOCK.tick(60)

pygame.quit()
sys.exit()