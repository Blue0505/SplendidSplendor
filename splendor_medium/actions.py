import enum
import numpy as np
from typing import Any


class SCategory(enum.IntEnum):
    """Action categories used in Splendor."""

    RESERVE = 0
    PURCHASE = enum.auto()
    PURCHASE_RESERVE = enum.auto()
    TAKE3 = enum.auto()
    TAKE2 = enum.auto()
    RETURN = enum.auto()
    SPENDING_TURN = enum.auto()


class SAction(enum.IntEnum):
    "Action ids used in Splendor."

    RESERVE_00 = 0  # Hidden card.
    RESERVE_01 = enum.auto()
    RESERVE_02 = enum.auto()
    RESERVE_03 = enum.auto()
    RESERVE_04 = enum.auto()
    RESERVE_10 = enum.auto()  # Hidden card.
    RESERVE_11 = enum.auto()
    RESERVE_12 = enum.auto()
    RESERVE_13 = enum.auto()
    RESERVE_14 = enum.auto()
    RESERVE_20 = enum.auto()  # Hidden card.
    RESERVE_21 = enum.auto()
    RESERVE_22 = enum.auto()
    RESERVE_23 = enum.auto()
    RESERVE_24 = enum.auto()

    PURCHASE_01 = enum.auto()
    PURCHASE_02 = enum.auto()
    PURCHASE_03 = enum.auto()
    PURCHASE_04 = enum.auto()
    PURCHASE_11 = enum.auto()
    PURCHASE_12 = enum.auto()
    PURCHASE_13 = enum.auto()
    PURCHASE_14 = enum.auto()
    PURCHASE_21 = enum.auto()
    PURCHASE_22 = enum.auto()
    PURCHASE_23 = enum.auto()
    PURCHASE_24 = enum.auto()

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

    # RETURN_0 = enum.auto()
    # RETURN_1 = enum.auto()
    # RETURN_2 = enum.auto()
    # RETURN_3 = enum.auto()
    # RETURN_4 = enum.auto()
    # RETURN_GOLD = enum.auto()

    # CONSUME_GOLD_WHITE = enum.auto()
    # CONSUME_GOLD_BLUE = enum.auto()
    # CONSUME_GOLD_GREEN = enum.auto()
    # CONSUME_GOLD_RED = enum.auto()
    # CONSUME_GOLD_BLACK = enum.auto()
    # END_SPENDING_TURN = enum.auto()
    
SPLENDOR_ACTIONS = {
    SAction.RESERVE_00: (SCategory.RESERVE, (0, 0)),
    SAction.RESERVE_01: (SCategory.RESERVE, (0, 1)),
    SAction.RESERVE_02: (SCategory.RESERVE, (0, 2)),
    SAction.RESERVE_03: (SCategory.RESERVE, (0, 3)),
    SAction.RESERVE_04: (SCategory.RESERVE, (0, 4)),
    SAction.RESERVE_10: (SCategory.RESERVE, (1, 0)),
    SAction.RESERVE_11: (SCategory.RESERVE, (1, 1)),
    SAction.RESERVE_12: (SCategory.RESERVE, (1, 2)),
    SAction.RESERVE_13: (SCategory.RESERVE, (1, 3)),
    SAction.RESERVE_14: (SCategory.RESERVE, (1, 4)),
    SAction.RESERVE_20: (SCategory.RESERVE, (2, 0)),
    SAction.RESERVE_21: (SCategory.RESERVE, (2, 1)),
    SAction.RESERVE_22: (SCategory.RESERVE, (2, 2)),
    SAction.RESERVE_23: (SCategory.RESERVE, (2, 3)),
    SAction.RESERVE_24: (SCategory.RESERVE, (2, 4)),
    SAction.PURCHASE_01: (SCategory.PURCHASE, (0, 1)),
    SAction.PURCHASE_02: (SCategory.PURCHASE, (0, 2)),
    SAction.PURCHASE_03: (SCategory.PURCHASE, (0, 3)),
    SAction.PURCHASE_04: (SCategory.PURCHASE, (0, 4)),
    SAction.PURCHASE_11: (SCategory.PURCHASE, (1, 1)),
    SAction.PURCHASE_12: (SCategory.PURCHASE, (1, 2)),
    SAction.PURCHASE_13: (SCategory.PURCHASE, (1, 3)),
    SAction.PURCHASE_14: (SCategory.PURCHASE, (1, 4)),
    SAction.PURCHASE_21: (SCategory.PURCHASE, (2, 1)),
    SAction.PURCHASE_22: (SCategory.PURCHASE, (2, 2)),
    SAction.PURCHASE_23: (SCategory.PURCHASE, (2, 3)),
    SAction.PURCHASE_24: (SCategory.PURCHASE, (2, 4)),
    SAction.PURCHASE_RESERVE_0: (SCategory.PURCHASE_RESERVE, 0),
    SAction.PURCHASE_RESERVE_1: (SCategory.PURCHASE_RESERVE, 1),
    SAction.PURCHASE_RESERVE_2: (SCategory.PURCHASE_RESERVE, 2),
    SAction.TAKE3_11100: (SCategory.TAKE3, np.array([1, 1, 1, 0, 0, 0])),
    SAction.TAKE3_11010: (SCategory.TAKE3, np.array([1, 1, 0, 1, 0, 0])),
    SAction.TAKE3_11001: (SCategory.TAKE3, np.array((1, 1, 0, 0, 1, 0))),
    SAction.TAKE3_10110: (SCategory.TAKE3, np.array((1, 0, 1, 1, 0, 0))),
    SAction.TAKE3_10101: (SCategory.TAKE3, np.array((1, 0, 1, 0, 1, 0))),
    SAction.TAKE3_10011: (SCategory.TAKE3, np.array([1, 0, 0, 1, 1, 0])),
    SAction.TAKE3_01110: (SCategory.TAKE3, np.array([0, 1, 1, 1, 0, 0])),
    SAction.TAKE3_01101: (SCategory.TAKE3, np.array([0, 1, 1, 0, 1, 0])),
    SAction.TAKE3_01011: (SCategory.TAKE3, np.array([0, 1, 0, 1, 1, 0])),
    SAction.TAKE3_00111: (SCategory.TAKE3, np.array([0, 0, 1, 1, 1, 0])),
    SAction.TAKE2_0: (SCategory.TAKE2, np.array([2, 0, 0, 0, 0, 0])),
    SAction.TAKE2_1: (SCategory.TAKE2, np.array([0, 2, 0, 0, 0, 0])),
    SAction.TAKE2_2: (SCategory.TAKE2, np.array([0, 0, 2, 0, 0, 0])),
    SAction.TAKE2_3: (SCategory.TAKE2, np.array([0, 0, 0, 2, 0, 0])),
    SAction.TAKE2_4: (SCategory.TAKE2, np.array([0, 0, 0, 0, 2, 0])),
}

class SActions: 
    """A class representing splendor actions associated with an arbitrary object and category that can be accessed with an id."""

    def __init__(self):
        self._action_map = SPLENDOR_ACTIONS

    def get_action_object(self, id: int):
        return self._action_map[id][1]

    def get_category(self, id: int) -> int:
        return self._action_map[id][0]

    def get_action_ids(self, action_category: int):
        action_ids = []
        for action_id, (dict_action_category, _) in self._action_map.items():
            if dict_action_category == action_category:
                action_ids.append(action_id)
        return action_ids
