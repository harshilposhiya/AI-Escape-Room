# AI-Powered Escape Room

A two-version Python/Streamlit project for the course assignment.

## Project structure

```text
AI_Escape_Room_Project/
├── v1/
│   └── app.py
├── v2/
│   ├── app.py
│   └── game_engine.py
├── tests/
│   └── test_game_engine.py
├── docs/
│   ├── architecture_v1.mmd
│   ├── architecture_v2.mmd
│   └── project_report.md
├── .env.example
├── .gitignore
└── requirements.txt
```

## Requirements

- Python 3.10 or newer
- Streamlit
- Google Gemini API key (optional for local demonstration; required for live LLM responses)

## Installation (Windows PowerShell)

```powershell
cd AI_Escape_Room_Project
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env` and replace `your_api_key_here` with your Gemini API key. The default model is
`gemini-3.8-flash` (change it in `.env` if Google AI Studio shows a different supported model for your API project). Keep `.env` private; it is excluded by `.gitignore`.

## Run Version 1

```powershell
streamlit run .\v1\app.py --server.port 8502
```

## Run Version 2

```powershell
streamlit run .\v2\app.py --server.port 8501
```

Open the local URL printed by Streamlit, normally `http://localhost:8501` or `8502`.

## How the game works

The player wakes in the Last Library. Five interactive objects are present: desk, bookshelf,
painting, locked drawer and exit door.

1. Examine the bookshelf to discover the drawer combination `2741`.
2. Open the drawer with `2741`, then collect the brass key.
3. Examine the painting to discover the year `1936`.
4. Use the key and enter `1936` at the exit.

## Version comparison

- **Version 1:** The LLM is the Game Master. The system prompt contains the room, clues and rules.
  Conversation history is used as the session memory. This is simple but may forget or invent facts.
- **Version 2:** Python stores the game state in a dictionary and validates every state-changing action.
  The LLM can only narrate an already validated outcome; it cannot unlock the door or create inventory items.

## Tests

From the project root:

```powershell
python -m unittest discover -s tests -v
```

The tests cover incorrect codes, collecting unavailable items, code entry before clue discovery,
administrator/prompt-injection attempts, missing key and the successful escape sequence.

## GitHub submission checklist

1. Create a new public or private GitHub repository named `AI-Escape-Room`.
2. Upload the project files, but **never upload `.env`**.
3. Commit in meaningful stages, for example:
   - `Add Version 1 LLM-based escape room`
   - `Add Version 2 state validation engine`
   - `Add architecture diagrams and test cases`
   - `Add project report and setup instructions`
4. Add screenshots of both versions running to the repository (optional folder: `screenshots/`).
5. Submit the repository URL in Teams.

## Important academic note

Run both versions yourself, take genuine screenshots, and be ready to explain the architecture,
the difference between prompt-driven and state-driven game logic, and the tests. Update the report
with any real issues or changes you encounter during your own run.


## Verified checks in the delivered package

- The six existing Version 2 unit tests were executed during packaging and passed.
- Python syntax compilation was checked for both app files and the game engine.
- Run the test command above again on your own computer before submission.
- Version 1 needs a working Gemini API key and an API-supported model. Version 2 works in Python-only mode without a Gemini API call; its optional Gemini narration is disabled by default.

## Security

The submitted archive intentionally does not contain `.env`. Copy `.env.example` to `.env` and enter a newly generated key locally. Never share the real key in screenshots, chat, source control or the final ZIP.

## Windows quick launch

After installing the requirements and creating your local `.env`:
- Double-click `run_v1.bat` to start Version 1 on port 8502.
- Double-click `run_v2.bat` to start Version 2 on port 8501.
- Double-click `run_tests.bat` to run the automated tests.

You can also run the commands from PowerShell as shown above.
