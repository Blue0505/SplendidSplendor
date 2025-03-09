import numpy as np

def eval_against_random_bots(env, trained_agent, random_agent, num_episodes, mmd=False) -> None:
    """Evaluates `trained_agent` against `random_agent` for `num_episodes`."""

    total_episode_rewards = []
    game_lengths = []
    game_wins = 0
    game_ties = 0

    agents = [trained_agent, random_agent]
    for _ in range(num_episodes):
      game_length = 0
      time_step = env.reset()
      episode_rewards = 0
      while not time_step.last():
        game_length += 1
        player_id = time_step.observations["current_player"]
        if player_id == 0 and mmd:
            agent_output = agents[player_id].step([time_step], is_evaluation=True)
            action_list = [agent_output[0].action]
        
        else: 
            agent_output = agents[player_id].step(time_step, is_evaluation=True)
            action_list = [agent_output.action]
    
   
        time_step = env.step(action_list)
        episode_rewards += time_step.rewards[0]

      if time_step.rewards[0] > 0: 
        game_wins += 1
      elif time_step.rewards == [0, 0]:
        game_ties += 1
      total_episode_rewards.append(episode_rewards)
      game_lengths.append(game_length)
    
    stats = {}

    stats["rewards_avg"] = sum(total_episode_rewards) / num_episodes
    stats["rewards_std"] = float(np.std(total_episode_rewards))
    stats["rewards_max"] = float(np.max(total_episode_rewards))
    stats["rewards_min"] = float(np.min(total_episode_rewards))
    stats["game_length_avg"] = sum(game_lengths) / num_episodes
    stats["game_length_std"] = float(np.std(game_lengths))
    stats["game_wins"] = game_wins
    stats["game_ties"] = game_ties
    
    return stats