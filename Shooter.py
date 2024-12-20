import streamlit as st
import random
import time

#Initialize game variables
score = 0
lives = 5
enemy_x = random.randint(0, 100)
enemy_y = random.randint(0, 100)

#Function to update game state
def update_game_state(action):
    global score, lives, enemy_x, enemy_y

    if action == "shoot":
        if abs(enemy_x - 50) < 10 and abs(enemy_y - 50) < 10:
            score += 1
            enemy_x = random.randint(0, 100)
            enemy_y = random.randint(0, 100)
        else:
            lives -= 1

    elif action == "move_up":
        enemy_y -= 10

    elif action == "move_down":
        enemy_y += 10

    elif action == "move_left":
        enemy_x -= 10

    elif action == "move_right":
        enemy_x += 10

#Streamlit app
st.title("Shooter Game")

#Game canvas
game_canvas = st.empty()

#Game loop
while lives > 0:
    # Draw game state
    game_canvas.write(f"Score: {score}, Lives: {lives}")
    game_canvas.write(f"Enemy position: ({enemy_x}, {enemy_y})")

    # Get user input
    action = st.selectbox("Action", ["shoot", "move_up", "move_down", "move_left", "move_right"])

    # Update game state
    update_game_state(action)

    # Wait for 1 second
    time.sleep(1)

#Game over
game_canvas.write("Game Over!")
game_canvas.write(f"Final score: {score}") 
