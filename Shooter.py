# File: streamlit_chess.py

import streamlit as st
from streamlit.chessboard import chessboard
import chess
import chess.engine

# Initialize session state
if "board" not in st.session_state:
    st.session_state.board = chess.Board()
if "last_move" not in st.session_state:
    st.session_state.last_move = None
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# Title and description
st.title("Chess Game")
st.markdown("Play chess against yourself or an AI!")

# Display the chessboard
last_move = st.session_state.last_move
board = st.session_state.board

# Display the board using `streamlit-chessboard`
selected_move = chessboard(
    board=board.fen(),
    key="chessboard",
    last_move=last_move,
    interactive=not st.session_state.game_over,
)

# Game Over check
if board.is_checkmate():
    st.session_state.game_over = True
    st.success("Checkmate!")
elif board.is_stalemate():
    st.session_state.game_over = True
    st.info("Stalemate!")
elif board.is_insufficient_material():
    st.session_state.game_over = True
    st.info("Draw due to insufficient material.")
elif board.is_seventyfive_moves():
    st.session_state.game_over = True
    st.info("Draw due to 75 moves rule.")

# Make the selected move
if selected_move and not st.session_state.game_over:
    try:
        move = chess.Move.from_uci(selected_move)
        if move in board.legal_moves:
            board.push(move)
            st.session_state.last_move = selected_move
        else:
            st.error("Illegal move!")
    except Exception as e:
        st.error(f"Invalid move format: {e}")

# AI response (optional)
ai_enabled = st.checkbox("Play against AI", value=False)

if ai_enabled and not st.session_state.game_over:
    try:
        # Using a simple Stockfish integration
        with chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish") as engine:
            result = engine.play(board, chess.engine.Limit(time=1.0))
            board.push(result.move)
            st.session_state.last_move = result.move.uci()
    except Exception as e:
        st.warning(f"AI could not make a move: {e}")

# Reset the game
if st.button("Reset Game"):
    st.session_state.board = chess.Board()
    st.session_state.last_move = None
    st.session_state.game_over = False
    st.info("Game reset!")

# Display FEN and PGN
st.text_area("FEN", board.fen(), height=50)
st.text_area("PGN", board.pgn().read(), height=150)
