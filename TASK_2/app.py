
import streamlit as st

st.set_page_config(
    page_title="Tic-Tac-Toe AI",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- GAMING UI ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

.stApp {
    background:
        radial-gradient(circle at 10% 10%, #25144d 0%, transparent 35%),
        radial-gradient(circle at 90% 20%, #102d54 0%, transparent 30%),
        linear-gradient(135deg, #070b19, #0d1630);
    color: #f0f5ff;
    font-family: Inter, sans-serif;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
}

.hero {
    padding: 25px;
    border: 1px solid #334b83;
    border-radius: 22px;
    background: linear-gradient(110deg, #111d40, #211344);
    margin-bottom: 24px;
}

.hero h1 {
    font-size: clamp(30px, 4vw, 48px);
    font-weight: 800;
    background: linear-gradient(90deg, #5ee7ff, #a78bfa, #f472d0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p { color: #a9c3f7; }

div[data-testid="stMetric"] {
    background: #111d3b;
    border: 1px solid #344c83;
    border-radius: 16px;
    padding: 15px;
}

div[data-testid="stMetricLabel"] {
    color: #b6c8f5 !important;
}

div[data-testid="stMetricValue"] {
    color: white !important;
    font-weight: 800;
}

div.stButton > button {
    min-height: 76px;
    width: 100%;
    border-radius: 15px;
    border: 1px solid #397cf5;
    background: linear-gradient(145deg, #152448, #111a35);
    color: #e8f3ff;
    font-size: 1.65rem;
    font-weight: 800;
    transition: 0.2s;
}

div.stButton > button:hover {
    background: linear-gradient(135deg, #244a91, #44318b);
    border-color: #67e8f9;
    color: white;
}

div.stButton > button:disabled {
    opacity: 1;
    background: #111a35;
    color: #9cb7ed;
    border-color: #263d6d;
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #4f46e5, #9333ea);
    border: none;
    color: white;
}

.panel {
    background: rgba(13, 24, 53, 0.9);
    border: 1px solid #293e6d;
    border-radius: 20px;
    padding: 20px;
}

div[data-testid="stAlert"] {
    border-radius: 13px;
}

div[data-testid="stExpander"] {
    background: #101a35;
    border: 1px solid #293e6d;
    border-radius: 14px;
}

hr { border-color: #293e6d; }

.muted {
    color: #9bb0dd;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("""
<div class="hero">
    <h1>🎮 Tic-Tac-Toe AI</h1>
    <h3>Think Ahead. Make Your Move.</h3>
    <p>🤖 Minimax Algorithm &nbsp; • &nbsp; Alpha-Beta Pruning</p>
</div>
""", unsafe_allow_html=True)

# ---------- WIN CONDITIONS ----------
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


# ---------- SESSION STATE ----------
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

if "last_result" not in st.session_state:
    st.session_state.last_result = None


def reset_game():
    st.session_state.board = [None] * 9
    st.session_state.game_over = False
    st.session_state.message = "Your turn! You play X."
    st.session_state.last_result = None


def finish_game(result):
    st.session_state.game_over = True
    st.session_state.last_result = result

    if result == "X":
        st.session_state.scores["You"] += 1
        st.session_state.message = "🎉 You won! Excellent moves!"

    elif result == "O":
        st.session_state.scores["AI"] += 1
        st.session_state.message = "🤖 AI wins! Try again!"

    else:
        st.session_state.scores["Draws"] += 1
        st.session_state.message = "🤝 It's a draw! Well played!"


# ---------- SCOREBOARD ----------
st.markdown("### 🏆 Match Scoreboard")

s1, s2, s3 = st.columns(3)

s1.metric("👤 YOU · X", st.session_state.scores["You"])
s2.metric("🤖 AI · O", st.session_state.scores["AI"])
s3.metric("🤝 DRAWS", st.session_state.scores["Draws"])

st.write("")

# ---------- MAIN LAYOUT ----------
left, center, right = st.columns([1, 2.1, 1], gap="large")

# LEFT PANEL
with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.markdown("### 🎯 Your Mission")
    st.write("Get three X symbols in a row to win.")

    st.divider()

    st.markdown("### 🔷 Your Symbol")
    st.markdown("## ❌ X")
    st.markdown(
        '<p class="muted">You play first.</p>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### 💡 Pro Tip")
    st.write(
        "Control the center, use corners, "
        "and block the AI's winning moves."
    )

    st.markdown("</div>", unsafe_allow_html=True)

# CENTER PANEL: GAME BOARD
with center:
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.markdown("### ⚔️ Human vs AI")

    if st.session_state.game_over:
        if st.session_state.last_result == "X":
            st.success(st.session_state.message)
        elif st.session_state.last_result == "O":
            st.error(st.session_state.message)
        else:
            st.info(st.session_state.message)
    else:
        st.info("🟦 " + st.session_state.message)

    board = st.session_state.board

    for row in range(3):
        cols = st.columns(3, gap="small")

        for col in range(3):
            index = row * 3 + col
            value = board[index]

            if value == "X":
                label = "❌"
            elif value == "O":
                label = "⭕"
            else:
                label = "＋"

            if cols[col].button(
                label,
                key=f"cell_{index}",
                use_container_width=True,
                disabled=(
                    value is not None
                    or st.session_state.game_over
                )
            ):
                # Human move
                board[index] = "X"

                result = check_winner(board)

                if result:
                    finish_game(result)

                else:
                    # AI move
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

    st.markdown(
        '<p class="muted" style="text-align:center">'
        '❌ You (X) &nbsp; • &nbsp; ⭕ AI (O)'
        '</p>',
        unsafe_allow_html=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

# RIGHT PANEL: CONTROLS
with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.markdown("### 🕹️ Game Controls")
    st.caption("Ready for another round?")

    if st.button(
        "🔄 New Game",
        type="primary",
        use_container_width=True
    ):
        reset_game()
        st.rerun()

    if st.button(
        "🗑️ Reset Scores",
        use_container_width=True
    ):
        st.session_state.scores = {
            "You": 0, "AI": 0, "Draws": 0
        }
        reset_game()
        st.rerun()

    st.divider()

    st.markdown("### 🧠 AI Status")
    st.write("**Algorithm:** Minimax")
    st.write("**Optimization:** Alpha-Beta")
    st.write("**Difficulty:** Unbeatable")

    st.markdown(
        '<p class="muted">AI evaluates possible moves '
        'and selects the optimal move.</p>',
        unsafe_allow_html=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- HOW IT WORKS ----------
st.write("")

with st.expander("🧠 How does this AI work?"):
    st.markdown("""
    **1. Search:** The AI checks available moves.

    **2. Simulate:** It explores possible future moves
    for both players.

    **3. Minimax:** Winning positions get positive scores,
    losing positions get negative scores, and draws score zero.

    **4. Alpha-Beta Pruning:** Unnecessary search branches
    are skipped to improve efficiency.

    **Result:** The AI plays optimally. With correct play,
    you can force a draw, but you cannot beat the AI.
    """)

st.markdown("---")

st.markdown(
    '<p class="muted" style="text-align:center">'
    'Built with Python + Streamlit | '
    'Powered by Minimax with Alpha-Beta Pruning 🎮'
    '</p>',
    unsafe_allow_html=True
)



