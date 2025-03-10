import pyspiel
import argparse
import pickle
from open_spiel.python.observation import make_observation
from open_spiel.python.algorithms import dqn
from rl.algorithms.mmd.mmd import MMD 
import tensorflow.compat.v1 as tf
from open_spiel.python import rl_environment
from open_spiel.python.algorithms import random_agent as ha
import os 
import sys

import splendor_hard.splendor_game, splendor_medium.splendor_game, splendor_lite.splendor_game
from splendor_hard.actions import SAction as h_SAction
from splendor_medium.actions import SAction as m_SAction
from splendor_lite.actions import SAction as l_SAction
import splendor_hard.ansi_escape_codes as ansi

_DEBUG = False

def command_line_action(time_step, game_string):
    """Gets a valid action from the user on the command line."""
    current_player = time_step.observations["current_player"]
    legal_actions = time_step.observations["legal_actions"][current_player]
    action = -1
    while action not in legal_actions:
        for action in legal_actions:
            print(get_action_name(action, game_string))
        sys.stdout.flush()
        action_str = input()
        try:
            action = int(action_str)
        except ValueError:
            continue
    return action

def get_action_name(action, game_string) -> str:
    """Turns a numeric action id into a pretty string with text."""
    if game_string == "splendor_hard":
        action_name: str = h_SAction(action).name
    elif game_string == "splendor_medium":
        action_name: str = m_SAction(action).name
    else:
        action_name: str = l_SAction(action).name

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
            
    elif action_name.startswith("END_SPENDING_TURN"):
        action_type = "End spending turn"
    else:
        action_type = action_name
        # action_type = "INVALID ACTION"

    
    return f"{action:>2}: {action_type} {action_details}{ansi.RESET}"


def main():

    parser = argparse.ArgumentParser()

    AGENTS = ["dqn", "mmd"]
    parser.add_argument('--game_string', type=str, required=True)
    parser.add_argument('--agent', type=str, required=False)

    args = parser.parse_args()

    game = pyspiel.load_game(args.game_string)
    env = rl_environment.Environment(game)


    if args.agent is not None:
        if args.agent == "dqn":
            # Temporary DQN initializer using the same hyper-parameters in our last training.
            sess = tf.Session()
            agent = dqn.DQN(
                session=sess,
                player_id=0,
                state_representation_size=game.observation_tensor_size(), 
                num_actions=game.num_distinct_actions(), 
                learning_rate=0.001, 
                hidden_layers_sizes=[239, 128],
                replay_buffer_capacity=100000,
                epsilon_decay_duration=1e6,
                batch_size=128
            )
            checkpoint_dir = os.getcwd() + "/rl/runs/model_dqn"
            print(checkpoint_dir)
            agent.restore(os.getcwd() + "/rl/runs/model_dqn")
    elif args.agent == "mmd": pass
        # agent = MMD
        # TODO!
    else: 
        raise SystemExit(f"Agent {args.agent} does not exist.")
    
    human_agent = ha.RandomAgent(player_id=1, num_actions=game.num_distinct_actions())
    agents = [agent, human_agent]

    human_player = 1

    time_step = env.reset()
    while not time_step.last():
        print(env._state)
        player_id = time_step.observations["current_player"]
        if player_id == human_player:
            agent_out = agents[human_player].step(time_step, is_evaluation=True)
            action = command_line_action(time_step, args.game_string)
        else:
            agent_out = agents[1 - human_player].step(time_step, is_evaluation=True)
            action = agent_out.action
        time_step = env.step([action])

        # logging.info("\n%s", pretty_board(time_step))

        # logging.info("End of game!")
        # if time_step.rewards[human_player] > 0:
        #     logging.info("You win")
        # elif time_step.rewards[human_player] < 0:
        #     logging.info("You lose")
        # else:
        #     logging.info("Draw")
        # Switch order of players
        # human_player = 1 - human_player

if __name__ == '__main__':
    main()
