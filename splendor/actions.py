from typing import Any
import enum

class Actions:
    """A class representing actions with an arbitrary object and category that can be accessed with an id."""
    def __init__(self):
        self._action_map = {}
    
    def register_action(self, id: int, category: int, action_object: Any):
        self._action_map[id] = (category, action_object)
    
    def get_action_object(self, id: int):
        return self._action_map[id][1]
    
    def get_category(self, id: int) -> int:
        return self._action_map[id][0]
    
    def get_action_ids(self, action_category: int):
        action_ids = []
        for action_id, dict_action_category, _ in self._action_map.values():
            if dict_action_category == action_category:
                action_ids.append(action_id)
        return action_ids


class SCategory(enum.IntEnum):
  """Action categories used in Splendor."""
  RESERVE = 0
  PURCHASE = enum.auto()
  PURCHASE_RESERVE = enum.auto()
  TAKE3 = enum.auto()
  TAKE2 = enum.auto()
  SPENDING_TURN = enum.auto()

class SAction(enum.IntEnum):
    "Action ids used in Splendor."
    RESERVE_00 = 0
    RESERVE_01 = enum.auto()
    RESERVE_02 = enum.auto()
    RESERVE_03 = enum.auto()
    RESERVE_04 = enum.auto()
    RESERVE_10 = enum.auto()
    RESERVE_11 = enum.auto()
    RESERVE_12 = enum.auto()
    RESERVE_13 = enum.auto()
    RESERVE_14 = enum.auto()
    RESERVE_20 = enum.auto()
    RESERVE_21 = enum.auto()
    RESERVE_22 = enum.auto()
    RESERVE_23 = enum.auto()
    RESERVE_24 = enum.auto()
    
    PURCHASE_00 = enum.auto()
    PURCHASE_01 = enum.auto()
    PURCHASE_02 = enum.auto()
    PURCHASE_03 = enum.auto()
    PURCHASE_10 = enum.auto()
    PURCHASE_11 = enum.auto()
    PURCHASE_12 = enum.auto()
    PURCHASE_13 = enum.auto()
    PURCHASE_20 = enum.auto()
    PURCHASE_21 = enum.auto()
    PURCHASE_22 = enum.auto()
    PURCHASE_23 = enum.auto()

    PURCHASE_RESERVE_0 = enum.auto()
    PURCHASE_RESERVE_1 = enum.auto()
    PURCHASE_RESERVE_2 = enum.auto()

    TAKE3_11100 = enum.auto()
    TAKE3_11010 = enum.auto()
    TAKE3_11001 = enum.auto()
    TAKE3_10110 = enum.auto()
    TAKE3_10101 = enum.auto()
    TAKE3_10011 = enum.auto()
    TAKE3_01110 = enum.auto()
    TAKE3_01101 = enum.auto()
    TAKE3_01011 = enum.auto()
    TAKE3_00111 = enum.auto()
    
    TAKE2_0 = enum.auto()
    TAKE2_1 = enum.auto()
    TAKE2_2 = enum.auto()
    TAKE2_3 = enum.auto()
    TAKE2_4 = enum.auto()
    
    CONSUME_GOLD_WHITE = enum.auto()
    CONSUME_GOLD_BLUE = enum.auto()
    CONSUME_GOLD_GREEN = enum.auto()
    CONSUME_GOLD_RED = enum.auto()
    CONSUME_GOLD_BLACK = enum.auto()
    END_SPENDING_TURN = enum.auto()