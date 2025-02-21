---
layout: default
title: Status
---

## Project Summary
Our primary goal is to create an reinforcement learning (RL) trained agent that can play the Splendor board game. Thus far, we have coded the Splendor board game within the OpenSpiel framework. In doing so, we have immediate access to reinforcement learning algorithms including DQN and PPO. As of week 7, we have written extensive tests for the Splendor game and to our knowledge the game is in a working state. We have also run OpenSpiel's Q-learning algorithm against the game with 10,000 episodes. Our goal for the rest of the quarter is to fine tune the reward shaping and try other algorithms.

## Approach

### Summary
We built Splendor from scratch within the OpenSpiel environment. Crucially, we had to decide on an observation system, action system, and rewards system.
After implementing the game and these systems, we tested them against OpenSpiel's Q-learning algorithm.

### Action System
Defining an action system for Splendor was our first major hurdle. Although the action space is discrete we had to partition the action space into different "turn types"
to limit an exponential growth of discrete actions. 

<img src="./actions_diagram.png" alt="Flow chart depicting different turn types of the action space for Splendor." style="
    width: 100%;
">

As denoted in the diagram with the dotted rectangular regions, the three turn types are `NORMAL`, `SPENDING`, and `RETURN`. The `SPENDING` turn type enables
a player to use gold to purchase a card without needing an action for every variation. This reduces $5^5 \times 12$ actions to $12$ actions. Simiarly, the `RETURN` type 
allows a player to take two or three gems and return gems from their inventory if they exceed 10 gems without needing an action for every variation. This reduces $5^2 \times \binom{5}{2} + \binom{5}{3}$
actions to $\binom{5}{2} + \binom{5}{3}$ actions. 


### Observation System
Building the observation system for Splendor was a key problem that we solved. 
OpenSpiel requires a one dimensional tensor to be returned from the `set_from` function of the `BoardObserver` class. This tensor
represents an observation of the game state that is fed as input to the RL algorithms in OpenSpiel. Note that Splendor is an imperfect information game,
since there are three "upside-down" decks that both the board and the player draw from. Note also that both players observe identical information at all times, 
simplifying the creation of the observation tensor.

First, we define a card vector, $\vec{C} = (p, \vec{t}, \vec{g})$. $p$ is the number of points associated with a card. $\vec{t}$ is a five element 
vector representing the one-hot encoding of the card type (e.g. $(1, 0, 0, 0, 0)$ corresponds to a white card). $\vec{g}$ is a five
element vector corresponding to the costs of each gem type for the card.

Second, we define a player vector for the $i\text{'th}$ player, $p_i =  (s_i, \vec{g_i}, \vec{C_{i_0}}, \vec{C_{i_1}}, \vec{C_{i_2}})$. $s_i$ is the score/points for the $i\text{'th}$ player.
$g_i$ is the gem array of the $i\text{'th}$ player, containing six entries corresponding to the gem count (including gold) of each player. $\vec{C_{i_j}}$ is the 
$j\text{'th}$ reserved card of the $i\text{'th}$ player; this vector is filled with zeroes if the player has no reserved card at that slot. 

Third, we define a board vector $\vec{B} = (\vec{g}, \vec{C_{00}}, \vec{C_{01}}, \vec{C_{02}}, \vec{C_{03}}, \vec{C_{10}}, \vec{C_{11}}, \vec{C_{12}}, \vec{C_{13}}, \vec{C_{20}}, \vec{C_{21}}, \vec{C_{22}}, \vec{C_{23}} )$. $\vec{g}$ is a six element vector representing the gems (including gold) on the board. Card vectors 
$\vec{C_{00}} \dots \vec{C_{23}}$ represent the cards on the board that the players can purchase or reserve. 

These vectors are generated on the fly using information in the data structures of the game. Specifically, these vectors are used to form the entire observation vector of the game state,

$$\text{observation} = (\vec{p_0}, \vec{p_1}, \vec{B}, \vec{C_s})$$

, where $\vec{C_s}$ is what we call the "spending card". This card appears during a `SPENDING` turn type when the
player can choose to redeem gold for a specific colored gem of the card. For example, if a player spends a 
gold gem in place of a blue gem, this is reflected in the blue cost of $\vec{C_s}$. 


### Rewards System
We also built a reward mechanism for the Splendor game. OpenSpiel requires a `returns` function which returns a two element vector representing the total accumulated rewards
for player 0 and player 1. Note that the two person variation of Splendor is a zero sum game, so we can calculate the rewards of player 1 as 
the opposite of player 0's rewards. 

First, we define $w_i$ to be 0 if player $i$ has not won, otherwise 1. Second, we define $s_i$ to be the total points of player $i$. Third,
we define $r_i$ to be the total amount of resources of player $i$. We use these values to calculate the accumulated reward of player 0 with the function, 

$$\text{player 0 returns} = \alpha(w_0 - w_1) + \beta(s_0 - s_1) + \gamma(r_0 - r_1)$$

, with $\alpha = 1000$, $\beta = 3$, and $\gamma = 1.5$. We plan to experiment with the values of $\alpha, \beta, \gamma$. Time permitted, we also want to make $\gamma$ and $\beta$
functions of the number of time steps in the game. Specifically, we want to try increasing $\beta$ and lowering $\gamma$ as the time steps increases. Our hope is that this matches
to the strategy in Splendor of focusing on resource acquisition in the early game, then trying to get points with the resources you've aquired in the later stages of the game. 




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
