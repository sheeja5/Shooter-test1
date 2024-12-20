import streamlit as st
import random

# Game settings
st.set_page_config(page_title="Shooting Game", layout="wide")
st.title("🎯 Shooting Game")

# Initialize session state
if "target_position" not in st.session_state:
    st.session_state.target_position = [random.randint(50, 450), random.randint(50, 450)]
if "score" not in st.session_state:
    st.session_state.score = 0
if "ammo" not in st.session_state:
    st.session_state.ammo = 10

# Display the game area
col1, col2 = st.columns([1, 3])
with col1:
    st.write("### Game Stats")
    st.write(f"**Score:** {st.session_state.score}")
    st.write(f"**Ammo Left:** {st.session_state.ammo}")
    if st.session_state.ammo == 0:
        st.warning("Out of ammo! Reload to continue.")
        if st.button("Reload"):
            st.session_state.ammo = 10

with col2:
    st.write("### Game Area")
    target_x, target_y = st.session_state.target_position
    canvas = st.empty()

    # Display target
    target_html = f"""
    <div style='position: absolute; top: {target_y}px; left: {target_x}px; 
    width: 50px; height: 50px; background-color: red; border-radius: 50%;'></div>
    """
    canvas.markdown(
        f"<div style='position: relative; width: 500px; height: 500px; background-color: lightblue;'>{target_html}</div>",
        unsafe_allow_html=True,
    )

# User input
st.write("### Shoot Target")
x = st.number_input("Enter x-coordinate (0-500):", min_value=0, max_value=500, value=0)
y = st.number_input("Enter y-coordinate (0-500):", min_value=0, max_value=500, value=0)
if st.button("Shoot"):
    if st.session_state.ammo > 0:
        st.session_state.ammo -= 1
        if abs(x - target_x) <= 25 and abs(y - target_y) <= 25:
            st.success("Hit! 🎯")
            st.session_state.score += 1
            st.session_state.target_position = [random.randint(50, 450), random.randint(50, 450)]
        else:
            st.error("Missed!")
    else:
        st.warning("No ammo left! Reload to shoot again.")
