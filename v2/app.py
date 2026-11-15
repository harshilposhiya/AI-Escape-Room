
"""
AI ESCAPE ROOM - VERSION 2
Python validates actions and owns structured game state.
Gemini narration is optional and never controls game logic.

Run:
py -m streamlit run v2/app.py --server.port 8501
"""

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from google import genai

from v2.game_engine import new_state, process_action, state_summary


# ==================================================
# 1. CONFIGURATION
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(
    dotenv_path=PROJECT_ROOT / ".env",
    override=True
)

st.set_page_config(
    page_title="AI Escape Room - Version 2",
    page_icon="🗝️",
    layout="wide"
)

API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
).strip()


# ==================================================
# 2. OPTIONAL GEMINI NARRATION
# ==================================================

def optional_narration(validated_text, use_gemini=False):

    # Python response is the default.
    if not use_gemini:
        return validated_text

    if not API_KEY:
        return validated_text

    try:

        client = genai.Client(
            api_key=API_KEY,
            http_options={"timeout": 8000}
        )

        response = client.models.generate_content(
            model=MODEL,
            contents=(
                "Rewrite this validated escape room event "
                "in one or two atmospheric sentences. "
                "Do not add facts, objects, clues, codes, "
                "or change the outcome:\n\n"
                + validated_text
            )
        )

        if response.text:
            return response.text.strip()

        return validated_text

    except Exception as error:

        print(
            "Gemini narration unavailable:",
            type(error).__name__,
            str(error)
        )

        # Never block the game if Gemini fails.
        return validated_text


# ==================================================
# 3. SESSION STATE
# ==================================================

if "game_state" not in st.session_state:
    st.session_state.game_state = new_state()

if "messages_v2" not in st.session_state:

    st.session_state.messages_v2 = [
        {
            "role": "assistant",
            "content": (
                "🌙 You wake inside the Last Library.\n\n"
                "Five things stand out: a desk, bookshelf, "
                "painting, locked drawer and keypad-secured exit.\n\n"
                "Discover the drawer code, collect the key, "
                "find the year in the painting, then unlock "
                "the exit.\n\n"
                "**What will you examine?**"
            )
        }
    ]


# ==================================================
# 4. HEADER
# ==================================================

st.title("🗝️ The Last Library")

st.caption(
    "AI Escape Room · Version 2 · "
    "Python-validated gameplay"
)

st.divider()


# ==================================================
# 5. MAIN LAYOUT
# ==================================================

left, right = st.columns(
    [2, 1],
    gap="large"
)


# ==================================================
# 6. GAME STATE PANEL
# ==================================================

with right:

    st.subheader("🎮 Game state")

    state = st.session_state.game_state

    st.write("**Inventory**")

    if state["inventory"]:

        for item in state["inventory"]:
            st.write(f"🔑 {item.title()}")

    else:

        st.caption("Empty")

    st.divider()

    st.write("**Puzzle progress**")

    st.write(
        f"{'✅' if state['bookshelf_examined'] else '⬜'} "
        "Bookshelf clue discovered"
    )

    st.write(
        f"{'✅' if state['drawer_open'] else '⬜'} "
        "Drawer opened"
    )

    st.write(
        f"{'✅' if state['key_collected'] else '⬜'} "
        "Brass key collected"
    )

    st.write(
        f"{'✅' if state['painting_examined'] else '⬜'} "
        "Painting clue discovered"
    )

    st.write(
        f"{'🏆' if state['escaped'] else '⬜'} "
        "Escaped"
    )

    st.metric(
        "Code attempts",
        state["attempts"]
    )

    with st.expander("Structured state (debug view)"):

        st.json(state_summary(state))

    st.divider()

    if st.button(
        "🔄 Restart Version 2",
        use_container_width=True
    ):

        st.session_state.game_state = new_state()

        st.session_state.messages_v2 = [
            {
                "role": "assistant",
                "content": (
                    "You wake inside the Last Library. "
                    "Examine the bookshelf, desk and "
                    "painting to find clues."
                )
            }
        ]

        st.rerun()


# ==================================================
# 7. GAME CONVERSATION
# ==================================================

with left:

    st.subheader("💬 Game conversation")

    with st.expander("📖 Instructions"):

        st.write(
            "Use natural language to investigate the library."
        )

        st.markdown("""
        **Example actions:**

        - Examine the bookshelf
        - Investigate the desk
        - Read the notebook
        - Open the drawer with 2741
        - Collect the brass key
        - Inspect the painting
        - Unlock the door with 1936
        - Check inventory
        """)

        st.info(
            "Python validates every action. Gemini "
            "cannot directly change the game state."
        )

    # Gemini is OFF by default to keep gameplay fast.
    use_gemini = st.checkbox(
        "✨ Use Gemini AI narration (optional)",
        value=False,
        help=(
            "When enabled, Gemini rewrites Python's "
            "validated response. Python remains in control."
        )
    )

    if use_gemini:
        st.caption(
            "Gemini narration enabled. Python responses "
            "will be used automatically if Gemini fails."
        )
    else:
        st.caption(
            "Fast Python gameplay mode. No API request needed."
        )

    # Display previous messages
    for msg in st.session_state.messages_v2:

        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Player input
    prompt = st.chat_input(
        "Describe your action..."
    )

    if prompt:

        # Store player action
        st.session_state.messages_v2.append({
            "role": "user",
            "content": prompt
        })

        # Python validates the action and updates state.
        result = process_action(
            prompt,
            st.session_state.game_state
        )

        # Gemini only changes narration, never game state.
        answer = optional_narration(
            result,
            use_gemini=use_gemini
        )

        # Store the final response.
        st.session_state.messages_v2.append({
            "role": "assistant",
            "content": answer
        })

        st.rerun()
