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

from open_spiel.python.observation import IIGObserverForPublicInfoGame
import pyspiel
import enum

from splendor.board import Board, BOARD_GEM_START
from splendor.player import Player
from splendor.actions import Actions, SAction, SCategory
from splendor.gem import Gem
import splendor.engine as engine
import splendor.ansi_escape_codes as ansi
from splendor.helpers import gem_to_tuple

_NUM_PLAYERS = 2
_CARDS_FILENAME = 'data/cards.csv'
_WIN_POINTS = 15
_MAX_PLAYER_GEMS = 10

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
  parameter_specification={
    "shuffle_cards": True
  })

_GAME_INFO = pyspiel.GameInfo( # TODO: Fix.
  num_distinct_actions=51,
  max_chance_outcomes=0,
  num_players=2,
  min_utility=-1.0,
  max_utility=1.0,
  utility_sum=0.0,
  max_game_length=1000)

class TurnType(enum.IntEnum):
  NORMAL = 0
  SPENDING = enum.auto() # Player consumes gold for a card.
  RETURN = enum.auto() # Player gives back gems to the board to not exceed 10 gems.


class SplendorGame(pyspiel.Game):
  """Two player implementation of the Splendor board game."""

  def __init__(self, params=None):
    super().__init__(_GAME_TYPE, _GAME_INFO, params or dict())
    game_parameters = self.get_parameters()
    self.shuffle_cards = game_parameters.get("shuffle_cards")

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
    engine.register_splendor_actions(self._actions)
    self._turn_type = TurnType.NORMAL


  def current_player(self):
    """Returns id of the next player to move, or TERMINAL if game is over."""
    return pyspiel.PlayerId.TERMINAL if self._is_terminal else self._cur_player

  def _legal_actions(self, player):
    """Returns a list of legal actions, sorted in ascending order."""
    player = self._player_0 if self._cur_player == 0 else self._player_1
    legal_actions: list[int] = []

    # "SPENDING" turn.
    if self._turn_type == TurnType.SPENDING:
      # "Spending gold" actions. 
      if engine.still_afford(player, self._spending_card, Gem.WHITE):
        legal_actions.append(SAction.CONSUME_GOLD_WHITE)
      if engine.still_afford(player, self._spending_card, Gem.BLUE):
        legal_actions.append(SAction.CONSUME_GOLD_BLUE)
      if engine.still_afford(player, self._spending_card, Gem.GREEN):
        legal_actions.append(SAction.CONSUME_GOLD_GREEN)
      if engine.still_afford(player, self._spending_card, Gem.RED):
        legal_actions.append(SAction.CONSUME_GOLD_RED)
      if engine.still_afford(player, self._spending_card, Gem.BLACK):
        legal_actions.append(SAction.CONSUME_GOLD_BLACK)

      # "End turn" action.
      if player.can_purchase(self._spending_card, using_gold=False):
        legal_actions.append(SAction.END_SPENDING_TURN)
      
        return legal_actions
    
    # "RETURN" turn.
    elif self._turn_type == TurnType.RETURN:
      if player.has_gems(white=1): 
        legal_actions.append(SAction.RETURN_0)
      if player.has_gems(blue=1):
        legal_actions.append(SAction.RETURN_1)
      if player.has_gems(green=1): 
        legal_actions.append(SAction.RETURN_2)
      if player.has_gems(red=1): 
        legal_actions.append(SAction.RETURN_3)
      if player.has_gems(black=1): 
        legal_actions.append(SAction.RETURN_4)
      if player.has_gems(gold=1):
        legal_actions.append(SAction.RETURN_GOLD)
      return legal_actions
  
    # "NORMAL" turn.

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

    return sorted(legal_actions)

  def _apply_action(self, action):
    """Applies the specified action to the state."""
    player = self._player_0 if self._cur_player == 0 else self._player_1
    action_category = self._actions.get_category(action)
    action_object = self._actions.get_action_object(action)
    
    if self._turn_type == TurnType.SPENDING:
      if action == SAction.END_SPENDING_TURN:
        self.spending_turn = False
        self._cur_player = 1 if self._cur_player == 0 else 1
        engine.apply_end_spending_turn(player, self._board, self._spending_card)
      else: # Player spent gold.
        engine.apply_spending_turn(player, self._board, self._spending_card, action_object)

      return 
    
    elif self._turn_type == TurnType.RETURN:
      gem_tuple = gem_to_tuple(action_object)
      player.update_gems(*(-gem for gem in gem_tuple))
      self._board.update_gems(*gem_tuple)
      if player.get_sum() <= 10:
        self._turn_type = TurnType.NORMAL
        self.__swap_player()
    
    else: # "NORMAL" turn.
      if action_category == SCategory.RESERVE: 
        engine.apply_reserve(player, self._board, *action_object)
        self.__swap_player()

      elif action_category == SCategory.PURCHASE: 
        self._spending_card = engine.apply_purchase(player, self._board, *action_object)
        if player.has_gold(): self._turn_type = TurnType.SPENDING
        else: 
          engine.apply_end_spending_turn(player, self._board, self._spending_card)
          self.__swap_player()

      elif action_category == SCategory.PURCHASE_RESERVE:
        self._spending_card = player.pop_reserved_card(action_object)
        if player.has_gold(): self._turn_type = TurnType.SPENDING
     
        else:
          engine.apply_end_spending_turn(player, self._board, self._spending_card)
          self.__swap_player()

      elif action_category == SCategory.TAKE2 or action_category == SCategory.TAKE3:
        engine.apply_take_gems(player, self._board, action_object)
        if player.get_sum() > _MAX_PLAYER_GEMS:
          self._turn_type = TurnType.RETURN
        else:
          self.__swap_player()

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
    output = ""
    dashes = ("-" * 59) + "\n"

    output += f"{ansi.B_WHITE}\nBOARD:\n{ansi.RESET}" + dashes + str(self._board)

    player0_str = f"{ansi.B_WHITE}\nPLAYER 0:{ansi.RESET}"
    player1_str = f"{ansi.B_WHITE}\nPLAYER 1:{ansi.RESET}"
    if self._cur_player == 0:
      player0_str += " <-- \n"
      player1_str += "\n"
    else:
      player0_str += "\n"
      player1_str +=  " <-- \n"
      
    output += player0_str + dashes + str(self._player_0)
    output += player1_str + dashes + str(self._player_1)

    return output

  def __swap_player(self):
    self._cur_player = 0 if self._cur_player == 1 else 1


class BoardObserver:
  """Observer, conforming to the PyObserver interface (see observation.py)."""

  def __init__(self, params): pass 

  def set_from(self, state, player): pass

  def string_from(self, state, player): pass 

# Register the game with the OpenSpiel library
pyspiel.register_game(_GAME_TYPE, SplendorGame)