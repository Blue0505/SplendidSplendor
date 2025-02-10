import pyspiel
import splendor_game
from splendor.actions import SAction

game = pyspiel.load_game("python_splendor", {"shuffle_cards": False})
state = game.new_initial_state()
while not state.is_terminal():
  print(state)
  legal_actions = state.legal_actions()
  for action in state.legal_actions():
    print(f"{action} - {SAction(action).name}")
  action = int(input("Select action."))
  state.apply_action(action)