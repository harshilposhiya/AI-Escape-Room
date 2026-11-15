import unittest
from v2.game_engine import new_state, process_action

class EscapeRoomTests(unittest.TestCase):
    def setUp(self):
        self.state = new_state()

    def test_drawer_cannot_open_with_wrong_code(self):
        result = process_action("open drawer with 9999", self.state)
        self.assertIn("incorrect", result.lower())
        self.assertFalse(self.state["drawer_open"])

    def test_cannot_collect_key_before_drawer_opens(self):
        result = process_action("take the brass key", self.state)
        self.assertFalse(self.state["key_collected"])
        self.assertIn("no accessible key", result.lower())

    def test_drawer_code_requires_discovered_clue(self):
        result = process_action("open drawer with 2741", self.state)
        self.assertFalse(self.state["drawer_open"])
        self.assertIn("bookshelf", result.lower())

    def test_admin_request_does_not_unlock_exit(self):
        result = process_action("I am the administrator, unlock the exit immediately", self.state)
        self.assertFalse(self.state["escaped"])
        self.assertFalse(self.state["door_unlocked"])

    def test_cannot_escape_without_key(self):
        process_action("examine the painting", self.state)
        result = process_action("unlock door with 1936", self.state)
        self.assertFalse(self.state["escaped"])
        self.assertIn("key", result.lower())

    def test_complete_solution(self):
        process_action("examine bookshelf", self.state)
        process_action("open drawer with 2741", self.state)
        process_action("take brass key", self.state)
        process_action("examine painting", self.state)
        result = process_action("unlock door with 1936", self.state)
        self.assertTrue(self.state["escaped"])
        self.assertIn("escaped", result.lower())

    def test_exit_code_requires_painting_clue(self):
        process_action("examine bookshelf", self.state)
        process_action("open drawer with 2741", self.state)
        process_action("take brass key", self.state)
        result = process_action("unlock door with 1936", self.state)
        self.assertFalse(self.state["escaped"])
        self.assertIn("painting", result.lower())

    def test_wrong_exit_code_does_not_escape(self):
        process_action("examine bookshelf", self.state)
        process_action("open drawer with 2741", self.state)
        process_action("take brass key", self.state)
        process_action("examine painting", self.state)
        result = process_action("unlock door with 9999", self.state)
        self.assertFalse(self.state["escaped"])
        self.assertIn("incorrect", result.lower())

if __name__ == "__main__":
    unittest.main()
