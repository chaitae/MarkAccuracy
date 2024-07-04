
import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Draw Line Accuracy Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Game variables
drawing = False
start_pos = None
end_pos = None
target_length = 100

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            start_pos = event.pos
            drawing = True
        elif event.type == pygame.MOUSEBUTTONUP:
            end_pos = event.pos
            drawing = False
            if start_pos and end_pos:
                drawn_length = math.dist(start_pos, end_pos)
                accuracy = 100 - abs(drawn_length - target_length)
                print(f"Drawn length: {drawn_length}, Accuracy: {accuracy}%")

    # Clear screen
    screen.fill(WHITE)

    # Draw target line
    pygame.draw.line(screen, RED, (50, height//2), (50 + target_length, height//2), 2)

    # Draw user line
    if drawing and start_pos:
        end_pos = pygame.mouse.get_pos()
        pygame.draw.line(screen, BLACK, start_pos, end_pos, 2)

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
