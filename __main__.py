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

from splendor.card import Card
from splendor.board import Board, BOARD_GEM_START
from splendor.player import Player
from splendor.actions import Actions, SAction, SCategory
import splendor.helpers as helpers

_NUM_PLAYERS = 2
_TODO_VAL = 0 # TODO: Remove.
_CARDS_FILENAME = 'data/cards.csv'
_WIN_POINTS = 15

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
    self.shuffle_cards = params.get('shuffle_cards', True) if params != None else True

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
    self._cur_player: int = 0
    self._is_terminal: bool = False
    self._board: Board = Board(_CARDS_FILENAME, shuffle_cards)
    self._player_0: Player = Player()
    self._player_1: Player = Player()
    self._actions: Actions = Actions()
    self._spending_turn: bool = False
    self._spending_gems_left: dict = dict()
    helpers.register_splendor_actions(self._actions)


  def current_player(self):
    """Returns id of the next player to move, or TERMINAL if game is over."""
    return pyspiel.PlayerId.TERMINAL if self._is_terminal else self._cur_player

  def _legal_actions(self, player):
    """Returns a list of legal actions, sorted in ascending order."""
    player = self._player_0 if self._cur_player == 0 else self._player_1
    legal_actions: list[int] = []

    # "Reserving" action. # TODO.
    # if player.can_reserve() and self._board.has_gems()

    # "Purchasing" action
    for card, action in zip(self._board.get_cards(), range(SAction.PURCHASE_00, SAction.PURCHASE_23 + 1)):
      if player.can_purchase(card):
        legal_actions.append(action)# # # 
    
    # "Purchase reversed" action
    for card, action in zip(player._reserved_cards, range(SAction.PURCHASE_RESERVE_0, SAction.PURCHASE_RESERVE_2 + 1)):
      if player.can_purchase(card):
        legal_actions.append(action)
        
    
    # "Take 2" 
    if self._board.has_gems(white=BOARD_GEM_START):
      legal_actions.append(SAction.TAKE2_0)
    if self._board.has_gems(blue=BOARD_GEM_START):
      legal_actions.append(SAction.TAKE2_1)
    if self._board.has_gems(green=BOARD_GEM_START):
      legal_actions.append(SAction.TAKE2_2)
    if self._board.has_gems(red=BOARD_GEM_START):
      legal_actions.append(SAction.TAKE2_3)
    if self._board.has_gems(black=BOARD_GEM_START):
      legal_actions.append(SAction.TAKE2_4)

    # "Take 3" actions. 
    if (self._board.has_gems(white=1, blue=1, green=1)):
      legal_actions.append(SAction.TAKE3_11100)
    if (self._board.has_gems(white=1, blue=1, red=1)):
      legal_actions.append(SAction.TAKE3_11010)
    if (self._board.has_gems(white=1, blue=1, black=1)):
      legal_actions.append(SAction.TAKE3_11001)
    if (self._board.has_gems(white=1, green=1, red=1)):
      legal_actions.append(SAction.TAKE3_10110)
    if (self._board.has_gems(white=1, green=1, red=1)):
      legal_actions.append(SAction.TAKE3_10101)
    if (self._board.has_gems(white=1, red=1, black=1)):
      legal_actions.append(SAction.TAKE3_10011)
    if (self._board.has_gems(blue=1, green=1, red=1)):
      legal_actions.append(SAction.TAKE3_01110)
    if (self._board.has_gems(blue=1, green=1, gold=1)):
      legal_actions.append(SAction.TAKE3_01101)
    if (self._board.has_gems(blue=1, red=1, black=1)):
      legal_actions.append(SAction.TAKE3_01011)
    if (self._board.has_gems(green=1, red=1, black=1)):
      legal_actions.append(SAction.TAKE3_00111)  

    return legal_actions.sort()

  def _apply_action(self, action):
    """Applies the specified action to the state."""
    # TODO: Update reward score.

    player = self._player_0 if self._cur_player == 0 else self._player_1
    action_category = self._actions.get_category(action)
    action_object = self._actions.get_action_object(action)
    
    if not self._spending_turn: 
      if action_category == SCategory.RESERVE: 
        helpers.apply_reserve(player, self._board, action_object)
      elif action_category == SCategory.PURCHASE or action_category == SCategory.PURCHASE_RESERVE:
        card = self._board.pop_card(action_object[0], action_object[1])
        self._spending_gems_left = helpers.card_costs_dict(card, player)
        self._spending_turn = True
      elif action_category == SCategory.TAKE2:
        helpers.apply_take_gems(player, self._board, action_object)
      elif action_category == SCategory.TAKE3:
        helpers.apply_take_gems(player, self._board, action_object)

    else: # self._spending turn is True. 
      helpers.apply_spending_turn(self._spending_gems_left, player, action_category, action_object)
      if not self._spending_gems_left:
        self._spending_turn = False
        self._cur_player = 1 if self._cur_player == 1 else 0


    
      
    
    if player.get_points() == _WIN_POINTS:
      self._is_terminal = True


  def _action_to_string(self, player, action): # TODO.
    """Action -> string."""
    return ""

  def is_terminal(self):
    """Returns True if the game is over."""
    return self._is_terminal

  def returns(self):
    """Total reward for each player over the course of the game so far."""
    return [self._player0_score, -self._player0_score]

  def __str__(self): # TODO.
    """String for debug purposes. No particular semantics are required."""
    return ""


class BoardObserver:
  """Observer, conforming to the PyObserver interface (see observation.py)."""

  def __init__(self, params): pass 
    # """Initializes an empty observation tensor."""
    # if params:
    #   raise ValueError(f"Observation parameters not supported; passed {params}")
    # # The observation should contain a 1-D tensor in `self.tensor` and a
    # # dictionary of views onto the tensor, which may be of any shape.
    # # Here the observation is indexed `(cell state, row, column)`.
    # shape = (1 + _NUM_PLAYERS, _NUM_ROWS, _NUM_COLS)
    # self.tensor = np.zeros(np.prod(shape), np.float32)
    # self.dict = {"observation": np.reshape(self.tensor, shape)}

  def set_from(self, state, player): pass
    # """Updates `tensor` and `dict` to reflect `state` from PoV of `player`."""
    # del player
    # # We update the observation via the shaped tensor since indexing is more
    # # convenient than with the 1-D tensor. Both are views onto the same memory.
    # obs = self.dict["observation"]
    # obs.fill(0)
    # for row in range(_NUM_ROWS):
    #   for col in range(_NUM_COLS):
    #     cell_state = ".ox".index(state.board[row, col])
    #     obs[cell_state, row, col] = 1

  def string_from(self, state, player): pass 
    # """Observation of `state` from the PoV of `player`, as a string."""
    # del player
    # return _board_to_string(state.board)


# Helper functions for game details.

# Register the game with the OpenSpiel library
pyspiel.register_game(_GAME_TYPE, SplendorGame)