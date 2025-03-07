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
import numpy as np
from numpy.typing import NDArray
import enum

from splendor.board import Board
from splendor.player import Player
from splendor.card import Card
from splendor.gems import Gems
from splendor.actions import SActions, SAction, SCategory
import splendor.ansi_escape_codes as ansi

_NUM_PLAYERS = 2
_CARDS_FILENAME = "../data/cards.csv"
_WIN_POINTS = 15
_MAX_PLAYER_GEMS = 10
_MAX_TAKE2_GEMS = 4

_CARD_SHAPE = 11
_GEM_SHAPE = 6
_BOARD_SHAPE = ( _CARD_SHAPE * 12 ) + _GEM_SHAPE
_PLAYER_SHAPE = _GEM_SHAPE + ( 3 * _CARD_SHAPE ) + 1 + 5 
_TENSOR_SHAPE = ( _NUM_PLAYERS * _PLAYER_SHAPE ) + _BOARD_SHAPE + _CARD_SHAPE
_DECK_CARDS = 5

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
    provides_information_state_string=False,
    provides_information_state_tensor=False,
    provides_observation_string=True,
    provides_observation_tensor=True,
    parameter_specification={"shuffle_cards": True},
)

_GAME_INFO = pyspiel.GameInfo(
    num_distinct_actions=len(SAction),
    max_chance_outcomes=0,
    num_players=2,
    min_utility=-1,  
    max_utility=1, 
    utility_sum=0.0,
    max_game_length=1000,
)


class TurnType(enum.IntEnum):
    NORMAL = 0
    # SPENDING = enum.auto()  # Player consumes gold for a card.
    # RETURN = enum.auto()  # Player gives back gems to the board to not exceed 10 gems.


class SplendorGame(pyspiel.Game):
    """Two player implementation of the Splendor board game."""

    def __init__(self, params=None):
        super().__init__(_GAME_TYPE, _GAME_INFO, params or dict())
        game_parameters = self.get_parameters()
        self.shuffle_cards = game_parameters.get("shuffle_cards")

    def new_initial_state(self):
        return SplendorState(self, self.shuffle_cards)

    def make_py_observer(self, iig_obs_type=None, params=None):
        return BoardObserver(params)


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
        self._actions = SActions()
        self._turn_type = TurnType.NORMAL
        self._spending_card: Card
        self._spending_card_exists: bool = False

    def current_player(self):
        """Returns id of the next player to move, or TERMINAL if game is over."""
        return pyspiel.PlayerId.TERMINAL if self._is_terminal else self._cur_player

    def _legal_actions(self, player):
        """Returns a list of legal actions, sorted in ascending order."""
        player = self._player_0 if self._cur_player == 0 else self._player_1
        legal_actions: list[int] = []

        # # "SPENDING" turn.
        # if self._turn_type == TurnType.SPENDING:
        #     consume_ids = self._actions.get_action_ids(SCategory.SPENDING_TURN)
        #     consume_ids.pop() # Remove END_SPENDING_TURN. 
        #     for action_id in consume_ids:
        #         gems = self._actions.get_action_object(action_id)
        #         if self.__spending_turn_afford(player, gems):
        #             legal_actions.append(action_id)

        #     # "End turn" actions.
        #     if self._spending_card_exists and player.can_purchase(self._spending_card, using_gold=False):
        #         legal_actions.append(SAction.END_SPENDING_TURN)

        #     return legal_actions

        # # "RETURN" turn.
        # elif self._turn_type == TurnType.RETURN:
        #     return_ids = self._actions.get_action_ids(SCategory.RETURN)
        #     for action_id in return_ids:
        #         gems = self._actions.get_action_object(action_id)
        #         if player.gems.has_at_least(gems):
        #             legal_actions.append(action_id)
        #     return legal_actions

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

        # "Purchase reversed" actions.
        purchase_reserve_ids = self._actions.get_action_ids(SCategory.PURCHASE_RESERVE)
        for card, action in zip(player._reserved_cards, purchase_reserve_ids):
            if player.can_purchase(card):
                legal_actions.append(action)

        # "Take 2" actions.
        take2_ids = self._actions.get_action_ids(SCategory.TAKE2)
        for action_id in take2_ids:
            gems_required = np.copy(self._actions.get_action_object(action_id))
            gems_required[gems_required != 0] = _MAX_TAKE2_GEMS
            if self._board.gems.has_at_least(gems_required):
                legal_actions.append(action_id)

        # "Take 3" actions.
        take3_ids = self._actions.get_action_ids(SCategory.TAKE3)
        for action_id in take3_ids:
            if self._board.gems.has_at_least(self._actions.get_action_object(action_id)):
                legal_actions.append(action_id)

        return sorted(legal_actions)

    def _apply_action(self, action):
        """Applies the specified action to the state."""

        player = self._player_0 if self._cur_player == 0 else self._player_1
        action_category = self._actions.get_category(action)
        action_object = self._actions.get_action_object(action)

        # if self._turn_type == TurnType.SPENDING:
        #     if action == SAction.END_SPENDING_TURN:
        #         self._turn_type = TurnType.NORMAL
        #         self.__apply_end_spending_turn(player)
        #     else:  # Player spent gold.
        #         self.__apply_spending_turn(player, action_object)

        # elif self._turn_type == TurnType.RETURN:
        #     player.num_returns += 1
        #     gems = np.copy(action_object)
        #     player.gems.update(-gems)
        #     self._board.gems.update(gems)
        #     if player.gems.get_gem_sum() <= 10:
        #         self._turn_type = TurnType.NORMAL
        #         self.__swap_player()

        # else:  # "NORMAL" turn.
        # Note: Everything below was indented. 
        if action_category == SCategory.RESERVE:
            row, col = action_object
            self.__apply_reserve(player, row, col)

        elif action_category == SCategory.PURCHASE:

            row, col = action_object
            self._spending_card = self._board.pop_card(row, col)
            # self._spending_card_exists = True
            # if player.gems.has_gold():
            #     self._turn_type = TurnType.SPENDING
            # else:
            self.__apply_end_spending_turn(player) # Note: Was indented. 


        elif action_category == SCategory.PURCHASE_RESERVE:
            self._spending_card = player.pop_reserved_card(action_object)
            # self._spending_card_exists = True
            # if player.gems.has_gold():
            #     self._turn_type = TurnType.SPENDING
            # else:
            self.__apply_end_spending_turn(player) # Note: Was indented. 

        elif (action_category == SCategory.TAKE2 or action_category == SCategory.TAKE3):
            self.__apply_take_gems(player, action_object)
            # if player.gems.get_gem_sum() > _MAX_PLAYER_GEMS:
            #     self._turn_type = TurnType.RETURN
            # else:
            self.__swap_player() # Note: Was indented. 

        if player.get_points() >= _WIN_POINTS:
            # print("WIN")
            self._is_terminal = True
        
        if not self._board.enough_cards():
            self._is_terminal = True
            # print("TIE: NOT ENOUGH CARDS")
        
        if len(self._legal_actions(self._cur_player)) == 0: # Next player has no action.
            player = self._player_0 if self._cur_player == 0 else self._player_1
            player.no_moves += 1
            self.__swap_player()
            if len(self._legal_actions(self._cur_player)) == 0: # Both players have no action.
                # print("TIE: NO ACTIONS")
                self._is_terminal = True
    
    def _action_to_string(self, player, action):  # TODO.
        """Action -> string."""
        return ""

    def is_terminal(self):
        """Returns True if the game is over."""
        return self._is_terminal

    def returns(self):
        """Total reward for each player over the course of the game so far."""
        if self._player_0.get_points() >= _WIN_POINTS:
            return [1, -1]
        elif self._player_1.get_points() >= _WIN_POINTS:
            return [-1, 1]
        else:
            return [0, 0]

    def __str__(self):
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
            player1_str += " <-- \n"

        output += player0_str + dashes + str(self._player_0)
        output += f"   Score: {self.returns()[0]}"
        output += player1_str + dashes + str(self._player_1)
        output += f"   Score: {self.returns()[1]}"

        # if self._turn_type == TurnType.SPENDING:
        #     output += f"{ansi.B_WHITE}\nSPENDING CARD:{ansi.RESET}\n"
        #     output += dashes
        #     output += "   " + str(self._spending_card) + "\n"


        return output

    def __swap_player(self):
        self._cur_player = 0 if self._cur_player == 1 else 1

    # def __spending_turn_afford(self, player: Player, gems_array: NDArray):
    #     "Check if a player can still afford a card after a gold is spent for a specific color."
    #     if player.gems.get_gold() == 0:
    #         return False
            
    #     if not self._spending_card.gems.has_at_least(gems_array):
    #         return False

    #     player.gems.update(np.array([0, 0, 0, 0, 0, -1]))
    #     can_afford = False

    #     self._spending_card.gems.update(-gems_array)
    #     can_afford = player.can_purchase(self._spending_card)
    #     self._spending_card.gems.update(gems_array)
    #     player.gems.update(np.array([0, 0, 0, 0, 0, 1]))
    #     return can_afford

    def __apply_take_gems(self, player: Player, gems):
        """Moves gems from the board to the player."""
        player.gems.update(gems)
        self._board.gems.update(-gems)

    def __apply_reserve(self, player: Player, row, col):
        """Moves a card from the board to the reserve slot of a player."""
        # if self._board.gems.has_gold():
        #     self._board.gems.update(np.array([0, 0, 0, 0, 0, -1]))
        #     player.gems.update(np.array([0, 0, 0, 0, 0, 1]))
        card = self._board.pop_card(row, col)
        player.add_reserved_card(card)
        self.__swap_player()

    def __apply_end_spending_turn(self, player: Player):
        self.__swap_player()
        # self._spending_card_exists = False
        to_update = self._spending_card.gems.get_array() - player.get_resources_array()
        to_update = np.clip(to_update, a_min=0, a_max=None)
        player.gems.update(-to_update)
        self._board.gems.update(to_update)
        player.add_purchased_card(self._spending_card)

    # def __apply_spending_turn(self, player: Player, gems: Gems):
    #     """Moves a player's gold back to the board and reduces the gem of the card it was used for."""
    #     player.gems.update(np.array([0, 0, 0, 0, 0, -1]))
    #     self._board.gems.update(np.array([0, 0, 0, 0, 0, 1]))
    #     self._spending_card.gems.update(-gems)

      


class BoardObserver:
    """Observer, conforming to the PyObserver interface (see observation.py).

    Observation objects:
        * Card: 
            - points
            - is_white, is_blue, is_green, is_red, is_black, 
            - white_cost, blue_cost, green_cost, red_cost, black_cost 
        
        * Player:
            - points
            - white_gems, blue_gems, green_gems, red_gems, black_gems, gold_gems
            - white_resources, blue_resources, green_resources, red_resources, black_resources
            - Card_reserved_{0..2}
        
        * Board:
            - white_gems, blue_gems, green_gems, red_gems, black_gems, gold_gems
            - Card_{0..3}{0..4}

        * Purchase_Card:
            - Card
    
        Observation objects can be generated in the __array__ methods of the corresponding class type. 
    
    Observation tensor: [ Player0, Player1, Board, Purchase_Card ]
    """

    def __init__(self, params):
        """Initializes an empty observation tensor."""
        if params:
            raise ValueError(f"Observation parameters not supported; passed {params}")
    
        self.tensor = np.zeros(_TENSOR_SHAPE)
        self.dict = {"observation": self.tensor }

    def set_from(self, state, player):
        """Updates `tensor` and `dict` to reflect `state` from PoV of `player`."""

        del player

        self.tensor = np.concatenate([
            state._player_0,
            state._player_1,
            state._board,
            state._spending_card if state._spending_card_exists else np.zeros(_CARD_SHAPE)
        ])

    def string_from(self, state, player):
        del player
        return " ".join(str(x) for x in self.dict["observation"])

pyspiel.register_game(_GAME_TYPE, SplendorGame)
