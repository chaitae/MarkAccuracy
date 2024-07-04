import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600

# Create Pygame display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Draw Line Accuracy Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Font for displaying text
font = pygame.font.SysFont(None, 36)

# Game variables
drawing = False
trail_points = []
trail_thickness = 3
accuracy = 0.0
accuracy_position = (50, 50)

def generate_target_line():
    """Generate a new random target line centered horizontally with a biased length."""
    center_x = width // 2
    center_y = height // 2
    
    # Randomly choose the line length with a bias
    if random.random() < 0.8:  # 80% chance for lengths below 200 pixels
        line_length = random.randint(100, 200)
    else:
        line_length = random.randint(200, 260)
    
    # Randomly choose the angle in radians (0 to 2*pi)
    angle = random.uniform(0, 2*math.pi)
    
    # Calculate end points based on the center, length, and angle
    end_x = center_x + line_length * math.cos(angle)
    end_y = center_y + line_length * math.sin(angle)
    start_x = center_x - line_length * math.cos(angle)
    start_y = center_y - line_length * math.sin(angle)
    
    return (start_x, start_y), (end_x, end_y), line_length

def point_line_distance(point, start, end):
    """Calculate the distance of a point from a line segment."""
    px, py = point
    x1, y1 = start
    x2, y2 = end
    
    if x1 == x2 and y1 == y2:
        return math.dist(point, start)
    
    # Line segment vector
    lx, ly = x2 - x1, y2 - y1
    # Point vector
    dx, dy = px - x1, py - y1
    # Project point onto the line segment, clamped to [0,1]
    t = max(0, min(1, (dx * lx + dy * ly) / (lx * lx + ly * ly)))
    closest_point = (x1 + t * lx, y1 + t * ly)
    return math.dist(point, closest_point)

# Initial target line and length
target_start, target_end, target_length = generate_target_line()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            trail_points = [event.pos]
            drawing = True
        elif event.type == pygame.MOUSEBUTTONUP:
            trail_points.append(event.pos)
            drawing = False
            # Calculate accuracy
            if len(trail_points) > 1:
                distances = [point_line_distance(point, target_start, target_end) for point in trail_points]
                avg_distance = sum(distances) / len(distances)
                accuracy = max(0, 100 - avg_distance * 10)  # Increased penalty factor
                # Check if accuracy is 90% or higher
                if accuracy >= 85:
                    target_start, target_end, target_length = generate_target_line()
                    trail_points = []
                    accuracy = 0.0
        elif event.type == pygame.MOUSEMOTION and drawing:
            trail_points.append(event.pos)
    
    # Clear screen
    screen.fill(WHITE)
    
    # Draw target line
    pygame.draw.line(screen, RED, target_start, target_end, 2)
    
    # Draw the trail smoothly
    if trail_points:
        for i in range(len(trail_points) - 1):
            pygame.draw.line(screen, BLACK, trail_points[i], trail_points[i + 1], trail_thickness)
    
    # Render and display accuracy
    accuracy_text = font.render(f"Accuracy: {accuracy:.2f}%", True, BLUE)
    screen.blit(accuracy_text, accuracy_position)
    
    # Render and display target line length
    length_text = font.render(f"Line Length: {target_length:.2f} pixels", True, BLACK)
    screen.blit(length_text, (50, height - 50))
    
    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
