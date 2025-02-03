# Copyright 2019 DeepMind Technologies Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import enum
import numpy as np
from open_spiel.python.observation import IIGObserverForPublicInfoGame
import pyspiel

from splendor_objects import *

_NUM_PLAYERS = 2
_TODO_VAL = 0
_CARDS_FILENAME = 'cards.csv'
_WIN_POINTS = 15

class SCategory(enum.IntEnum):
  RESERVE = 0
  PURCHASE = enum.auto()
  PURCHASE_RESERVE = enum.auto()
  TAKE3 = enum.auto()
  TAKE2 = enum.auto()
  CONSUME = enum.auto()

class SAction(enum.IntEnum):
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
    
    CONSUME_GEM = enum.auto()
    CONSUME_GOLD = enum.auto()


_GAME_TYPE = pyspiel.GameType(
    short_name="python_splendor",
    long_name="Python Splendor",
    dynamics=pyspiel.GameType.Dynamics.SEQUENTIAL,
    chance_mode=pyspiel.GameType.ChanceMode.DETERMINISTIC,
    information=pyspiel.GameType.Information.IMPERFECT_INFORMATION,
    utility=pyspiel.GameType.Utility.ZERO_SUM,
    reward_model=pyspiel.GameType.RewardModel.TERMINAL,
    max_num_players=_NUM_PLAYERS,
    min_num_players=_NUM_PLAYERS,
    provides_information_state_string=True, # TODO: Confused.  
    provides_information_state_tensor=True, # TODO: Confused. 
    provides_observation_string=True,
    provides_observation_tensor=True,
    parameter_specification={})

_GAME_INFO = pyspiel.GameInfo( # TODO: Neccesarily needs to have these parameters? Also set the parameters if neccesary. 
    num_distinct_actions=_TODO_VAL,
    max_chance_outcomes=0,
    num_players=2,
    min_utility=-1.0,
    max_utility=1.0,
    utility_sum=0.0,
    max_game_length=_TODO_VAL)


class SplendorGame(pyspiel.Game):
  """Two player implementation of the Splendor board game."""

  def __init__(self, params=None):
    super().__init__(_GAME_TYPE, _GAME_INFO, params or dict())
    self.shuffle_cards = params.get('shuffle_cards', True)

  def new_initial_state(self):
    return SplendorState(self, self.shuffle_cards)

  def make_py_observer(self, iig_obs_type=None, params=None): # TODO: Fix/update. 
    if ((iig_obs_type is None) or
        (iig_obs_type.public_info and not iig_obs_type.perfect_recall)):
      return BoardObserver(params)
    else:
      return IIGObserverForPublicInfoGame(iig_obs_type, params)
    


class SplendorState(pyspiel.State):
  """A python version of the Splendor state."""

  def __init__(self, game, shuffle_cards: bool):
    """Constructor; should only be called by Game.new_initial_state."""
    super().__init__(game)
    self._cur_player = 0
    self._is_terminal = False
    self._board: Board = Board(_CARDS_FILENAME, shuffle_cards)
    self._player_0: Player = Player()
    self._player_1: Player = Player()
    self._actions = Actions()
    register_splendor_actions(self._actions)



  def current_player(self):
    """Returns id of the next player to move, or TERMINAL if game is over."""
    return pyspiel.PlayerId.TERMINAL if self._is_terminal else self._cur_player

  def _legal_actions(self, player):
    """Returns a list of legal actions, sorted in ascending order."""
    player = self._player_0 if self._cur_player == 0 else self._player_1
    legal_actions: list[int] = []

      # "Reserving" action. 
    if player.can_reserve() and self._board.has_gems()

    # "Purchasing" action
    for card, action in zip(self._board.get, range(Action.PURCHASE_00, Action.PURCHASE_23 + 1)):
      if player.can_purchase(card):
        legal_actions.append(action)# # # 
    
    # "Purchase reversed" action
    for card, action in zip(player._reserved_cards, range(Action.PURCHASE_REVERSE_0, Action.PURCHASE_RESERVE_2 + 1)):
      if player.can_purchase(card):
        legal_actions.append(action)
        
    
    # "Take 2" 
    if self._board.has_gems(white=BOARD_GEM_START):
      legal_actions.append(Action.TAKE2_10000)
    if self._board.has_gems(blue=BOARD_GEM_START):
      legal_actions.append(Action.TAKE2_01000)
    if self._board.has_gems(green=BOARD_GEM_START):
      legal_actions.append(Action.TAKE2_00100)
    if self._board.has_gems(red=BOARD_GEM_START):
      legal_actions.append(Action.TAKE2_00010)
    if self._board.has_gems(black=BOARD_GEM_START):
      legal_actions.append(Action.TAKE2_00001)

    # "Take 3" actions. 
    if (self._board.has_gems(white=1, blue=1, green=1)):
      legal_actions.append(Action.TAKE3_11100)
    if (self._board.has_gems(white=1, blue=1, red=1)):
      legal_actions.append(Action.TAKE3_11010)
    if (self._board.has_gems(white=1, blue=1, black=1)):
      legal_actions.append(Action.TAKE3_11001)
    if (self._board.has_gems(white=1, green=1, red=1)):
      legal_actions.append(Action.TAKE3_10110)
    if (self._board.has_gems(white=1, green=1, red=1)):
      legal_actions.append(Action.TAKE3_10101)
    if (self._board.has_gems(white=1, red=1, black=1)):
      legal_actions.append(Action.TAKE3_10011)
    if (self._board.has_gems(blue=1, green=1, red=1)):
      legal_actions.append(Action.TAKE3_01110)
    if (self._board.has_gems(blue=1, green=1, gold=1)):
      legal_actions.append(Action.TAKE3_01101)
    if (self._board.has_gems(blue=1, red=1, black=1)):
      legal_actions.append(Action.TAKE3_01011)
    if (self._board.has_gems(green=1, red=1, black=1)):
      legal_actions.append(Action.TAKE3_00111)  

    return legal_actions.sort()

  def _apply_action(self, action):
    """Applies the specified action to the state."""
    # TODO: Update reward score.
    # TODO: Perform action.
    player = self._player_0 if self._cur_player == 0 else self._player_1
    category = self._actions.get_category(action)
    action_object = self._actions.get_action_object(action)
    if category == SCategory.RESERVE: pass
      # apply_reserve(player, self._board, action_object)
    elif category == SCategory.PURCHASE:
      pass# apply_purchase(player, self._board, action_object)
    elif category == SCategory.PURCHASE_RESERVE:
      pass# apply_purchase_reserve(player, self._board, action_object)
    elif category == SCategory.TAKE2:
      apply_take(player, self._board, action_object)
    elif category == SCategory.TAKE3:
      apply_take(player, self.board, action_object)
    



    if player.get_points() == _WIN_POINTS:
      self._is_terminal = True


  def _action_to_string(self, player, action):
    """Action -> string."""
    row, col = _coord(action)
    return "{}({},{})".format("x" if player == 0 else "o", row, col)

  def is_terminal(self):
    """Returns True if the game is over."""
    return self._is_terminal

  def returns(self):
    """Total reward for each player over the course of the game so far."""
    return [self._player0_score, -self._player0_score]

  def __str__(self):
    """String for debug purposes. No particular semantics are required."""
    return _board_to_string(self.board)


class BoardObserver:
  """Observer, conforming to the PyObserver interface (see observation.py)."""

  def __init__(self, params):
    """Initializes an empty observation tensor."""
    if params:
      raise ValueError(f"Observation parameters not supported; passed {params}")
    # The observation should contain a 1-D tensor in `self.tensor` and a
    # dictionary of views onto the tensor, which may be of any shape.
    # Here the observation is indexed `(cell state, row, column)`.
    shape = (1 + _NUM_PLAYERS, _NUM_ROWS, _NUM_COLS)
    self.tensor = np.zeros(np.prod(shape), np.float32)
    self.dict = {"observation": np.reshape(self.tensor, shape)}

  def set_from(self, state, player):
    """Updates `tensor` and `dict` to reflect `state` from PoV of `player`."""
    del player
    # We update the observation via the shaped tensor since indexing is more
    # convenient than with the 1-D tensor. Both are views onto the same memory.
    obs = self.dict["observation"]
    obs.fill(0)
    for row in range(_NUM_ROWS):
      for col in range(_NUM_COLS):
        cell_state = ".ox".index(state.board[row, col])
        obs[cell_state, row, col] = 1

  def string_from(self, state, player):
    """Observation of `state` from the PoV of `player`, as a string."""
    del player
    return _board_to_string(state.board)


# Helper functions for game details.


def _line_value(line):
  """Checks a possible line, returning the winning symbol if any."""
  if all(line == "x") or all(line == "o"):
    return line[0]


def _line_exists(board):
  """Checks if a line exists, returns "x" or "o" if so, and None otherwise."""
  return (_line_value(board[0]) or _line_value(board[1]) or
          _line_value(board[2]) or _line_value(board[:, 0]) or
          _line_value(board[:, 1]) or _line_value(board[:, 2]) or
          _line_value(board.diagonal()) or
          _line_value(np.fliplr(board).diagonal()))

def _board_to_string(board):
  """Returns a string representation of the board."""
  return "\n".join("".join(row) for row in board)


def apply_take(player: Player, board, action_object):
  player.update_gems(*action_object)
  reduce = tuple(-gem for gem in action_object)
  board.update_gems(*reduce)

def apply_reserve(player, board, action_object):
  board.update_gems(gold=-1)
  player.update_gems(gold=1)
  card = board.pop_card(action_object[0], action_object[1])
  player.reserve_card(card)

def register_splendor_actions(actions):
    actions.register_action(SAction.RESERVE_00, SCategory.RESERVE, (0, 0))
    actions.register_action(SAction.RESERVE_01, SCategory.RESERVE, (0, 1))
    actions.register_action(SAction.RESERVE_02, SCategory.RESERVE, (0, 2))
    actions.register_action(SAction.RESERVE_03, SCategory.RESERVE, (0, 3))
    actions.register_action(SAction.RESERVE_04, SCategory.RESERVE, (0, 4))
    actions.register_action(SAction.RESERVE_10, SCategory.RESERVE, (1, 0))
    actions.register_action(SAction.RESERVE_11, SCategory.RESERVE, (1, 1))
    actions.register_action(SAction.RESERVE_12, SCategory.RESERVE, (1, 2))
    actions.register_action(SAction.RESERVE_13, SCategory.RESERVE, (1, 3))
    actions.register_action(SAction.RESERVE_14, SCategory.RESERVE, (1, 4))
    actions.register_action(SAction.RESERVE_20, SCategory.RESERVE, (2, 0))
    actions.register_action(SAction.RESERVE_21, SCategory.RESERVE, (2, 1))
    actions.register_action(SAction.RESERVE_22, SCategory.RESERVE, (2, 2))
    actions.register_action(SAction.RESERVE_23, SCategory.RESERVE, (2, 3))
    actions.register_action(SAction.RESERVE_24, SCategory.RESERVE, (2, 4))
    
    actions.register_action(SAction.PURCHASE_00, SCategory.PURCHASE, (0, 0))
    actions.register_action(SAction.PURCHASE_01, SCategory.PURCHASE, (0, 1))
    actions.register_action(SAction.PURCHASE_02, SCategory.PURCHASE, (0, 2))
    actions.register_action(SAction.PURCHASE_03, SCategory.PURCHASE, (0, 3))
    actions.register_action(SAction.PURCHASE_10, SCategory.PURCHASE, (1, 0))
    actions.register_action(SAction.PURCHASE_11, SCategory.PURCHASE, (1, 1))
    actions.register_action(SAction.PURCHASE_12, SCategory.PURCHASE, (1, 2))
    actions.register_action(SAction.PURCHASE_13, SCategory.PURCHASE, (1, 3))
    actions.register_action(SAction.PURCHASE_10, SCategory.PURCHASE, (2, 0))
    actions.register_action(SAction.PURCHASE_21, SCategory.PURCHASE, (2, 1))
    actions.register_action(SAction.PURCHASE_22, SCategory.PURCHASE, (2, 2))
    actions.register_action(SAction.PURCHASE_23, SCategory.PURCHASE, (2, 3))
    
    actions.register_action(SAction.PURCHASE_RESERVE_0, SCategory.PURCHASE, 0)
    actions.register_action(SAction.PURCHASE_RESERVE_1, SCategory.PURCHASE, 1)
    actions.register_action(SAction.PURCHASE_RESERVE_2, SCategory.PURCHASE, 2)
    
    actions.register_action(SAction.TAKE3_11100, SCategory.TAKE3, (1, 1, 1, 0, 0))
    actions.register_action(SAction.TAKE3_11010, SCategory.TAKE3, (1, 1, 0, 1, 0))
    actions.register_action(SAction.TAKE3_11001, SCategory.TAKE3, (1, 1, 0, 0, 1))
    actions.register_action(SAction.TAKE3_10110, SCategory.TAKE3, (1, 0, 1, 1, 0))
    actions.register_action(SAction.TAKE3_10101, SCategory.TAKE3, (1, 0, 1, 0, 1))
    actions.register_action(SAction.TAKE3_10011, SCategory.TAKE3, (1, 0, 0, 1, 1))
    actions.register_action(SAction.TAKE3_01110, SCategory.TAKE3, (0, 1, 1, 1, 0))
    actions.register_action(SAction.TAKE3_01101, SCategory.TAKE3, (0, 1, 1, 0, 1))
    actions.register_action(SAction.TAKE3_01011, SCategory.TAKE3, (0, 1, 0, 1, 1))
    actions.register_action(SAction.TAKE3_00111, SCategory.TAKE3, (0, 0, 1, 1, 1))

    actions.register_action(SAction.TAKE2_0, SCategory.TAKE2, (2, 0, 0, 0, 0))
    actions.register_action(SAction.TAKE2_1, SCategory.TAKE2, (0, 2, 0, 0, 0))
    actions.register_action(SAction.TAKE2_2, SCategory.TAKE2, (0, 0, 2, 0, 0))
    actions.register_action(SAction.TAKE2_3, SCategory.TAKE2, (0, 0, 0, 2, 0))
    actions.register_action(SAction.TAKE2_4, SCategory.TAKE2, (0, 0, 0, 0, 2))

    actions.register_action(SAction.CONSUME_GEM, SCategory.CONSUME, None)
    actions.register_action(SAction.CONSUME_GOLD, SCategory.CONSUME, None)

# Register the game with the OpenSpiel library
pyspiel.register_game(_GAME_TYPE, SplendorGame)