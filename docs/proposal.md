---
layout: default
title: Proposal
---

# Project Summary
We plan to create an AI agent for the board game Splendor; in particular, we will create the two person version of Splendor so that the game has the zero-sum property. Our preliminary goal is to code Splendor in Python with an interface to the OpenSpiel library. This enables experimentation with different reinforcement algorithms already implemented with OpenSpiel. Our other main goal is to experiment with and report on reward shaping. We hypothesize that reward shaping will play a significant role in the efficacy of the agent, since winning Splendor requires a resource acquisition strategy with a long horizon. By applying different reinforcement algorithms and shaping rewards, our main goal is to create a Splendor playing agent with a sufficient level of skill to be a fun opponent. 

# I/ML Algorithms
We plan to try to train an agent with the reinforcement algorithms XDO, PPO (on OpenSpiel already), and DQN (on OpenSpiel already). 

# Evaluation Plan
To evaluate the success of our Splendor agent, we will look at game performance metrics. Specifically, we will analyze win rate, score difference, and game trajectory length. Quantitative analysis will inform our comparison analysis of different algorithms. Our baseline is an AI agent that takes actions at random. Our moonshot case is an AI that can consistently beat human players. We also plan on creating a terminal interface with the game so that a human player can compete against the Splendor agent to visualize and verify the model’s effectiveness.

# AI Tools Usage
We did not use any AI tools for the creation of this proposal. 
