import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Tic-Tac-Toe AI Pro",
    page_icon="🎮",
    layout="centered"
)

# ---------- PREMIUM NEON CYBERPUNK CSS DESIGN ----------
st.markdown("""
<style>
/* ஆப் பின்னணி - Deep Space Neon Gradient */
.stApp {
    background: linear-gradient(135deg, #060814 0%, #0b1120 50%, #131130 100%);
    color: #f3f4f6;
    font-family: 'Segoe UI', Roboto, sans-serif;
}

/* தலைப்பு மற்றும் உரைகள் */
h1, h2, h3, p, label {
    color: #ffffff !important;
}

/* பிரீமியம் நியான் தலைப்பு */
.main-title {
    text-align: center;
    font-size: 3.5rem !important;
    font-weight: 900;
    background: linear-gradient(45deg, #3b82f6, #a855f7, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 30px rgba(168, 85, 247, 0.4);
    margin-bottom: 5px;
}
.sub-caption {
    text-align: center;
    color: #9ca3af;
    font-size: 1.1rem;
    margin-bottom: 2rem;
    letter-spacing: 2px;
}

/* ஸ்கோர்போர்டு கார்டுகள் டிசைன் */
div[data-testid="stMetric"] {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid #4f46e5;
    padding: 15px;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(79, 70, 229, 0.15);
    backdrop-filter: blur(10px);
    transition: transform 0.3s ease;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    border-color: #818cf8;
    box-shadow: 0 4px 25px rgba(129, 140, 248, 0.3);
}

/* 🟢 பொதுவான கேம் போர்டு கட்டங்கள் (Default Empty Cells) */
div.stButton > button[key^="cell_"] {
    border-radius: 20px;
    min-height: 100px;
    background: rgba(30, 41, 59, 0.4);
    border: 2px solid #334155;
    color: #ffffff !important;
    font-size: 38px !important;
    font-weight: 800;
    box-shadow: inset 0 0 12px rgba(255,255,255,0.05);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* காலி கட்டங்கள் மீது மவுஸ் வைக்கும் போது */
div.stButton > button[key^="cell_"]:hover:not([disabled]) {
    background: #1e293b !important;
    border-color: #6366f1 !important;
    box-shadow: 0 0 15px rgba(99, 102, 241, 0.4);
    transform: scale(1.05);
}

/* ❌ X விழுந்த கட்டத்திற்கான பிரத்யேக Neon Pink ஸ்டைல் */
div.stButton > button[key^="cell_"]:disabled p:contains("❌") {
    font-size: 45px !important;
    filter: drop-shadow(0 0 12px #f43f5e) drop-shadow(0 0 25px #f43f5e);
    animation: popIn 0.3s ease-out;
}
div.stButton > button[key^="cell_"]:has(p:contains("❌")) {
    background: rgba(244, 63, 94, 0.1) !important;
    border-color: #f43f5e !important;
    box-shadow: 0 0 20px rgba(244, 63, 94, 0.25) !important;
}

/* ⭕ O விழுந்த கட்டத்திற்கான பிரத்யேக Neon Cyan ஸ்டைல் */
div.stButton > button[key^="cell_"]:disabled p:contains("⭕") {
    font-size: 45px !important;
    filter: drop-shadow(0 0 12px #06b6d4) drop-shadow(0 0 25px #06b6d4);
    animation: popIn 0.3s ease-out;
}
div.stButton > button[key^="cell_"]:has(p:contains("⭕")) {
    background: rgba(6, 182, 212, 0.1) !important;
    border-color: #06b6d4 !important;
    box-shadow: 0 0 20px rgba(6, 182, 212, 0.25) !important;
}

/* தோன்றும் போது வரும் அனிமேஷன் */
@keyframes popIn {
    0% { transform: scale(0.5); opacity: 0; }
    100% { transform: scale(1); opacity: 1; }
}

/* கண்ட்ரோல் பட்டன்கள் (New Game & Reset) */
div.stButton > button:not([key^="cell_"]) {
    border-radius: 14px;
    background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%) !important;
    color: white !important;
    border: none !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    padding: 0.7rem 1rem !important;
    box-shadow: 0 4px 15px rgba(168, 85, 247, 0.2);
    transition: all 0.3s ease;
}
div.stButton > button:not([key^="cell_"]):hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(168, 85, 247, 0.4);
}

/* இன்ஃபோ பாக்ஸ் */
.stAlert {
    border-radius: 14px !important;
    background-color: rgba(15, 23, 42, 0.8) !important;
    border: 1px solid #6366f1 !important;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.1);
}
hr {
    border-color: #1e293b !important;
}
</style>
""", unsafe_allow_html=True)

# அழகிய ஹெடர் பகுதி
st.markdown('<h1 class="main-title">🎮 Tic-Tac-Toe AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-caption">⚡ ADVANCED MINIMAX • ALPHA-BETA PRUNING</p>', unsafe_allow_html=True)

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
    if result == "O": return 10 - depth, None
    if result == "X": return depth - 10, None
    if result == "Draw": return 0, None

    best_move = None
    if is_ai:
        best_score = -100
        for i in range(9):
            if board[i] is None:
                board[i] = "O"
                score, _ = minimax(board, False, depth + 1, alpha, beta)
                board[i] = None
                if score > best_score:
                    best_score = score
                    best_move = i
                alpha = max(alpha, best_score)
                if beta <= alpha: break
        return best_score, best_move
    else:
        best_score = 100
        for i in range(9):
            if board[i] is None:
                board[i] = "X"
                score, _ = minimax(board, True, depth + 1, alpha, beta)
                board[i] = None
                if score < best_score:
                    best_score = score
                    best_move = i
                beta = min(beta, best_score)
                if beta <= alpha: break
        return best_score, best_move

# ---------- GAME STATE ----------
if "board" not in st.session_state: st.session_state.board = [None] * 9
if "scores" not in st.session_state: st.session_state.scores = {"You": 0, "AI": 0, "Draws": 0}
if "game_over" not in st.session_state: st.session_state.game_over = False
if "message" not in st.session_state: st.session_state.message = "⚡ Your turn! Tap an empty square to place ❌."

def new_game():
    st.session_state.board = [None] * 9
    st.session_state.game_over = False
    st.session_state.message = "⚡ Your turn! Tap an empty square to place ❌."

def finish_game(result):
    st.session_state.game_over = True
    if result == "X":
        st.session_state.scores["You"] += 1
        st.session_state.message = "🎉 Victory! You defeated the AI!"
    elif result == "O":
        st.session_state.scores["AI"] += 1
        st.session_state.message = "🤖 AI Wins! Better luck next time!"
    else:
        st.session_state.scores["Draws"] += 1
        st.session_state.message = "🤝 Spectacular defense! It's a Draw!"

# ---------- SCOREBOARD ----------
st.subheader("🏆 Live Scoreboard")
c1, c2, c3 = st.columns(3)
c1.metric("👤 You (❌)", st.session_state.scores["You"])
c2.metric("🤖 AI (⭕)", st.session_state.scores["AI"])
c3.metric("🤝 Draws", st.session_state.scores["Draws"])

st.divider()
st.subheader("🎯 Arena")
st.info(st.session_state.messages if "messages" in st.session_state else st.session_state.message)

# ---------- BOARD ARRANGE ----------
board = st.session_state.board

for row in range(3):
    cols = st.columns(3, gap="medium")
    for col in range(3):
        index = row * 3 + col
        value = board[index]

        label = "❌" if value == "X" else ("⭕" if value == "O" else " ")

        if cols[col].button(
            label,
            key=f"cell_{index}",
            use_container_width=True,
            disabled=(value is not None or st.session_state.game_over)
        ):
            # Player Move
            board[index] = "X"
            result = check_winner(board)

            if result is not None:
                finish_game(result)
            else:
                # AI Move
                _, move = minimax(board, True)
                if move is not None:
                    board[move] = "O"
                result = check_winner(board)
                if result is not None:
                    finish_game(result)
                else:
                    st.session_state.message = "⚡ Your turn! Tap an empty square to place ❌."

            st.rerun()

# ---------- CONTROLS ----------
st.divider()
ctrl1, ctrl2 = st.columns(2)
with ctrl1:
    st.button("🔄 Next Match", use_container_width=True, on_click=new_game)
with ctrl2:
    if st.button("🗑️ Reset All Scores", use_container_width=True):
        st.session_state.scores = {"You": 0, "AI": 0, "Draws": 0}
        new_game()
        st.rerun()

# ---------- INFO ----------
with st.expander("🧠 System Core Intelligence"):
    st.write("""
    - **Minimax Tree Engine**: Simulates every single move permutation up to terminal states.
    - **Alpha-Beta Bounds**: Prunes branches that yield sub-optimal results for high performance.
    - **Heuristic Constraints**: Depth penalties guarantee the quickest path to victory or draw.
    """)

st.caption("Cyber-Grid Interface v2.0 • Python & Streamlit 🎮")



