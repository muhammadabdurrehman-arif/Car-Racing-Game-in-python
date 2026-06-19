import pygame
import random
from pygame.locals import *

pygame.init()

# Window setup
width = 500
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Car Game")

# Colors
grey = (100, 100, 100)              
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)

# Game settings
gameover = False
speed = 2
score = 0

# Road and edge markers
road = (100, 0, 300, height)
left_edge_marker = (95, 0, 10, height)
right_edge_marker = (395, 0, 10, height)

# Lane positions
lanes = [150, 250, 350]

# Lane marker animation
lane_marker_move_y = 0

# Load crash image
crash_path = r"f:\Python programs\Simple car game racing\images\crash.png"
crash = pygame.image.load(crash_path)
crash_rect = crash.get_rect()


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)

        image_scale = 45 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (new_width, new_height))

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


class PlayerVehicle(Vehicle):
    def __init__(self, x, y):
        image_path = r"f:\Python programs\Simple car game racing\images\car.png"
        image = pygame.image.load(image_path)
        super().__init__(image, x, y)


class EnemyVehicle(Vehicle):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)


# Create player's car
player_group = pygame.sprite.Group()
player = PlayerVehicle(250, 400)
player_group.add(player)

# Load enemy vehicle images
images_filenames = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
vehicle_images = [pygame.image.load(f"f:\Python programs\Simple car game racing\images\\{img}") for img in images_filenames]

# Enemy vehicles
vehicle_group = pygame.sprite.Group()

# Game loop
clock = pygame.time.Clock()
fps = 30
running = True

while running:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Player movement
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.centerx > lanes[0]:
                player.rect.x -= 100
            elif event.key == K_RIGHT and player.rect.centerx < lanes[-1]:
                player.rect.x += 100

    # Detect collisions
    if pygame.sprite.spritecollide(player, vehicle_group, False):
        gameover = True

    # Draw background
    screen.fill(green)
    pygame.draw.rect(screen, grey, road)
    pygame.draw.rect(screen, yellow, left_edge_marker)
    pygame.draw.rect(screen, yellow, right_edge_marker)

    # Animate lane markers
    lane_marker_move_y += speed * 2
    if lane_marker_move_y >= 50 * 2:
        lane_marker_move_y = 0

    # Draw lane markers
    for y in range(-100, height, 100):
        pygame.draw.rect(screen, white, (lanes[0] + 45, y + lane_marker_move_y, 10, 50))
        pygame.draw.rect(screen, white, (lanes[1] + 45, y + lane_marker_move_y, 10, 50))

    # Spawn enemy vehicles
    if len(vehicle_group) < 2:
        add_vehicle = True
        for vehicle in vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 1.5:
                add_vehicle = False
        if add_vehicle:
            lane = random.choice(lanes)
            image = random.choice(vehicle_images)
            vehicle = EnemyVehicle(image, lane, -50)
            vehicle_group.add(vehicle)

    # Move enemy vehicles
    for vehicle in vehicle_group:
        vehicle.rect.y += speed
        if vehicle.rect.top >= height:
            vehicle.kill()

    # Increase speed over time
    score += 1
    if score % 3 == 0:
        speed += 0.5

    # Draw player and vehicles
    player_group.draw(screen)
    vehicle_group.draw(screen)

    # Display score
    font = pygame.font.Font(None, 24)
    text = font.render(f'Score: {score}', True, white)
    screen.blit(text, (50, 450))

    # Show crash if game over
    if gameover:
        screen.blit(crash, player.rect)
        pygame.draw.rect(screen, red, (0, 50, width, 100))
        text = font.render("Game Over! Play again? (Y/N)", True, white)
        screen.blit(text, (width / 2 - 100, 100))

        pygame.display.update()

        # Check if player wants to play again
        while gameover:
            clock.tick(fps)
            for event in pygame.event.get():
                if event.type == QUIT:
                    gameover = False
                    running = False

                if event.type == KEYDOWN:
                    if event.key == K_y:
                        # Reset the game
                        gameover = False
                        speed = 1
                        score = 0
                        vehicle_group.empty()
                        player.rect.center = (250, 400)
                    elif event.key == K_n:
                        # Exit the loops
                        gameover = False
                        running = False

    pygame.display.update()

pygame.quit()