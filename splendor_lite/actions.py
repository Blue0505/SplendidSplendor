import enum
import numpy as np
from typing import Any


class SCategory(enum.IntEnum):
    """Action categories used in Splendor."""

    PURCHASE = enum.auto()
    TAKE3 = enum.auto()


class SAction(enum.IntEnum):
    "Action ids used in Splendor."

    PURCHASE_01 = 0
    PURCHASE_02 = enum.auto()
    PURCHASE_11 = enum.auto()
    PURCHASE_12 = enum.auto()
    PURCHASE_21 = enum.auto()
    PURCHASE_22 = enum.auto()

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
    
SPLENDOR_ACTIONS = {
    SAction.PURCHASE_01: (SCategory.PURCHASE, (0, 1)),
    SAction.PURCHASE_02: (SCategory.PURCHASE, (0, 2)),
    SAction.PURCHASE_11: (SCategory.PURCHASE, (1, 1)),
    SAction.PURCHASE_12: (SCategory.PURCHASE, (1, 2)),
    SAction.PURCHASE_21: (SCategory.PURCHASE, (2, 1)),
    SAction.PURCHASE_22: (SCategory.PURCHASE, (2, 2)),
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
