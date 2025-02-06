import enum

from .board import Board
from .player import Player
from .gem import Gem
from .card import Card
from .actions import SAction, SCategory


def apply_take_gems(player: Player, board : Board, action_object):
  player.update_gems(*action_object)
  reduce = tuple(-gem for gem in action_object)
  board.update_gems(*reduce)


def apply_reserve(player: Player, board : Board, action_object):
  board.update_gems(gold=-1)
  player.update_gems(gold=1)
  card = board.pop_card(action_object[0], action_object[1])
  player.reserve_card(card)

def apply_purchase(player: Player, board: Board, action_object):
  #Unused function (probably remove)
  card = board.pop_card(action_object[0], action_object[1])
  # TODO: gold gems?
  card_costs = card_costs_dict(card, player)
  player.update_gems(-card_costs[Gem.WHITE],-card_costs[Gem.BLUE],-card_costs[Gem.GREEN],-card_costs[Gem.RED],-card_costs[Gem.BLACK])

  



def card_costs_dict(card: Card, player: Player) -> dict[Gem, int]:
  resources = player.get_gems()
  return {
    Gem.WHITE: card.white_cost - resources[Gem.WHITE],
    Gem.BLUE: card.blue_cost - resources[Gem.BLUE],
    Gem.GREEN: card.green_cost - resources[Gem.GREEN],
    Gem.RED: card.red_cost - resources[Gem.RED],
    Gem.BLACK: card.black_cost - resources[Gem.BLACK]
  }

def apply_spending_turn(spending_dict, player: Player, action_category, action_object):
    # Update spending dictionary.
    spending_dict[action_object] =- 1

    # Decrease gold for player.
    if action_category == SCategory.CONSUME_GOLD:
        player.update_gems(gold=-1)
        return
    
    # Decrease gem for player.
    if action_object == Gem.WHITE:
        player.update_gems(white=-1)
    elif action_object == Gem.BLUE:
        player.update_gems(blue=-1)
    elif action_object == Gem.GREEN:
        player.update_gems(green=-1)
    elif action_object == Gem.RED:
        player.update_gems(red=-1)
    else: # Gem.BLACK.
        player.update_gems(black=-1)

    
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