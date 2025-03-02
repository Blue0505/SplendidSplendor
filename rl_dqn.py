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

"""DQN agents trained on Breakthrough by independent Q-learning."""

from absl import app
from absl import flags
from absl import logging
import pickle
import time
import splendor_game
import numpy as np
import tensorflow.compat.v1 as tf

from open_spiel.python import rl_environment
from open_spiel.python.algorithms import dqn
from open_spiel.python.algorithms import random_agent
import splendor_game

FLAGS = flags.FLAGS

# Training parameters
flags.DEFINE_string("checkpoint_dir", "/tmp/dqn_test",
                    "Directory to save/load the agent models.")
flags.DEFINE_integer(
    "save_every", int(1e4),
    "Episode frequency at which the DQN agent models are saved.")
flags.DEFINE_integer("num_train_episodes", int(1e6),
                     "Number of training episodes.")
flags.DEFINE_integer(
    "eval_every", 1000,
    "Episode frequency at which the DQN agents are evaluated.")
flags.DEFINE_integer(
    "eval_amount", 1000,
    "Episodes to use during evaluation."
)

# DQN model hyper-parameters
flags.DEFINE_list("hidden_layers_sizes", [64, 64],
                  "Number of hidden units in the Q-Network MLP.")
flags.DEFINE_integer("replay_buffer_capacity", int(1e5),
                     "Size of the replay buffer.")
flags.DEFINE_integer("batch_size", 32,
                     "Number of transitions to sample at each learning step.")
flags.DEFINE_float("learning_rate", 0.01,
                     "Learning rate.")


def eval_against_random_bots(env, trained_agents, random_agents, num_episodes):
  """Evaluates `trained_agents` against `random_agents` for `num_episodes`."""
  num_players = len(trained_agents)
  total_episode_rewards = [[], []]
  game_lengths = [[], []]
  game_wins = [0, 0]

  for player_pos in range(num_players):
    cur_agents = random_agents[:]
    cur_agents[player_pos] = trained_agents[player_pos]
    for _ in range(num_episodes):
      game_length = 0
      time_step = env.reset()
      episode_rewards = 0
      while not time_step.last():
        game_length += 1
        player_id = time_step.observations["current_player"]
        if env.is_turn_based:
          agent_output = cur_agents[player_id].step(
              time_step, is_evaluation=True)
          action_list = [agent_output.action]
        else:
          agents_output = [
              agent.step(time_step, is_evaluation=True) for agent in cur_agents
          ]
          action_list = [agent_output.action for agent_output in agents_output]
        time_step = env.step(action_list)
        episode_rewards += time_step.rewards[player_pos]
      if time_step.rewards[player_pos] > 0:
        game_wins[player_pos] += 1
      total_episode_rewards[player_pos].append(episode_rewards)
      game_lengths[player_pos].append(game_length)
    
  stats = {}
  for pos in range(num_players):
    stats[f"p{pos}_rewards_avg"] = sum(total_episode_rewards[pos]) / num_episodes
    stats[f"p{pos}_rewards_std"] = float(np.std(total_episode_rewards[pos]))
    stats[f"p{pos}_rewards_max"] = float(np.max(total_episode_rewards[pos]))
    stats[f"p{pos}_rewards_min"] = float(np.min(total_episode_rewards[pos]))
    stats[f"p{pos}_game_length_avg"] = sum(game_lengths[pos]) / num_episodes
    stats[f"p{pos}_game_length_std"] = float(np.std(game_lengths[pos]))
    stats[f"p{pos}_game_wins"] = game_wins[pos]
  return stats



def main(_):
  logging.get_absl_handler().python_handler.use_absl_log_file(log_dir='./logs')

  game = "python_splendor"
  num_players = 2

  env = rl_environment.Environment(game)
  info_state_size = env.observation_spec()["info_state"][0]
  num_actions = env.action_spec()["num_actions"]

  # random agents for evaluation
  random_agents = [
      random_agent.RandomAgent(player_id=idx, num_actions=num_actions)
      for idx in range(num_players)
  ]

  # Log hyperparameters.
  logging.info(f"Checkpoint directory: {FLAGS.checkpoint_dir}")
  logging.info(f"Save every: {FLAGS.save_every}")
  logging.info(f"Evaluate every: {FLAGS.eval_every}")
  logging.info(f"Evaluate amount: {FLAGS.eval_amount}")
  logging.info(f"Hidden layers sizes: {FLAGS.hidden_layers_sizes}")
  logging.info(f"Replay buffer capacity: {FLAGS.replay_buffer_capacity}")
  logging.info(f"Batch sizses: {FLAGS.batch_size}")
  logging.info(f"Learning rate: {FLAGS.learning_rate}")

  with tf.Session() as sess:
    hidden_layers_sizes = [int(l) for l in FLAGS.hidden_layers_sizes]
    # pylint: disable=g-complex-comprehension
    agents = [
        dqn.DQN(
            session=sess,
            player_id=idx,
            state_representation_size=info_state_size,
            num_actions=num_actions,
            learning_rate=FLAGS.learning_rate, 
            hidden_layers_sizes=hidden_layers_sizes,
            replay_buffer_capacity=FLAGS.replay_buffer_capacity,
            batch_size=FLAGS.batch_size) for idx in range(num_players)
    ]
    sess.run(tf.global_variables_initializer())

    for ep in range(FLAGS.num_train_episodes):
      if (ep + 1) % FLAGS.eval_every == 0:
        stats = eval_against_random_bots(env, agents, random_agents, FLAGS.eval_amount)
        logging.info(f"Episode: {ep}")
        logging.info(f"Stats: {stats}")
        if logging.get_log_file_name() != "":
          fname = logging.get_log_file_name() + ".pkl"
          with open(fname, "ab") as bout:
            pickle.dump(ep, bout)
            pickle.dump(stats, bout)

      if (ep + 1) % FLAGS.save_every == 0:
        for agent in agents:
          agent.save(FLAGS.checkpoint_dir)

      time_step = env.reset()
      while not time_step.last():
        player_id = time_step.observations["current_player"]
        if env.is_turn_based:
          agent_output = agents[player_id].step(time_step)
          action_list = [agent_output.action]
        else:
          agents_output = [agent.step(time_step) for agent in agents]
          action_list = [agent_output.action for agent_output in agents_output]
        time_step = env.step(action_list)

      # Episode is over, step all agents with final info state.
      for agent in agents:
        agent.step(time_step)


if __name__ == "__main__":
  app.run(main)