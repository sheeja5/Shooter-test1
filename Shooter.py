# File: streamlit_shooting_game.py

import pygame
import random
import sys
import threading
import streamlit as st

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialize pygame
pygame.init()
pygame.font.init()

# Load assets
player_image = pygame.image.load("spaceship.png")
enemy_image = pygame.image.load("enemy.png")
bullet_image = pygame.image.load("bullet.png")

# Scale images
player_image = pygame.transform.scale(player_image, (50, 50))
enemy_image = pygame.transform.scale(enemy_image, (50, 50))
bullet_image = pygame.transform.scale(bullet_image, (10, 30))

# Game variables
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - 70
player_speed = 5

bullets = []
enemies = []
enemy_speed = 2
spawn_rate = 30  # Higher is slower spawn rate

score = 0
running = False


def draw_text(screen, text, x, y, font, color=WHITE):
    """Draws text on the screen."""
    label = font.render(text, True, color)
    screen.blit(label, (x, y))


def game_loop():
    """Runs the game loop in a separate thread."""
    global running, player_x, bullets, enemies, score

    # Initialize screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Shooting Game")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    running = True
    frame_count = 0

    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - 50:
            player_x += player_speed
        if keys[pygame.K_SPACE]:
            if len(bullets) < 5:  # Limit bullets
                bullets.append([player_x + 20, player_y])

        # Update bullets
        for bullet in bullets:
            bullet[1] -= 10  # Move bullet up
            if bullet[1] < 0:
                bullets.remove(bullet)

        # Spawn enemies
        frame_count += 1
        if frame_count % spawn_rate == 0:
            enemy_x = random.randint(0, SCREEN_WIDTH - 50)
            enemies.append([enemy_x, 0])

        # Update enemies
        for enemy in enemies:
            enemy[1] += enemy_speed
            if enemy[1] > SCREEN_HEIGHT:
                running = False  # Game over if enemy reaches bottom

        # Check for collisions
        for bullet in bullets:
            for enemy in enemies:
                if (
                    bullet[0] < enemy[0] + 50
                    and bullet[0] + 10 > enemy[0]
                    and bullet[1] < enemy[1] + 50
                    and bullet[1] + 30 > enemy[1]
                ):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1
                    break

        # Draw player
        screen.blit(player_image, (player_x, player_y))

        # Draw bullets
        for bullet in bullets:
            screen.blit(bullet_image, (bullet[0], bullet[1]))

        # Draw enemies
        for enemy in enemies:
            screen.blit(enemy_image, (enemy[0], enemy[1]))

        # Draw score
        draw_text(screen, f"Score: {score}", 10, 10, font)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


# Streamlit interface
st.title("Shooting Game")

if "game_thread" not in st.session_state:
    st.session_state.game_thread = None

if st.button("Start Game"):
    if not st.session_state.game_thread or not st.session_state.game_thread.is_alive():
        st.session_state.game_thread = threading.Thread(target=game_loop)
        st.session_state.game_thread.start()
        st.success("Game started! Check the Pygame window.")

if st.button("Stop Game"):
    running = False
    if st.session_state.game_thread and st.session_state.game_thread.is_alive():
        st.session_state.game_thread.join()
    st.warning("Game stopped.")
