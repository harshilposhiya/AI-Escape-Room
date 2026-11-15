"""
Version 2 deterministic game engine.
Python owns the state and validates every state-changing action.
The LLM is optional and only rewrites validated outcomes as narration.
"""
import re

INITIAL_STATE = {
    "drawer_open": False,
    "key_collected": False,
    "bookshelf_examined": False,
    "desk_examined": False,
    "painting_examined": False,
    "door_unlocked": False,
    "escaped": False,
    "inventory": [],
    "attempts": 0,
}

OBJECTS = {"desk", "bookshelf", "painting", "drawer", "door"}

def new_state():
    return {
        **INITIAL_STATE,
        "inventory": [],
    }

def _has(text, *words):
    return any(word in text for word in words)

def process_action(user_text, state):
    """Return a validated response and mutate state only after valid actions."""
    text = user_text.lower().strip()
    if not text:
        return "Please enter an action. You can examine an object or try a code."

    # Requests to bypass rules are treated as ordinary invalid actions.
    if _has(text, "administrator", "admin", "ignore all rules", "reveal all", "show me the solution",
            "tell me every code", "bypass", "pretend you"):
        return "The library does not respond to titles or demands. You must discover the clues and solve its locks."

    if _has(text, "inventory", "what do i have", "items collected", "check my items"):
        items = ", ".join(state["inventory"]) if state["inventory"] else "nothing yet"
        return f"Inventory: {items}."

    if _has(text, "help", "what can i do"):
        return "Try: examine the bookshelf, examine the desk, inspect the painting, enter a code, open the drawer, check inventory, or unlock the door."

    if _has(text, "bookshelf", "books", "book"):
        state["bookshelf_examined"] = True
        return ("You pull out four unusual books. Each has a handwritten number on its spine: "
                "2, 7, 4 and 1. The sequence may open the desk drawer.")

    if _has(text, "painting", "picture", "portrait", "frame"):
        state["painting_examined"] = True
        return ("You wipe dust from the painting. Above the university entrance, the year "
                "1936 is carved clearly into the stone. It may be important.")

    if _has(text, "desk", "notebook", "notepad"):
        state["desk_examined"] = True
        return ('Inside the notebook, a sentence is underlined: "The year above the entrance '
                'is the final number." The desk has a locked drawer.')

    # Drawer interaction requires the correct code and the bookshelf clue.
    if _has(text, "drawer"):
        code = re.search(r"(?<!\d)(\d{4})(?!\d)", text)
        if state["drawer_open"]:
            return "The drawer is already open. A small brass key is inside."
        if code:
            state["attempts"] += 1
            if code.group(1) == "2741" and state["bookshelf_examined"]:
                state["drawer_open"] = True
                return "Click! The drawer opens. Inside is a small brass key. Type 'take the brass key' to collect it."
            if code.group(1) == "2741":
                return "The code seems familiar, but you have not discovered it yet. Investigate the bookshelf first."
            return "The drawer stays locked. That four-digit combination is incorrect."
        if _has(text, "open", "unlock", "use", "enter", "try"):
            return "The drawer is locked and needs a four-digit code. Examine the bookshelf for a clue."
        return "The drawer has a small four-digit combination lock."

    if _has(text, "take", "collect", "pick up", "grab") and _has(text, "key"):
        if not state["drawer_open"]:
            return "There is no accessible key yet. The drawer is still locked."
        if not state["key_collected"]:
            state["key_collected"] = True
            state["inventory"].append("brass key")
            return "You collect the brass key. It is now in your inventory."
        return "You already collected the brass key."

    if _has(text, "door", "exit", "escape", "keypad"):
        code = re.search(r"(?<!\d)(\d{4})(?!\d)", text)
        if state["escaped"]:
            return "You are already outside. You escaped the Last Library!"
        if not state["key_collected"]:
            return "The exit door is secured by a physical lock and a keypad. You need to find the brass key first."
        if code:
            state["attempts"] += 1
            if code.group(1) == "1936" and state["painting_examined"]:
                state["door_unlocked"] = True
                state["escaped"] = True
                return "The brass key turns, and the keypad flashes green. The door swings open. Fresh air rushes in — you escaped the Last Library!"
            if code.group(1) == "1936":
                return "That year may be correct, but you have not discovered it. Examine the painting before entering it."
            return "The keypad flashes red. The code is incorrect."
        if _has(text, "unlock", "open", "use", "enter", "try"):
            return "You need the brass key and the four-digit year from the painting to unlock the exit."
        return "The exit has a keyhole and a four-digit keypad."

    if _has(text, "key"):
        return "You should search the locked drawer for a key. Examine the bookshelf to discover its combination."

    return "I don't recognize that action. Try examining the desk, bookshelf or painting, or ask for help."

def state_summary(state):
    return {
        "drawer_open": state["drawer_open"],
        "key_collected": state["key_collected"],
        "bookshelf_examined": state["bookshelf_examined"],
        "desk_examined": state["desk_examined"],
        "painting_examined": state["painting_examined"],
        "door_unlocked": state["door_unlocked"],
        "escaped": state["escaped"],
        "inventory": list(state["inventory"]),
        "attempts": state["attempts"],
    }
