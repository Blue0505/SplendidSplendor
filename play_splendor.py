import pyspiel
import pickle
import splendor_game
import time
from splendor.actions import SAction

game = pyspiel.load_game("python_splendor", {"shuffle_cards": False})
state = game.new_initial_state()
cur_time = time.time()
info_fn = f"tests/playouts/{cur_time}_info.pkl"

while not state.is_terminal():
    print(state)
    legal_actions = state.legal_actions()
    tensor = state.observation_tensor()
    
    for action in state.legal_actions():
        print(f"{action} - {SAction(action).name}")

    action = int(input("Select action."))
    if action not in legal_actions:
        raise SystemExit(f"Illegal action: {action}")

    with open(info_fn, "ab") as info:
        pickle.dump(action, info)
        pickle.dump(legal_actions, info)
        pickle.dump(tensor, info)

    state.apply_action(action)
    
def getActionName(action) -> str:
    pass
