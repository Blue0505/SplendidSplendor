import pyspiel
import numpy as np

game = pyspiel.load_game("python_splendor")
state = game.new_initial_state()
while not state.is_terminal():
  legal_actions = state.legal_actions()
  print(legal_actions)
  action = input("Select action.")
  state.apply_action(action)