from splendor.board import Board
from splendor.player import Player
from splendor.gem import Gem
from splendor.card import Card
from splendor.actions import SAction, SCategory
from splendor.helpers import gem_to_tuple
import splendor.ansi_escape_codes as ansi

def still_afford(player: Player, card: Card, gem_to_remove: Gem):
  "Check if a player can still afford a card after a gold is spent for a specific color."
  if player.get_gold() == 0:
    return False
  
  player.update_gems(gold=-1)
  can_afford = False

  gem_tuple = gem_to_tuple(gem_to_remove)
  gem_tuple = gem_tuple[:-1] # Remove gold.
  card.update_gems(*gem_tuple)
  can_afford = player.can_purchase(card)
  card.update_gems(*tuple(-gem for gem in gem_tuple))
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
  player.update_gems(*tuple(-card.get_costs_array()))
  board.update_gems(*tuple(card.get_costs_array()))
  # player._gems -= card.get_costs_array()
  # board._gems += card.get_costs_array()

def apply_spending_turn(player: Player, board: Board, card: Card, gem):
  """Moves one specified gem from the player back to the board. """
  gem_tuple = gem_to_tuple(gem)
  player.update_gems(*tuple(-gem for gem in gem_tuple))
  board.update_gems(*gem_tuple)
  card.update_gems(*tuple(-gem for gem in gem_tuple))

    
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
    
    actions.register_action(SAction.PURCHASE_01, SCategory.PURCHASE, (0, 1))
    actions.register_action(SAction.PURCHASE_02, SCategory.PURCHASE, (0, 2))
    actions.register_action(SAction.PURCHASE_03, SCategory.PURCHASE, (0, 3))
    actions.register_action(SAction.PURCHASE_04, SCategory.PURCHASE, (0, 4))
    actions.register_action(SAction.PURCHASE_11, SCategory.PURCHASE, (1, 1))
    actions.register_action(SAction.PURCHASE_12, SCategory.PURCHASE, (1, 2))
    actions.register_action(SAction.PURCHASE_13, SCategory.PURCHASE, (1, 3))
    actions.register_action(SAction.PURCHASE_14, SCategory.PURCHASE, (1, 4))
    actions.register_action(SAction.PURCHASE_11, SCategory.PURCHASE, (2, 1))
    actions.register_action(SAction.PURCHASE_22, SCategory.PURCHASE, (2, 2))
    actions.register_action(SAction.PURCHASE_23, SCategory.PURCHASE, (2, 3))
    actions.register_action(SAction.PURCHASE_24, SCategory.PURCHASE, (2, 4))
    
    actions.register_action(SAction.PURCHASE_RESERVE_0, SCategory.PURCHASE_RESERVE, 0)
    actions.register_action(SAction.PURCHASE_RESERVE_1, SCategory.PURCHASE_RESERVE, 1)
    actions.register_action(SAction.PURCHASE_RESERVE_2, SCategory.PURCHASE_RESERVE, 2)
    
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

    actions.register_action(SAction.RETURN_0, SCategory.RETURN, Gem.WHITE)
    actions.register_action(SAction.RETURN_1, SCategory.RETURN, Gem.BLUE)
    actions.register_action(SAction.RETURN_2, SCategory.RETURN, Gem.GREEN)
    actions.register_action(SAction.RETURN_3, SCategory.RETURN, Gem.RED)
    actions.register_action(SAction.RETURN_4, SCategory.RETURN, Gem.BLACK)
    actions.register_action(SAction.RETURN_GOLD, SCategory.RETURN, Gem.GOLD)

    actions.register_action(SAction.CONSUME_GOLD_WHITE, SCategory.SPENDING_TURN, Gem.WHITE)
    actions.register_action(SAction.CONSUME_GOLD_BLUE, SCategory.SPENDING_TURN, Gem.BLUE)
    actions.register_action(SAction.CONSUME_GOLD_GREEN, SCategory.SPENDING_TURN, Gem.GREEN)
    actions.register_action(SAction.CONSUME_GOLD_RED, SCategory.SPENDING_TURN, Gem.RED)
    actions.register_action(SAction.CONSUME_GOLD_BLACK, SCategory.SPENDING_TURN, Gem.BLACK)
    actions.register_action(SAction.END_SPENDING_TURN, SCategory.SPENDING_TURN, None)