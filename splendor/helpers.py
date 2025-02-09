import numpy as np
from numpy.typing import NDArray

from .board import Board
from .player import Player
from .gem import Gem
from .card import Card
from .actions import SAction, SCategory

def still_afford(player: Player, to_remove_gems: NDArray, gem_to_remove: Gem, use_gold=False):
  "Check if a player can still afford a gem array after a color is updated."
  if gem_to_remove == Gem.WHITE:
     gem_tuple = (1, 0, 0, 0, 0)
  elif gem_to_remove == Gem.BLUE:
     gem_tuple = (0, 1, 0, 0, 0)
  elif gem_to_remove == Gem.GREEN:
     gem_tuple = (0, 0, 1, 0, 0)
  elif gem_to_remove == Gem.RED:
     gem_tuple = (0, 0, 0, 1, 0)
  elif gem_to_remove == Gem.BLACK:
     gem_tuple = (0, 0, 0, 0, 1)

  if not use_gold:
    player.update_gems(*gem_tuple)
  else:
     player.update_gems(gold=-1)

  gem_sum = to_remove_gems + np.array(gem_tuple) - player.get_gems_array()
  np.clip(gem_sum, amin=0)
  can_afford = True if np.sum(gem_sum) - player.get_gold() <= 0 else False
  
  if not use_gold:
     revert = tuple(-gem for gem in gem_tuple)
     player.update_gems(*revert)
  else:
     player.update_gems(gold=1)
     
  return can_afford

def apply_take_gems(player: Player, board : Board, gem_tuple):
  """Moves gems from the board to the player."""
  player.update_gems(*gem_tuple)
  reduce = tuple(-gem for gem in gem_tuple)
  board.update_gems(*gem_tuple)

def apply_reserve_purchase(player: Player, pos: int):
    """Changes a card of a player to be purchased instead of reserved."""
    card = player.pop_card(pos)
    player.add_purchased_card(card)
    return card.get_costs_array() - player.get_resources_array()

def apply_reserve(player: Player, board : Board, row, col):
  """Moves a card from the board to the reserve slot of a player."""
  if board.has_gold():
    board.update_gems(gold=-1)
    player.update_gems(gold=1)
  card = board.pop_card(row, col)
  player.reserve_card(card)

def apply_purchase(player: Player, board: Board, row, col) -> dict[Gem, int]:
  """Moves a card from the board to the player and returns a gem array representing what must be paid."""
  card = board.pop_card(row, col)
  player.purchase_card(card)
  return card.get_costs_array() - player.get_resources_array()

def apply_spending_turn(spending_dict, player: Player, board: Board, action_category, gem):
    """Moves one specified gem from the player back to the board. """
    spending_dict[gem] =- 1

    if action_category == SCategory.CONSUME_GOLD:
        player.update_gems(gold=-1)
        board.update_gems(gold=1)
        return

    if gem == Gem.WHITE:
        player.update_gems(white=-1)
        board.update_gems(white=1)
    elif gem == Gem.BLUE:
        player.update_gems(blue=-1)
        board.update_gems(blue=1)
    elif gem == Gem.GREEN:
        player.update_gems(green=-1)
        board.update_gems(green=1)
    elif gem == Gem.RED:
        player.update_gems(red=-1)
        board.update_gems(red=1)
    else: # Gem.BLACK.
        player.update_gems(black=-1)
        board.update_gems(black=1)

    
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

    actions.register_action(SAction.CONSUME_WHITE, SCategory.CONSUME_GEM, Gem.WHITE)
    actions.register_action(SAction.CONSUME_BLUE, SCategory.CONSUME_GEM, Gem.BLUE)
    actions.register_action(SAction.CONSUME_GREEN, SCategory.CONSUME_GEM, Gem.GREEN)
    actions.register_action(SAction.CONSUME_RED, SCategory.CONSUME_GEM, Gem.RED)
    actions.register_action(SAction.CONSUME_BLACK, SCategory.CONSUME_GEM, Gem.BLACK)
    actions.register_action(SAction.CONSUME_WHITE_GOLD, SCategory.CONSUME_GOLD, Gem.WHITE)
    actions.register_action(SAction.CONSUME_BLUE_GOLD, SCategory.CONSUME_GOLD, Gem.BLUE)
    actions.register_action(SAction.CONSUME_GREEN_GOLD, SCategory.CONSUME_GOLD, Gem.GREEN)
    actions.register_action(SAction.CONSUME_BLACK_GOLD, SCategory.CONSUME_GOLD, Gem.RED)
    actions.register_action(SAction.CONSUME_RED_GOLD, SCategory.CONSUME_GOLD, Gem.BLACK)