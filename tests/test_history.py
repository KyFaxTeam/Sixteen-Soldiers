# tests/test_history.py
import unittest
from datetime import datetime
from typing import Dict

from src.models.move import Move
from src.reducers.history_reducer import history_reducer
from src.utils.history_utils import *

class TestHistoryManagement(unittest.TestCase):
    def setUp(self):
        """Initialize test environment before each test"""
        self.initial_state: Dict = {
            "history": [],
            "redo_stack": []
        }
        
        # Sample move data for testing
        self.sample_move_1 = {
            "from_pos": "A1",
            "to_pos": "B2",
            "player_id": 1,
            "timestamp": 0.0004,
            "piece_capturee": None
        }
        
        self.sample_move_2 = {
            "from_pos": "B2",
            "to_pos": "C3",
            "player_id": 2,
            "timestamp": 1.00007,
            "piece_capturee": "B3"
        }
        
        self.sample_multiple_capture = {
            "from_pos": "B2",
            "to_pos": "D4",
            "player_id": 1,
            "timestamp": 0.500008,
            "piece_capturee": "C4"
        }

    def test_add_move(self):
        """Test adding a new move to history"""
        # Add first move
        action = {
            "type": "ADD_MOVE_TO_HISTORY",
            "payload": self.sample_move_1
        }
        
        state = history_reducer(self.initial_state, action)
        
        # Verify move was added
        self.assertEqual(len(get_history(state)), 1)
        last_move = get_last_move(state)
        self.assertEqual(last_move.get_start_position(), "A1")
        self.assertEqual(last_move.get_end_position(), "B2")
        self.assertEqual(last_move.player_id, 1)

    def test_multiple_capture(self):
        """Test handling of multiple capture moves"""
        # Add initial move
        state = history_reducer(self.initial_state, {
            "type": "ADD_MOVE_TO_HISTORY",
            "payload": self.sample_move_1
        })
        
        # Add multiple capture move
        state = history_reducer(state, {
            "type": "ADD_MOVE_TO_HISTORY",
            "payload": self.sample_multiple_capture
        })
        
        last_move = get_last_move(state)
        self.assertTrue(last_move.capture_multiple)
        self.assertEqual(len(last_move.pos), 3)  # Should contain all positions
        print("timestamp timestamp timestamp timestamp : ", last_move.timestamp)
        self.assertEqual(len(last_move.timestamp), 2)  # Should contain all statemps

    def test_undo_redo(self):
        """Test undo and redo functionality"""
        # Add two moves
        state = self.initial_state
        state = history_reducer(state, {
            "type": "ADD_MOVE_TO_HISTORY",
            "payload": self.sample_move_1
        })
        state = history_reducer(state, {
            "type": "ADD_MOVE_TO_HISTORY",
            "payload": self.sample_move_2
        })
        
        # Test undo
        state = history_reducer(state, {"type": "UNDO_LAST_MOVE"})
        self.assertEqual(len(get_history(state)), 1)
        self.assertTrue(can_redo(state))
        
        # Test redo
        state = history_reducer(state, {"type": "REDO_MOVE"})
        self.assertEqual(len(get_history(state)), 2)
        self.assertFalse(can_redo(state))

    def test_clear_history(self):
        """Test clearing the history"""
        # Add some moves first
        state = self.initial_state
        state = history_reducer(state, {
            "type": "ADD_MOVE_TO_HISTORY",
            "payload": self.sample_move_1
        })
        state = history_reducer(state, {
            "type": "ADD_MOVE_TO_HISTORY",
            "payload": self.sample_move_2
        })
        
        # Clear history
        state = history_reducer(state, {"type": "CLEAR_HISTORY"})
        self.assertEqual(len(get_history(state)), 0)
        self.assertEqual(len(state["redo_stack"]), 0)

    def test_move_retrieval(self):
        """Test move retrieval functions"""
        state = self.initial_state
        
        # Add moves
        state = history_reducer(state, {
            "type": "ADD_MOVE_TO_HISTORY",
            "payload": self.sample_move_1
        })
        state = history_reducer(state, {
            "type": "ADD_MOVE_TO_HISTORY",
            "payload": self.sample_move_2
        })
        
        # Test get_move_at
        first_move = get_move_at(state, 0)
        self.assertEqual(first_move.get_start_position(), "A1")
        
        # Test get_last_move
        last_move = get_last_move(state)
        self.assertEqual(last_move.get_start_position(), "B2")
        
        # Test invalid index
        invalid_move = get_move_at(state, 99)
        self.assertIsNone(invalid_move)

    def test_error_handling(self):
        """Test error handling scenarios"""
        # Test with None action
        state = history_reducer(self.initial_state, None)
        self.assertEqual(state, self.initial_state)
        
        # Test undo on empty history
        state = history_reducer(self.initial_state, {"type": "UNDO_LAST_MOVE"})
        self.assertEqual(len(get_history(state)), 0)
        
        # Test redo on empty redo stack
        state = history_reducer(self.initial_state, {"type": "REDO_MOVE"})
        self.assertEqual(len(get_history(state)), 0)

if __name__ == '__main__':
    unittest.main()


 # To run this test, you will paste this command in your terminal : python -m unittest tests/test_history.py -v