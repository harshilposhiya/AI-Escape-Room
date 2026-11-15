
"""
AI ESCAPE ROOM - VERSION 1
Gemini-powered interactive escape room.

Run:
py -m streamlit run v1/app.py --server.port 8502
"""

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types


# ==========================================
# 1. CONFIGURATION
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env", override=True)

API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()

st.set_page_config(
    page_title="AI Escape Room - Version 1",
    page_icon="🔐",
    layout="centered"
)


# ==========================================
# 2. GAME MASTER PROMPT
# ==========================================

SYSTEM_PROMPT = """
You are the Game Master of THE LAST LIBRARY,
an interactive AI escape room.

STORY:
The player wakes up inside a locked library at midnight.

There are five objects:
1. A wooden desk with a dusty notebook.
2. A bookshelf with four unusual books.
3. A painting of an old university building.
4. A locked drawer.
5. An exit door with a four-digit keypad.

SECRET SOLUTION:
- Examining the four books reveals drawer code 2741.
- Entering 2741 opens the drawer.
- The drawer contains a brass key.
- The player must collect the key.
- Examining the painting reveals year 1936.
- The exit requires the brass key AND code 1936.
- The notebook says: "The year above the entrance is the final number."

RULES:
- Act as an engaging Game Master.
- Respond to natural language actions.
- Allow examination, investigation, collecting and using items.
- Remember all discovered clues and collected items from chat history.
- Never reveal codes before the player discovers their clues.
- Never invent extra objects, clues or solutions.
- Wrong codes must not open locks.
- The drawer and exit have separate locks.
- Never claim the player escaped without the key and correct code.
- If the player requests the full solution, offer a hint instead.
- Keep responses concise, interesting and atmospheric.
"""


# ==========================================
# 3. GEMINI CONNECTION
# ==========================================

def gemini_reply(history):

    if not API_KEY or API_KEY == "your_api_key_here":

        return (
            "⚠️ Gemini API key is missing.\n\n"
            "Please add a valid key to your .env file."
        )

    try:

        client = genai.Client(
            api_key=API_KEY,
            http_options={
                "timeout": 20000
            }
        )

        contents = []

        for message in history:

            role = (
                "user"
                if message["role"] == "user"
                else "model"
            )

            contents.append(
                types.Content(
                    role=role,
                    parts=[
                        types.Part(
                            text=message["content"]
                        )
                    ]
                )
            )

        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.5,
                max_output_tokens=220
            )
        )

        if response.text:
            return response.text.strip()

        return (
            "The library is silent. "
            "Try investigating another object."
        )

    except Exception as error:

        print("\n========== GEMINI ERROR ==========")
        print(type(error).__name__)
        print(str(error))
        print("==================================\n")

        return (
            "⚠️ **Gemini connection failed.**\n\n"
            f"Error type: `{type(error).__name__}`. "
            "Please check that your API key is active, "
            "the model name in `.env` is available to your project, "
            "and your internet connection is working. "
            "Try again in a moment."
        )


# ==========================================
# 4. SESSION STATE
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "started" not in st.session_state:
    st.session_state.started = False


# ==========================================
# 5. HEADER
# ==========================================

st.title("🔐 The Last Library")

st.caption(
    "AI Escape Room · Version 1 · Gemini-powered gameplay"
)

st.divider()


# ==========================================
# 6. INSTRUCTIONS
# ==========================================

with st.expander("📖 How to play"):

    st.markdown("""
    You are trapped inside a mysterious library.

    Investigate the objects, discover clues,
    collect items and find a way out.

    **Example actions:**

    - Examine the bookshelf.
    - Investigate the desk.
    - Read the notebook.
    - Open the drawer.
    - Collect the brass key.
    - Inspect the painting.
    - Unlock the exit.

    Version 1 uses Gemini and conversation history
    as its main game logic.
    """)


# ==========================================
# 7. RESTART GAME
# ==========================================

if st.button(
    "🔄 Restart Version 1",
    use_container_width=True
):

    st.session_state.messages = []
    st.session_state.started = False

    st.rerun()


# ==========================================
# 8. START GAME
# ==========================================

if not st.session_state.started:

    welcome = """
    🌙 **You wake beneath a green-shaded lamp.**

    Rain taps against the tall library windows.

    A wooden desk, a crowded bookshelf, an old painting,
    a locked drawer and a keypad-secured exit door
    surround you.

    The clock has stopped at midnight.

    You need to find a way out.

    **What will you investigate first?**
    """

    st.session_state.messages.append({
        "role": "assistant",
        "content": welcome
    })

    st.session_state.started = True


# ==========================================
# 9. DISPLAY CONVERSATION
# ==========================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ==========================================
# 10. PLAYER INPUT
# ==========================================

prompt = st.chat_input(
    "What do you want to do?"
)


# ==========================================
# 11. GEMINI RESPONSE
# ==========================================

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner(
            "🔮 The Game Master is thinking..."
        ):

            answer = gemini_reply(
                st.session_state.messages
            )

        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
