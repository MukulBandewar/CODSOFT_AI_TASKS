
import streamlit as st

st.set_page_config(
    page_title="Tic-Tac-Toe AI Pro",
    page_icon="🎮",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#060814,#0b1120,#131130);
    color: #f3f4f6;
    font-family: 'Segoe UI',system-ui,sans-serif;
}

h1,h2,h3,p,label {
    color: #ffffff !important;
}

.main-title {
    text-align: center;
    font-size: 3.2rem !important;
    font-weight: 800;
    background: linear-gradient(45deg,#3b82f6,#a855f7,#ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 5px;
    line-height: 1.2;
}

.sub-caption {
    text-align: center;
    color: #9ca3af;
    font-size: 1.1rem;
    margin-bottom: 2rem;
    letter-spacing: 1.5px;
}

.block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

div[data-testid="stMetric"] {
    background: rgba(15,23,42,.7);
    border: 1px solid #4f46e5;
    padding: 15px;
    border-radius: 14px;
    box-shadow: 0 4px 15px rgba(79,70,229,.15);
}

div[data-testid="stMetricLabel"],
div[data-testid="stMetricValue"] {
    color: white !important;
}

div[data-testid="stHorizontalBlock"] {
    gap: 10px;
}

/* Buttons */
.stButton > button {
    width: 100%;
    min-height: 46px;
    border-radius: 12px;
    background: linear-gradient(90deg,#6366f1,#a855f7) !important;
    color: white !important;
    border: 1px solid transparent !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    padding: .6rem .5rem !important;
    transition: all .2s ease;
}

.stButton > button:hover:not(:disabled) {
    border-color: #a5b4fc !important;
    box-shadow: 0 4px 12px rgba(168,85,247,.3);
}

/* Game cells: Streamlit's button wrapper */
div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"] .stButton > button {
    min-height: clamp(65px, 15vw, 110px);
    height: clamp(65px, 15vw, 110px);
    border-radius: 16px;
    background: rgba(30,41,59,.75) !important;
    border: 2px solid #334155 !important;
    color: white !important;
    font-size: clamp(25px, 5vw, 40px) !important;
    font-weight: 700 !important;
    padding: 0 !important;
}

div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"] .stButton > button:hover:not(:disabled) {
    background: #1e293b !important;
    border-color: #818cf8 !important;
    box-shadow: 0 0 12px rgba(99,102,241,.4);
}

.stAlert {
    border-radius: 12px !important;
    background: rgba(15,23,42,.8) !important;
    border: 1px solid #6366f1 !important;
}

hr {
    border-color: #1e293b !important;
}

[data-testid="stExpander"] {
    border-color: #334155;
    border-radius: 12px;
}

/* Mobile responsive */
@media screen and (max-width: 768px) {
    .block-container {
        padding: 1rem .8rem 2rem .8rem !important;
    }

    .main-title {
        font-size: 2.25rem !important;
    }

    .sub-caption {
        font-size: .85rem;
        letter-spacing: .7px;
        margin-bottom: 1.3rem;
    }

    div[data-testid="stMetric"] {
        padding: 9px 4px;
        border-radius: 10px;
    }

    div[data-testid="stMetricLabel"] {
        font-size: .72rem !important;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.35rem !important;
    }

    div[data-testid="stHorizontalBlock"] {
        gap: 6px;
    }

    div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"] .stButton > button {
        min-height: clamp(65px, 24vw, 95px);
        height: clamp(65px, 24vw, 95px);
        font-size: clamp(24px, 8vw, 36px) !important;
        border-radius: 12px;
    }

    h2 {
        font-size: 1.25rem !important;
    }

    .stButton > button {
        font-size: 13px !important;
        min-height: 44px;
    }
}

@media screen and (max-width: 380px) {
    .block-container {
        padding-left: .5rem !important;
        padding-right: .5rem !important;
    }

    .main-title {
        font-size: 1.8rem !important;
    }

    .sub-caption {
        font-size: .7rem;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.1rem !important;
    }

    div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"] .stButton > button {
        min-height: 62px;
        height: 62px;
        font-size: 25px !important;
    }
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<h1 class="main-title">🎮 Tic-Tac-Toe AI</h1>',
    unsafe_allow_html=True
)
st.markdown(
    '<p class="sub-caption">⚡ ADVANCED MINIMAX • ALPHA-BETA PRUNING</p>',
    unsafe_allow_html=True
)

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

            if beta <= alpha:
                break

    return best_score, best_move


if "board" not in st.session_state:
    st.session_state.board = [None] * 9

if "scores" not in st.session_state:
    st.session_state.scores = {
        "You": 0, "AI": 0, "Draws": 0
    }

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "message" not in st.session_state:
    st.session_state.message = (
        "⚡ Your turn! Tap an empty square to place ❌."
    )


def new_game():
    st.session_state.board = [None] * 9
    st.session_state.game_over = False
    st.session_state.message = (
        "⚡ Your turn! Tap an empty square to place ❌."
    )


def finish_game(result):
    st.session_state.game_over = True

    if result == "X":
        st.session_state.scores["You"] += 1
        st.session_state.message = (
            "🎉 Victory! You defeated the AI!"
        )
    elif result == "O":
        st.session_state.scores["AI"] += 1
        st.session_state.message = (
            "🤖 AI Wins! Better luck next time!"
        )
    else:
        st.session_state.scores["Draws"] += 1
        st.session_state.message = (
            "🤝 Spectacular defense! It's a Draw!"
        )


st.subheader("🏆 Live Scoreboard")

col1, col2, col3 = st.columns(3)

col1.metric("👤 You (❌)", st.session_state.scores["You"])
col2.metric("🤖 AI (⭕)", st.session_state.scores["AI"])
col3.metric("🤝 Draws", st.session_state.scores["Draws"])

st.divider()
st.subheader("🎯 Arena")
st.info(st.session_state.message)

for row in range(3):
    grid_cols = st.columns(3, gap="small")

    for col in range(3):
        index = row * 3 + col
        cell_value = st.session_state.board[index]

        if cell_value == "X":
            label = "❌"
        elif cell_value == "O":
            label = "⭕"
        else:
            label = " "

        if grid_cols[col].button(
            label,
            key=f"cell_{index}",
            use_container_width=True,
            disabled=(
                cell_value is not None
                or st.session_state.game_over
            )
        ):
            st.session_state.board[index] = "X"
            result = check_winner(st.session_state.board)

            if result is not None:
                finish_game(result)
            else:
                _, ai_move = minimax(
                    st.session_state.board, is_ai=True
                )

                if ai_move is not None:
                    st.session_state.board[ai_move] = "O"

                result = check_winner(st.session_state.board)

                if result is not None:
                    finish_game(result)
                else:
                    st.session_state.message = (
                        "⚡ Your turn! Tap an empty square to place ❌."
                    )

            st.rerun()


st.divider()

control1, control2 = st.columns(2)

with control1:
    st.button(
        "🔄 Next Match",
        use_container_width=True,
        on_click=new_game
    )

with control2:
    if st.button(
        "🗑️ Reset All Scores",
        use_container_width=True
    ):
        st.session_state.scores = {
            "You": 0, "AI": 0, "Draws": 0
        }
        new_game()
        st.rerun()


with st.expander("🧠 System Core Intelligence"):
    st.markdown("""
    - **Minimax Tree Engine:** Evaluates possible game outcomes.
    - **Alpha-Beta Pruning:** Skips branches that cannot improve a decision.
    - **Depth-Based Scoring:** Prefers faster wins and delays losses.
    - **Unbeatable Strategy:** Plays optimally; with perfect play, the game ends in a win or draw.
    """)

st.caption(
    "Developer - Mukul Bandewar • Developed with Python & Streamlit 🎮"
)


