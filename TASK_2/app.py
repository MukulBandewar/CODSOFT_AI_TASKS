
import streamlit as st

st.set_page_config(
    page_title="Tic-Tac-Toe AI",
    page_icon="🎮",
    layout="centered"
)

# ---------- CSS DESIGN ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #080d20, #17133b);
    color: white;
}
h1, h2, h3, p, label {
    color: white !important;
}
div[data-testid="stMetric"] {
    background: #151f40;
    border: 1px solid #5145a8;
    padding: 12px;
    border-radius: 14px;
}
div.stButton > button {
    border-radius: 12px;
    min-height: 65px;
    background: #172447;
    border: 1px solid #536dfe;
    color: white;
    font-size: 25px;
    font-weight: bold;
}
div.stButton > button:hover {
    background: #5145a8;
    border-color: #a78bfa;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("🎮 Tic-Tac-Toe AI")
st.caption("⚡ MINIMAX ALGORITHM • ALPHA-BETA PRUNING")
st.write("Challenge the AI. Can you force a draw?")

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


# ---------- MINIMAX AI ----------
def minimax(board, is_ai, depth=0, alpha=-100, beta=100):
    result = check_winner(board)

    if result == "O":
        return 10 - depth, None
    if result == "X":
        return depth - 10, None
    if result == "Draw":
        return 0, None

    best_move = None

    if is_ai:
        best_score = -100

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

                if alpha >= beta:
                    break

        return best_score, best_move

    best_score = 100

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

            if alpha >= beta:
                break

    return best_score, best_move


# ---------- GAME STATE ----------
if "board" not in st.session_state:
    st.session_state.board = [None] * 9

if "scores" not in st.session_state:
    st.session_state.scores = {
        "You": 0, "AI": 0, "Draws": 0
    }

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "message" not in st.session_state:
    st.session_state.message = "Your turn! You play X."


def new_game():
    st.session_state.board = [None] * 9
    st.session_state.game_over = False
    st.session_state.message = "Your turn! You play X."


def finish_game(result):
    st.session_state.game_over = True

    if result == "X":
        st.session_state.scores["You"] += 1
        st.session_state.message = "🎉 You won! Great job!"
    elif result == "O":
        st.session_state.scores["AI"] += 1
        st.session_state.message = "🤖 AI wins! Try again!"
    else:
        st.session_state.scores["Draws"] += 1
        st.session_state.message = "🤝 It's a draw!"


# ---------- SCOREBOARD ----------
st.subheader("🏆 Scoreboard")

c1, c2, c3 = st.columns(3)
c1.metric("👤 You (X)", st.session_state.scores["You"])
c2.metric("🤖 AI (O)", st.session_state.scores["AI"])
c3.metric("🤝 Draws", st.session_state.scores["Draws"])

st.divider()
st.subheader("🎯 Game Board")
st.info(st.session_state.message)

# ---------- BOARD ----------
board = st.session_state.board

for row in range(3):
    cols = st.columns(3, gap="small")

    for col in range(3):
        index = row * 3 + col
        value = board[index]

        if value == "X":
            label = "❌ X"
        elif value == "O":
            label = "⭕ O"
        else:
            label = "＋"

        if cols[col].button(
            label,
            key=f"cell_{index}",
            use_container_width=True,
            disabled=(
                value is not None or
                st.session_state.game_over
            )
        ):
            # Human move
            board[index] = "X"
            result = check_winner(board)

            if result is not None:
                finish_game(result)
            else:
                # AI move
                _, move = minimax(board, True)

                if move is not None:
                    board[move] = "O"

                result = check_winner(board)

                if result is not None:
                    finish_game(result)
                else:
                    st.session_state.message = (
                        "Your turn! Choose an empty square."
                    )

            st.rerun()


# ---------- CONTROLS ----------
st.divider()

c1, c2 = st.columns(2)

with c1:
    st.button(
        "🔄 New Game",
        use_container_width=True,
        on_click=new_game
    )

with c2:
    if st.button("🗑️ Reset Scores", use_container_width=True):
        st.session_state.scores = {
            "You": 0, "AI": 0, "Draws": 0
        }
        new_game()
        st.rerun()


# ---------- ALGORITHM INFO ----------
with st.expander("🧠 How does the AI work?"):
    st.write("""
    - Minimax searches possible future moves.
    - The AI plays as O and the human plays as X.
    - Alpha-Beta Pruning skips unnecessary branches.
    - The AI chooses optimal moves and cannot lose
      when it plays correctly.
    """)

st.caption("Built with Python and Streamlit 🎮")



