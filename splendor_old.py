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

  def current_player(self):
    """Returns id of the next player to move, or TERMINAL if game is over."""
    return pyspiel.PlayerId.TERMINAL if self._is_terminal else self._cur_player

  def _legal_actions(self, player):
    """Returns a list of legal actions, sorted in ascending order."""
    player = self._player_0 if self._cur_player == 0 else self._player_1
    legal_actions: list[int] = []

    # TODO: Reserving a card.
    if player.can_reserve() and self._board.has_gems()
    # TODO: Buying a card.
    for deck_num in range(len(self._board.decks)):
      for card_num in range(len()):
        if player.gems.values() > card.costs.values():
          legal_actions.append(Action.purchase    
    
    # TODO: Take 2.
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

    # TODO: Take 3.
    if (self._board.has_gems(white=1, blue=1, green=1)):
      legal_actions.append(Action.TAKE3_11100)
    if (self._board.has_gems()):
      legal_actions.append(Action.TAKE3_11010)
    if (self._board.has_gems()):
      legal_actions.append(Action.TAKE3_11001)
    if (self._board.has_gems(      legal_actions.append(Action.TAKE3_10110)
    if (self._board.has_gems()):
      legal_actions.append(Action.TAKE3_10101)
    if (self._board.has_gems()):
      legal_actions.append(Action.TAKE3_10011)
    if (self._board.has_gems()):
      legal_actions.append(Action.TAKE3_01110)
    if (self._board.has_gems()):
      legal_actions.append(Action.TAKE3_01101)
    if (self._board.has_gems()):
      legal_actions.append(Action.TAKE3_01011)
    if (self._board.has_gems()):
      legal_actions.append(Action.TAKE3_00111)  

    # blue, green, red, black, gold

    # TODO: Return actions in ascending order. 

  def _apply_action(self, action):
    """Applies the specified action to the state."""
    self.board[_coord(action)] = "x" if self._cur_player == 0 else "o"
    if _line_exists(self.board):
      self._is_terminal = True
      self._player0_score = 1.0 if self._cur_player == 0 else -1.0
    elif all(self.board.ravel() != "."):
      self._is_terminal = True
    else:
      self._cur_player = 1 - self._cur_player

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


def _coord(move):
  """Returns (row, col) from an action id."""
  return (move // _NUM_COLS, move % _NUM_COLS)


def _board_to_string(board):
  """Returns a string representation of the board."""
  return "\n".join("".join(row) for row in board)


# Register the game with the OpenSpiel library

pyspiel.register_game(_GAME_TYPE, SplendorGame)
