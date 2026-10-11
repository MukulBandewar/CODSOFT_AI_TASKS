
import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Tic-Tac-Toe AI",
    page_icon="🎮",
    layout="centered"
)

# ---------------- PROFESSIONAL UI ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0b1020, #171936);
    color: white;
}
h1, h2, h3, p, label {
    color: white !important;
}
div.stButton > button {
    border-radius: 12px;
    font-weight: bold;
    min-height: 55px;
    border: 1px solid #5145a8;
    background: #202746;
    color: white;
    transition: 0.2s;
}
div.stButton > button:hover {
    background: #5145a8;
    border-color: #a78bfa;
}
div.stButton > button:disabled {
    opacity: 1;
    color: white;
    background: #292e48;
}
div[data-testid="stMetric"] {
    background: #171f37;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #303958;
}
</style>
""", unsafe_allow_html=True)

st.title("🎮 Tic-Tac-Toe AI")
st.caption("MINIMAX ALGORITHM  •  ALPHA-BETA PRUNING")
st.write("Challenge the AI. Can you force a draw?")

# ---------------- GAME CONFIGURATION ----------------
WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]


def check_winner(board):
    for a, b, c in WIN_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]

    if all(cell is not None for cell in board):
        return "Draw"

    return None


# ---------------- MINIMAX AI ----------------
def minimax(board, is_ai, depth=0, alpha=-1000, beta=1000):
    result = check_winner(board)

    if result == "O":
        return 10 - depth, None

    if result == "X":
        return depth - 10, None

    if result == "Draw":
        return 0, None

    best_move = None

    if is_ai:
        best_score = -1000

        for i in range(9):
            if board[i] is None:
                board[i] = "O"

                score, _ = minimax(
                    board, False, depth + 1, alpha, beta
                )

                board[i] = None

                if score > best_score:
                    best_score = score
                    best_move = i

                alpha = max(alpha, best_score)

                if beta <= alpha:
                    break

        return best_score, best_move

    else:
        best_score = 1000

        for i in range(9):
            if board[i] is None:
                board[i] = "X"

                score, _ = minimax(
                    board, True, depth + 1, alpha, beta
                )

                board[i] = None

                if score < best_score:
                    best_score = score
                    best_move = i

                beta = min(beta, best_score)

                if beta <= alpha:
                    break

        return best_score, best_move


# ---------------- SESSION STATE ----------------
if "board" not in st.session_state:
    st.session_state.board = [None] * 9

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "scores" not in st.session_state:
    st.session_state.scores = {
        "You": 0, "AI": 0, "Draws": 0
    }

if "message" not in st.session_state:
    st.session_state.message = "Your turn! You play X."


def reset_game():
    st.session_state.board = [None] * 9
    st.session_state.game_over = False
    st.session_state.message = "Your turn! You play X."


def finish_game(result):
    st.session_state.game_over = True

    if result == "X":
        st.session_state.scores["You"] += 1
        st.session_state.message = "🎉 Congratulations! You won!"
    elif result == "O":
        st.session_state.scores["AI"] += 1
        st.session_state.message = "🤖 AI wins! Try again."
    else:
        st.session_state.scores["Draws"] += 1
        st.session_state.message = "🤝 It's a draw! Well played."


# ---------------- SCOREBOARD ----------------
st.markdown("### 🏆 Scoreboard")

c1, c2, c3 = st.columns(3)

c1.metric("👤 You (X)", st.session_state.scores["You"])
c2.metric("🤖 AI (O)", st.session_state.scores["AI"])
c3.metric("🤝 Draws", st.session_state.scores["Draws"])

st.divider()

# ---------------- GAME BOARD ----------------
st.markdown("### 🎯 Game Board")

st.info(st.session_state.message)

board = st.session_state.board

for row in range(3):
    cols = st.columns(3, gap="small")

    for col in range(3):
        index = row * 3 + col
        value = board[index]

        label = value if value else "·"

        if value == "X":
            label = "❌ X"
        elif value == "O":
            label = "⭕ O"

        if cols[col].button(
            label,
            key=f"cell_{index}",
            use_container_width=True,
            disabled=value is not None or st.session_state.game_over
        ):
            # Human move
            board[index] = "X"

            result = check_winner(board)

            if result:
                finish_game(result)

            else:
                # AI calculates the best move
                _, ai_move = minimax(board, True)

                if ai_move is not None:
                    board[ai_move] = "O"

                result = check_winner(board)

                if result:
                    finish_game(result)
                else:
                    st.session_state.message = (
                        "Your turn! Choose an empty square."
                    )

            st.rerun()

# ---------------- CONTROLS ----------------
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.button(
        "🔄 New Game",
        use_container_width=True,
        on_click=reset_game
    )

with col2:
    if st.button("🗑️ Reset Scores", use_container_width=True):
        st.session_state.scores = {
            "You": 0, "AI": 0, "Draws": 0
        }
        reset_game()
        st.rerun()

# ---------------- PROJECT INFORMATION ----------------
with st.expander("🧠 How does this AI work?"):
    st.markdown("""
    **Algorithm:** Minimax with Alpha-Beta Pruning

    - **Step 1:** The AI checks all possible moves.
    - **Step 2:** It simulates future human and AI moves.
    - **Step 3:** Winning moves receive positive scores.
    - **Step 4:** Losing moves receive negative scores.
    - **Step 5:** Alpha-Beta Pruning skips unnecessary branches.

    **Result:** The AI plays optimally. You can force a draw,
    but you cannot beat it if it makes the correct moves.

    **Technologies:** Python and Streamlit.
    """)

