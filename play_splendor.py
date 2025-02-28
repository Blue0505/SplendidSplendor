import pyspiel
import pickle
import splendor_game
import time
import splendor.ansi_escape_codes as ansi
from splendor.actions import SAction
from open_spiel.python.observation import make_observation

def get_action_name(action) -> str:
    action_name: str = SAction(action).name

    action_type: str = ""
    action_details: str = ""

    if action_name.startswith("PURCHASE_RESERVE"):
        action_type = "Purchase reserve"
        action_details = f"({action_name[-1]})"
    elif action_name.startswith("RESERVE"):
        action_type = "Reserve"
        action_details = f"({action_name[-2:]})"
    elif action_name.startswith("PURCHASE"):
        action_type = "Purchase"
        action_details = f"({action_name[-2:]})"
    elif action_name.startswith("TAKE3"):
        action_type = "Take3"
        action_details = (
            f"({ansi.WHITE}{action_name[-5]}"
            f"{ansi.BLUE}{action_name[-4]}"
            f"{ansi.GREEN}{action_name[-3]}"
            f"{ansi.RED}{action_name[-2]}"
            f"{ansi.GRAY}{action_name[-1]}{ansi.RESET})"
        )
    elif action_name.startswith("TAKE2"):
        action_type = "Take2"
        match action_name[-1]:
            case "0":
                action_details = f"{ansi.WHITE}white"
            case "1":
                action_details = f"{ansi.BLUE}blue"
            case "2":
                action_details = f"{ansi.GREEN}green"
            case "3":
                action_details = f"{ansi.RED}red"
            case "4":
                action_details = f"{ansi.GRAY}black"
    elif action_name.startswith("RETURN"):
        action_type = "Return"
        match action_name[7:]:
            case "0":
                action_details = f"{ansi.WHITE}white"
            case "1":
                action_details = f"{ansi.BLUE}blue"
            case "2":
                action_details = f"{ansi.GREEN}green"
            case "3":
                action_details = f"{ansi.RED}red"
            case "4":
                action_details = f"{ansi.GRAY}black"
            case "GOLD":
                action_details = f"{ansi.YELLOW}gold"
            
    elif action_name.startswith("CONSUME_GOLD"):
        action_type = f"Consume {ansi.YELLOW}gold{ansi.RESET}"
        match action_name[13:]:
            case "WHITE":
                action_details = f"as {ansi.WHITE}white"
            case "BLUE":
                action_details = f"as {ansi.BLUE}blue"
            case "GREEN":
                action_details = f"as {ansi.GREEN}green"
            case "RED":
                action_details = f"as {ansi.RED}red"
            case "BLACK":
                action_details = f"as {ansi.GRAY}black"
    elif action_name.startswith("END_SPENDING_TURN"):
        action_type = "End spending turn"
    else:
        action_type = "INVALID ACTION"

    
    return f"{action:>2}: {action_type} {action_details}{ansi.RESET}"

game = pyspiel.load_game("python_splendor", {"shuffle_cards": True})
state = game.new_initial_state()
obs = make_observation(game)

while not state.is_terminal():
    print(state)
    legal_actions = state.legal_actions()
    obs.set_from(state,0) #type: ignore
    tensor = obs.tensor #type: ignore
    for action in state.legal_actions():
        print(get_action_name(action))

    action = -1
    while action not in legal_actions:
        try: 
            action = int(input("Select action."))
        except Exception as e:
            print(f"Retry: input was not an action.")
            continue

        if action not in legal_actions:
            print(f"Retry: {action} is not a legal action.")

    state.apply_action(action)

