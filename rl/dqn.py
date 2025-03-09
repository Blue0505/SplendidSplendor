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

"""DQN agent trained against a random agent in the "difficult" Splendor version."""

from absl import app
from absl import flags
from absl import logging
import os
import pickle
import time
import splendor_hard.splendor_game as splendor_game
import numpy as np
import tensorflow.compat.v1 as tf

from open_spiel.python import rl_environment
from open_spiel.python.algorithms import dqn
from open_spiel.python.algorithms import random_agent as ra

import splendor_hard.splendor_game as splendor_game
from rl.eval import eval_against_random_bots

FLAGS = flags.FLAGS

# Message for logging. 
flags.DEFINE_string("msg", "",
                    "Message for the top of the logging file.")

# Training parameters.
flags.DEFINE_integer(
    "save_every", int(1e4),
    "Episode frequency at which the DQN agent models are saved.")
flags.DEFINE_integer("num_train_episodes", int(5e4),
                     "Number of training episodes.")
flags.DEFINE_integer(
    "eval_every", 1000,
    "Episode frequency at which the DQN agents are evaluated.")
flags.DEFINE_integer(
    "eval_amount", 1000,
    "Episodes to use during evaluation."
)

# DQN model hyper-parameters.
flags.DEFINE_list("hidden_layers_sizes", [239, 128],
                  "Number of hidden units in the Q-Network MLP.")
flags.DEFINE_integer("replay_buffer_capacity", int(1e5),
                     "Size of the replay buffer.")
flags.DEFINE_integer("batch_size", 128, # Was 32.
                     "Number of transitions to sample at each learning step.")
flags.DEFINE_float("learning_rate", 0.001,
                     "Learning rate.")
flags.DEFINE_integer("epsilon_decay", int(1e6), "Epsilon decay.")


def main(_):
  model_save_name = os.getcwd() + "/rl/model_dqn.pkl"
  stats_save_name = os.getcwd() + "/rl/stats_dqn.pkl"

  if os.path.exists(stats_save_name):
    os.remove(stats_save_name)

  game = "splendor_hard"
  num_players = 2
  random_id = 1
  dqn_id = 0
  env = rl_environment.Environment(game)
  info_state_size = env.observation_spec()["info_state"][0]
  num_actions = env.action_spec()["num_actions"]
  random_agent = ra.RandomAgent(player_id=random_id, num_actions=num_actions)

  # Log info.
  logging.info(f"MESSAGE: {FLAGS.msg}\n")
  logging.info(f"Save every: {FLAGS.save_every}")
  logging.info(f"Evaluate every: {FLAGS.eval_every}")
  logging.info(f"Evaluate amount: {FLAGS.eval_amount}")
  logging.info(f"Epsilon decay: {FLAGS.epsilon_decay}")
  logging.info(f"Hidden layers sizes: {FLAGS.hidden_layers_sizes}")
  logging.info(f"Replay buffer capacity: {FLAGS.replay_buffer_capacity}")
  logging.info(f"Batch sizes: {FLAGS.batch_size}")
  logging.info(f"Learning rate: {FLAGS.learning_rate}")

  with tf.Session() as sess:
    hidden_layers_sizes = [int(l) for l in FLAGS.hidden_layers_sizes]
    # pylint: disable=g-complex-comprehension
    
    dqn_agent = dqn.DQN(
      session=sess,
      player_id=dqn_id,
      state_representation_size=info_state_size,
      num_actions=num_actions,
      learning_rate=FLAGS.learning_rate, 
      hidden_layers_sizes=hidden_layers_sizes,
      replay_buffer_capacity=FLAGS.replay_buffer_capacity,
      epsilon_decay_duration=FLAGS.epsilon_decay,
      batch_size=FLAGS.batch_size) 
    

    sess.run(tf.global_variables_initializer())

    agents = [ dqn_agent, random_agent ]

    for ep in range(FLAGS.num_train_episodes):
      if (ep + 1) % FLAGS.eval_every == 0:
        stats = eval_against_random_bots(env, dqn_agent, random_agent, FLAGS.eval_every, mmd=False)
        logging.info(f"Episode: {ep}")
        logging.info(f"Stats: {stats}")
        
        with open(stats_save_name, "ab") as bout:
          pickle.dump(ep, bout)
          pickle.dump(stats, bout)

      if (ep + 1) % FLAGS.save_every == 0:
          dqn_agent.save(model_save_name)

      time_step = env.reset()
      while not time_step.last():
        player_id = time_step.observations["current_player"]
        agent_output = agents[player_id].step(time_step)
        action_list = [agent_output.action]
        time_step = env.step(action_list)

      dqn_agent.step(time_step)


if __name__ == "__main__":
  app.run(main)