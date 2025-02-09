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

import numpy as np
from open_spiel.python.observation import IIGObserverForPublicInfoGame
import pyspiel

from splendor.card import Card
from splendor.board import Board, BOARD_GEM_START
from splendor.player import Player
from splendor.actions import Actions, SAction, SCategory
from splendor.gem import Gem
import splendor.helpers as helpers

_NUM_PLAYERS = 2
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
    provides_information_state_string=True,  
    provides_information_state_tensor=True,
    provides_observation_string=True,
    provides_observation_tensor=True,
    parameter_specification={})

_GAME_INFO = pyspiel.GameInfo( # TODO: Fix.
    max_chance_outcomes=0,
    num_players=2,
    min_utility=-1.0,
    max_utility=1.0,
    utility_sum=0.0,
    max_game_length=0)


class SplendorGame(pyspiel.Game):
  """Two player implementation of the Splendor board game."""

  def __init__(self, params=None):
    super().__init__(_GAME_TYPE, _GAME_INFO, params or dict())
    self.shuffle_cards = params.get('shuffle_cards', True) if params != None else True

  def new_initial_state(self):
    return SplendorState(self, self.shuffle_cards)

  def make_py_observer(self, iig_obs_type=None, params=None):
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
    helpers.register_splendor_actions(self._actions)
    self._spending_turn: bool = False


  def current_player(self):
    """Returns id of the next player to move, or TERMINAL if game is over."""
    return pyspiel.PlayerId.TERMINAL if self._is_terminal else self._cur_player

  def _legal_actions(self, player):
    """Returns a list of legal actions, sorted in ascending order."""
    player = self._player_0 if self._cur_player == 0 else self._player_1
    legal_actions: list[int] = []

    # Spending turn.
    if self._spending_turn:
      # "Spending gold" actions. 
      if helpers.still_afford(player, self._spending_card, Gem.WHITE):
        legal_actions.append(SAction.CONSUME_GOLD_WHITE)
      if helpers.still_afford(player, self._spending_card, Gem.BLUE):
        legal_actions.append(SAction.CONSUME_GOLD_BLUE)
      if helpers.still_afford(player, self._spending_card, Gem.GREEN):
        legal_actions.append(SAction.CONSUME_GOLD_GREEN)
      if helpers.still_afford(player, self._spending_card, Gem.RED):
        legal_actions.append(SAction.CONSUME_GOLD_RED)
      if helpers.still_afford(player, self._spending_card, Gem.BLACK):
        legal_actions.append(SAction.CONSUME_GOLD_BLACK)

      # "End turn" action.
      if player.can_purchase(self._spending_card, using_gold=False):
        legal_actions.append(SAction.END_SPENDING_TURN)
      
        return legal_actions

    # Normal turn.

    # "Reserving" action.
    if not player.reserve_limit():
      reserve_ids = self._actions.get_action_ids(SCategory.RESERVE)
      legal_actions.extend(reserve_ids)

    # "Purchasing" action.
    purchase_ids = self._actions.get_action_ids(SCategory.PURCHASE)
    for card, action in zip(self._board.get_visible_cards(), purchase_ids):
      if player.can_purchase(card):
        legal_actions.append(action)
    
    # "Purchase reversed" action. 
    purchase_reserve_ids = self._actions.get_action_ids(SCategory.PURCHASE_RESERVE)
    for card, action in zip(player._reserved_cards, purchase_reserve_ids):
      if player.can_purchase(card):
        legal_actions.append(action)
    
    # "Take 2" 
    if player.get_sum() <= 8: 
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
    if player.get_sum() <= 7:
      if (self._board.has_gems(white=1, blue=1, green=1)):
        legal_actions.append(SAction.TAKE3_11100)
      if (self._board.has_gems(white=1, blue=1, red=1)):
        legal_actions.append(SAction.TAKE3_11010)
      if (self._board.has_gems(white=1, blue=1, black=1)):
        legal_actions.append(SAction.TAKE3_11001)
      if (self._board.has_gems(white=1, green=1, red=1)):
        legal_actions.append(SAction.TAKE3_10110)
      if (self._board.has_gems(white=1, green=1, black=1)):
        legal_actions.append(SAction.TAKE3_10101)
      if (self._board.has_gems(white=1, red=1, black=1)):
        legal_actions.append(SAction.TAKE3_10011)
      if (self._board.has_gems(blue=1, green=1, red=1)):
        legal_actions.append(SAction.TAKE3_01110)
      if (self._board.has_gems(blue=1, green=1, black=1)):
        legal_actions.append(SAction.TAKE3_01101)
      if (self._board.has_gems(blue=1, red=1, black=1)):
        legal_actions.append(SAction.TAKE3_01011)
      if (self._board.has_gems(green=1, red=1, black=1)):
        legal_actions.append(SAction.TAKE3_00111)

    return legal_actions.sort()

  def _apply_action(self, action):
    """Applies the specified action to the state."""
    player = self._player_0 if self._cur_player == 0 else self._player_1
    action_category = self._actions.get_category(action)
    action_object = self._actions.get_action_object(action)
    
    # Spending turn.
    if self._spending_turn: 
      if action == SAction.END_SPENDING_TURN:
        self.spending_turn = False
        self._cur_player = 1 if self._cur_player == 0 else 1
        helpers.apply_end_spending_turn(player, self._board, self._spending_card)
      else: # Player spent gold.
        helpers.apply_spending_turn(player, self._board, self._spending_card, action_object)

      return 

    # Not a spending turn.
    if action_category == SCategory.RESERVE: 
      helpers.apply_reserve(player, self._board, *action_object)
      self._cur_player = 1 if self._cur_player == 0 else 1
    elif action_category == SCategory.PURCHASE: 
      self._spending_card = helpers.apply_purchase(player, self._board, *action_object)
      self._spending_turn = True
    elif action_category == SCategory.PURCHASE_RESERVE:
      self._spending_card = helpers.apply_reserve_purchase(player, *action_object)
      self._spending_turn = True
    elif action_category == SCategory.TAKE2 or action_category == SCategory.TAKE3:
      helpers.apply_take_gems(player, self._board, action_object)
      self._cur_player = 1 if self._cur_player == 0 else 1

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

  def set_from(self, state, player): pass

  def string_from(self, state, player): pass 

# Register the game with the OpenSpiel library
pyspiel.register_game(_GAME_TYPE, SplendorGame)