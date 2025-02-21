---
layout: default
title: Status
---

## Project Summary
Our primary goal is to create an AI agent that can play the Splendor board game. Thus far, we have coded the Splendor board game within the OpenSpiel framework. In doing so, we have immediate access to reinforcement learning algorithms including DQN and PPO. As of week 7, we have written extensive tests for the Splendor game and to our knowledge the game is in a working state. We have also run OpenSpiel's Q-learning algorithm against the game with 10,000 episodes. Our goal for the rest of the quarter is to fine tune the reward shaping and try other algorithms.

## Approach
* focus on how we created the game (file structure, etc.)
* put equations for q-learning
* how q-learning applies to the splendor game
* hyperparameters for q-learning from the docs
* reward system
* observation system

## Evaluation
* paragraph for the testing scripts that we wrote for the game itself
* plot metrics that can be archived from the open spiel environment (-> tensorboard); 1 p
* win statistics at the end of training 
* experiment with humans playing against trained agent (qualitative result)


## Remaining Goals and Challenges

* Limitation of current p
* challenge: inconsistencies in win rates
* Implement and test other algorithms
* make comparisons to other algorithms
* run for longer on hpc3
* test changing rewards shaping and hyperparameters

## Resources
- [OpenSpiel](https://github.com/google-deepmind/open_spiel)
- [Splendor Rules](https://cdn.1j1ju.com/medias/7f/91/ba-splendor-rulebook.pdf)
- [Splendor Card Info Spreadsheet](https://docs.google.com/spreadsheets/d/15ghp8rJ_vdVgxZIVJGawAYQXRMZSVHJYpZRfQUplAhE/edit?usp=sharing)
- [ChatGPT](https://chatgpt.com/)
- [Python Documentation](https://docs.python.org/3/)
