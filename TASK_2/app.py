import streamlit as st

st.set_page_config(
    page_title="Tic-Tac-Toe AI Pro",
    page_icon="🎮",
    layout="centered"
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #060814 0%, #0b1120 50%, #131130 100%);
        color: #f3f4f6;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }

    h1, h2, h3, p, label {
        color: #ffffff !important;
    }

    .main-title {
        text-align: center;
        font-size: 3.2rem !important;
        font-weight: 800;
        background: linear-gradient(45deg, #3b82f6, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }

    .sub-caption {
        text-align: center;
        color: #9ca3af;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        letter-spacing: 1.5px;
    }

    div[data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid #4f46e5;
        padding: 15px;
        border-radius: 14px;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.15);
        backdrop-filter: blur(8px);
    }

    div.stButton > button[key^="cell_"] {
        border-radius: 16px;
        min-height: 100px;
        background: rgba(30, 41, 59, 0.4);
        border: 2px solid #334155;
        color: #ffffff !important;
        font-size: 36px !important;
        font-weight: 700;
        transition: all 0.25s ease-in-out;
    }

    div.stButton > button[key^="cell_"]:hover:not([disabled]) {
        background: #1e293b !important;
        border-color: #6366f1 !important;
        box-shadow: 0 0 12px rgba(99, 102, 241, 0.4);
        transform: scale(1.02);
    }

    div.stButton > button:not([key^="cell_"]) {
        border-radius: 12px;
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        padding: 0.6rem 1.2rem !important;
        transition: all 0.2s ease;
    }

    div.stButton > button:not([key^="cell_"]):hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(168, 85, 247, 0.3);
    }

    .stAlert {
        border-radius: 12px !important;
        background-color: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid #6366f1 !important;
    }

    hr {
        border-color: #1e293b !important;
    }
</style>
""", unsafe_allow_html=True)

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
                score, _ = minimax(board, False, depth + 1, alpha, beta)
                board[i] = None
                
                if score > best_score:
                    best_score = score
                    best_move = i
                    
                alpha = max(alpha, best_score)
                if beta <= alpha: 
                    break
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
                if beta <= alpha: 
                    break
        return best_score, best_move

if "board" not in st.session_state: 
    st.session_state.board = [None] * 9

if "scores" not in st.session_state: 
    st.session_state.scores = {"You": 0, "AI": 0, "Draws": 0}

if "game_over" not in st.session_state: 
    st.session_state.game_over = False

if "message" not in st.session_state: 
    st.session_state.message = "⚡ Your turn! Tap an empty square to place ❌."

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

st.subheader("🏆 Live Scoreboard")
col_score1, col_score2, col_score3 = st.columns(3)
col_score1.metric("👤 You (❌)", st.session_state.scores["You"])
col_score2.metric("🤖 AI (⭕)", st.session_state.scores["AI"])
col_score3.metric("🤝 Draws", st.session_state.scores["Draws"])

st.divider()
st.subheader("🎯 Arena")
st.info(st.session_state.message)

current_board = st.session_state.board

for row in range(3):
    grid_cols = st.columns(3, gap="medium")
    
    for col in range(3):
        index = row * 3 + col
        cell_value = current_board[index]

        if cell_value == "X":
            btn_label = "❌"
        elif cell_value == "O":
            btn_label = "⭕"
        else:
            btn_label = " "

        if grid_cols[col].button(
            btn_label,
            key=f"cell_{index}",
            use_container_width=True,
            disabled=(cell_value is not None or st.session_state.game_over)
        ):
            current_board[index] = "X"
            match_result = check_winner(current_board)

            if match_result is not None:
                finish_game(match_result)
            else:
                _, ai_move = minimax(current_board, is_ai=True)
                if ai_move is not None:
                    current_board[ai_move] = "O"
                    
                match_result = check_winner(current_board)
                if match_result is not None:
                    finish_game(match_result)
                else:
                    st.session_state.message = "⚡ Your turn! Tap an empty square to place ❌."

            st.rerun()

st.divider()
control_col1, control_col2 = st.columns(2)

with control_col1:
    st.button("🔄 Next Match", use_container_width=True, on_click=new_game)
    
with control_col2:
    if st.button("🗑️ Reset All Scores", use_container_width=True):
        st.session_state.scores = {"You": 0, "AI": 0, "Draws": 0}
        new_game()
        st.rerun()

with st.expander("🧠 System Core Intelligence"):
    st.write("""
    - **Minimax Tree Engine**: Simulates every single move permutation up to terminal states.
    - **Alpha-Beta Bounds**: Prunes branches that yield sub-optimal results for high performance.
    - **Heuristic Constraints**: Depth penalties guarantee the quickest path to victory or draw.
    """)

st.caption("Developer - Mukul Bandewar • Developed with Python & Streamlit 🎮")



