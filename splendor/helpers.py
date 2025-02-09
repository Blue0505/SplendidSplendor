import numpy as np
from numpy.typing import NDArray

from .board import Board
from .player import Player
from .gem import Gem
from .card import Card
from .actions import SAction, SCategory
import ansi_escape_codes as ansi

def still_afford(player: Player, card: Card, gem_to_remove: Gem):
  "Check if a player can still afford a card after a gold is spent for a specific color."
  if player.get_gold() == 0:
    return False
  
  player.update_gems(gold=-1)
  can_afford = False

  if gem_to_remove == Gem.WHITE:
    card.update_gems(white=-1)
    can_afford = player.can_purchase(card)
    card.update_gems(white=1)
  elif gem_to_remove == Gem.BLUE:
    card.update_gems(blue=-1)
    can_afford = player.can_purchase(card)
    card.update_gems(blue=1)
  elif gem_to_remove == Gem.GREEN:
    card.update_gems(green=-1)
    can_afford = player.can_purchase(card)
    card.update_gems(green=1)
  elif gem_to_remove == Gem.RED:
    card.update_gems(red=-1)
    can_afford = player.can_purchase(card)
    card.update_gems(red=1)
  elif gem_to_remove == Gem.BLACK:
    card.update_gems(black=-1)
    can_afford = player.can_purchase(card)
    card.update_gems(black=1)
  
  player.update_gems(gold=1)
  return can_afford



def apply_take_gems(player: Player, board: Board, gem_tuple):
  """Moves gems from the board to the player."""
  player.update_gems(*gem_tuple)
  reduce = tuple(-gem for gem in gem_tuple)
  board.update_gems(*reduce)

def apply_reserve_purchase(player: Player, pos: int):
    """Changes a card of a player to be purchased instead of reserved."""
    card = player.pop_reserved_card(pos)
    player.add_purchased_card(card)
    return card

def apply_reserve(player: Player, board : Board, row, col):
  """Moves a card from the board to the reserve slot of a player."""
  if board.has_gold():
    board.update_gems(gold=-1)
    player.update_gems(gold=1)
  card = board.pop_card(row, col)
  player.add_reserved_card(card)

def apply_purchase(player: Player, board: Board, row, col) -> Card:
  """Moves a card from the board to the player and returns a gem array representing what must be paid."""
  card = board.pop_card(row, col)
  player.add_purchased_card(card)
  return card

def apply_end_spending_turn(player: Player, board: Board, card: Card): # TODO: Fix for using private members.
  player._gems -= card.get_costs_array()
  board._gems += card.get_costs_array()

def gem_array_str(gem_array, gold) -> str:
  """Returns a string reprsentation of a gem array and gold."""
  return (f"{ansi.WHITE}{gem_array[0]} {ansi.BLUE}{gem_array[1]} "
          f"{ansi.GREEN}{gem_array[2]} {ansi.RED}{gem_array[3]} "
          f"{ansi.GRAY}{gem_array[4]} {ansi.YELLOW}{gold}{ansi.RESET}")

def apply_spending_turn(player: Player, board: Board, card: Card, gem):
  """Moves one specified gem from the player back to the board. """

  if gem == Gem.WHITE:
    player.update_gems(white=-1)
    board.update_gems(white=1)
    card.update_gems(white=-1)
  elif gem == Gem.BLUE:
    player.update_gems(blue=-1)
    board.update_gems(blue=1)
    card.update_gems(blue=-1)
  elif gem == Gem.GREEN:
    player.update_gems(green=-1)
    board.update_gems(green=1)
    card.update_gems(green=-1)
  elif gem == Gem.RED:
    player.update_gems(red=-1)
    board.update_gems(red=1)
    card.update_gems(red=-1)
  else: # Gem.BLACK.
    player.update_gems(black=-1)
    board.update_gems(black=1)
    card.update_gems(black=-1)

    
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

    actions.register_action(SAction.CONSUME_GOLD_WHITE, SCategory.SPENDING_TURN, Gem.WHITE)
    actions.register_action(SAction.CONSUME_GOLD_BLUE, SCategory.SPENDING_TURN, Gem.BLUE)
    actions.register_action(SAction.CONSUME_GOLD_GREEN, SCategory.SPENDING_TURN, Gem.GREEN)
    actions.register_action(SAction.CONSUME_GOLD_RED, SCategory.SPENDING_TURN, Gem.RED)
    actions.register_action(SAction.CONSUME_GOLD_BLACK, SCategory.SPENDING_TURN, Gem.BLACK)
    actions.register_action(SAction.END_SPENDING_TURN, SCategory.SPENDING_TURN, None)