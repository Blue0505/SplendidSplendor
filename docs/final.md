---
 layout: default
 title: Final Report
---

## Video

## Project Summary
Splendor is a resource acquisition board game that is played with two to four players. Although we found repositories that train reinforcement learning (RL) agents against it, we did not see any use of state-of-the-art algorithms such as Magnetic Mirror Descent (MMD) nor any approaches that lent itself towards future experimentation with other algorithms. Thus, our group implemented the two player version of the Splendor board game within the OpenSpiel framework [1]. 

We built the environment from scratch using the game's manual and a spreadsheet containing the game's card information [2] [3]. We determined the RL properties of two-person Splendor and integrated them into the environment via the OpenSpiel API; specifically, our version of Splendor is imperfect information, zero-sum, no-chance, and has a discrete action space. We carefully designed the action space for Splendor to minimize its size. We built three different difficulties of Splendor ("lite", "medium", and "hard") to run against OpenSpiel's RL algorithms. In addition, we wrote extensive unit tests for the game. Lastly, we created an observation system that condensed the game's state from the its data structures into a numeric representation. 

After creating the Splendor environment, we experimented with different reinforcement learning algorithms via OpenSpiel's catalog. Our first attempt trained a Splendor playing agent with the Q-learning algorithm through self-play. Due to the large state space of Splendor, the tabular nature of Q-learning was insufficient for training a capable agent. Naturally, we pivoted to training an agent through self play with Deep Q-Learning (DQN). DQN yielded higher quality results, especially after experimentation with hyper-parameters; however, the zero-sum nature of Splendor ultimately hindered long term improvement from the agent. Consequently, we trained an agent using MMD provided by Lanctot et. al. in an OpenSpiel fork [4].

## Approaches

### Environment Setup
We created three different versions of Splendor at different difficulty versions ("lite", "medium", "hard"). The analysis of our game system corresponds to the "hard" version; we created this version first and the easier versions are derived from it. 

#### Action System
Defining an action system for Splendor was our first major hurdle. We partitioned the action space into three "turn types" to limit an exponential growth of actions. 

<img src="./actions_diagram.png" alt="Flow chart depicting different turn types of the action space for Splendor." style="
    width: 100%;
">
<a style="display: flex; justify-content: center; gap: 8px; "><b>Fig. 1</b>Splendor action space</a>

As illustrated in Fig. 1, the  `SPENDING` turn type (top right) enables a player to spend gold for a card without requiring an action for each variation. This reduces $5^5 \times 12$ actions to $12$ actions. Similarly, the `RETURN` turn type (bottom left) allows a player to return gems from their inventory without needing a special gem drawing action. This reduces $5^2 \times \big( \binom{5}{2} + \binom{5}{3} \big)$ actions to $\binom{5}{2} + \binom{5}{3}$ actions. 

#### Observation System
Building the observation system for Splendor was the next key problem that we solved. OpenSpiel requires a one dimensional tensor to be returned from the `set_from` function of the `BoardObserver` class. Depending on the algorithm, this tensor is used to represent either the game's observation state or the information state. Our implementation of Splendor is an imperfect information game since there are three "drawing" card decks hidden from the players; thus, we do not reveal these cards when representing the observation state.

First, we define a card vector, $\vec{C} = (p, \vec{t}, \vec{g})$. $p$ is the number of points associated with a card. $\vec{t}$ is a five element vector representing the one-hot encoding of the card type (e.g. $(1, 0, 0, 0, 0)$ corresponds to a white card). $\vec{g}$ is a five element vector corresponding to the costs of each gem type for the card.

Second, we define a player vector for the $i\text{'th}$ player, $p_i =  (s_i, \vec{g_i}, \vec{C_{i_0}}, \vec{C_{i_1}}, \vec{C_{i_2}})$. $s_i$ is the score/points for the $i\text{'th}$ player. $g_i$ is the gem array of the $i\text{'th}$ player, containing six entries corresponding to the gem count (including gold) of each player. $\vec{C_{i_j}}$ is the $j\text{'th}$ reserved card of the $i\text{'th}$ player; this vector is filled with zeroes if the player has no reserved card at that slot. 

Third, we define a board vector $\vec{B} = (\vec{g}, \vec{C_{00}}, \vec{C_{01}}, \vec{C_{02}}, \vec{C_{03}}, \vec{C_{10}}, \vec{C_{11}}, \vec{C_{12}}, \vec{C_{13}}, \vec{C_{20}}, \vec{C_{21}}, \vec{C_{22}}, \vec{C_{23}} )$. $\vec{g}$ is a six element vector representing the gems (including gold) on the board. Card vectors $\vec{C_{00}} \dots \vec{C_{23}}$ represent the cards on the board that the players can purchase or reserve. 

These vectors are generated on the fly using information in the data structures of the game. Specifically, these vectors are used to form the entire observation vector of the game state,

$$\text{observation} = (\vec{p_0}, \vec{p_1}, \vec{B}, \vec{C_s})$$

, where $\vec{C_s}$ is what we call the "spending card". This card appears during a `SPENDING` turn type when the player can choose to redeem gold for a specific colored gem of the card. For example, if a player spends a gold gem in place of a blue gem, this is reflected in the blue cost of $\vec{C_s}$. 

#### Rewards System
We also built a reward mechanism for the Splendor game. OpenSpiel requires a `returns` function which returns a two element vector representing the total accumulated rewards for player 0 and player 1. In our preliminary testing we experimented a lot with reward shaping. Specifically, we applied heuristics for:
* Rewarding a player when winning
* Rewarding player for having resources
* Rewarding a player for the number of points that they have
* Penalizing a player for returning gems
* Penalizing a player for not having moves

Each reward category $c$ had a different weight $\alpha_c$ and value associated with player $i$, $r_{c_i}$. We then used these weights and values to create a zero sum reward for player 0 with the function, $\sum_c \alpha_c (r_{c_0} - r_{c_1})$. After lots of experimentation with the weights, we did not observe any different on agent training. Thus, we decided to only reward a player with a point on a game win, to minimize the possible failure points in our agent training pipeline. 

### Algorithms
#### Q-Learning
As a baseline to verify that our algorithm worked, we trained a Splendor playing agent with Q-Learning. Q-Learning exploits the lower variance of an approach such as Bellman's Equations whilst not needing to calculate exponentially many trajectories like a Monte Carlo based approach. Q-learning associates a *Q-value* with state action pairs that are defined recursively in terms of future action pairs; specifically, the Q-value function is recursively defined $Q_{\pi}(s) = r(s, a) + \gamma \max_{a'}Q_{\pi}(s', a')$. The best policy $\pi$ can then be chosen at each state by choosing the action $a$ associated with the largest Q-value, that is, $\arg \max Q_a(s, a)$.

At this point in our project, our AI pipeline consisted only of capturing the number of wins each agent won against a random agent averaged over 1000 episodes.

#### Deep Q-Learning
Due to the limitations imposed by the tabular nature of Q-Learning, we pivoted to Deep Q-Learning. In contrast to Q-Learning, Deep Q-Learning estimates the Q-value function using two neural networks. There is an *online network* ($Q_\theta$) and a *target network* ($Q_{\bar{\theta}}$) which is periodically set to be equal to the online network. We enforced the epsilon greedy policy to train our agent. With probability epsilon, the agent picks a random move, and with probability 1 minus epsilon chance the agent picks the action associated with the highest estimated Q-value. As an agent explores through the states, the algorithm descends over $Q_\theta$, pushing $Q_\theta$ towards the Q-value's recursive definition using $Q_{\bar{\theta}}$. Specifically, it descends over $((r(s,a) + \gamma \max_{a'} Q_{\bar{\theta}}(s', a')) - Q_{\theta}(s, a))^2$.

At this point in our project, we implemented a more sophisticated AI pipeline. We continued to evaluate the two self-playing agents every 1000 games for 1000 games against a random agent. We also began capturing more statistics, namely:
* Mean rewards
* Standard deviation of rewards
* Average game length
* Standard deviation of game length
* Minimum reward amount
* Maximum reward amount


#### Magnetic Mirror Descent
Lastly, we used magnetic mirror descent to train our Splendor agent. 
TODO: Give a quick description
TODO: Explain how we created three different versions of Splendor for this part of the training

## Evaluation

### Q-Learning Results

<div style="display: flex; justify-content: space-between; align-items: center; max-width: 800px; margin: auto;">
    <img src="./game_length.png" alt="Image 1" style="width: 30%; height: auto;">
    <img src="./win_rates.png" alt="Image 3" style="width: 30%; height: auto;">
</div>
<a style="display: flex; justify-content: center; gap: 8px; "><b>Fig. 2</b>Average win amounts of Q-learning agents</a>

Training with Q-learning helped verify our game was working; however, Q-learning failed to train a competent agent. As shown in Fig. 2, the average game wins over 1000 games against a random agent oscillates heavily even after $5\cdot10^5$ episodes. We hypothesize this is because Q-learning is tabular; that is, the Q-value associated with each state action pair is stored. However, the state space of Splendor is massive and is unlikely to be entirely representable in computer memory. In addition, the amount of time it would take to fill Q-values for a reasonable amount of the state space would likely be too long to be realistic.

### Deep Q-Learning Results
#### Quantitative Analysis

Initially, we attempted to train the DQN agent with self-play as attempted with the Q-learning agent. The agent had better quantitative results (e.g. higher win rates); however, the results still oscillated even after two million time steps. Unsure of what was causing the lack of convergence, we experimented with the following hyper-parameters:
* **Neural network layers**: We saw some quantitative success by increasing the neural network size. Originally, there were two hidden layers with sizes 64 and 64. We increased this to 239 and 128 to ensure that each element of the observation tensor had a corresponding hidden unit in the first layer. 
* **Batch size**: We also tried increasing the batch size. We also saw minor improvements by increasing the batch size, which we think is due to a more stable gradient descent calculation when updating the online network.
 * **Learning rate**: We tried lowering the learning rate with the hope that small changes to the online network early on could lead to more stability in training; we did not notice a negligable effect on the quantiative statistics by lowering the learning rate.
* **Epsilon decay**: We also tried to decrease the rate that epsilon is lowered. We hoped that by exploring randomly for longer in the early parts of training, the agent would have a more stable policy at later timesteps. Unfortunately, we did not notice any effects on the quantitative statistics by doing so.

After speaking with our TA, [JB Lanier](https://jblanier.net/), we got more insight into why we were not converging to a stable policy. The key insight was that self-play was causing the agents to adapt to each other's strategy, but in a loop that does not lead to a net improvement overtime. Thus, we decided to try training a DQN agent solely against a random agent. 

<img src="./dqn_stats.png" alt="Statistics for DQN" style="width: 100%">
<a style="display: flex; justify-content: center; gap: 8px; "><b>Fig. 3</b>DQN agent statists</a>

As shown in Fig. 3, the DQN agent had a much more stable policy overtime when not trained with self-play. Over roughly the first 20000 episodes, the reward averages greatly increase. Similarly, the reward standard deviation, game length average, game length standard deviation, and game wins minus ties all decrease. We also observed a slight rebound in performance after 20000 episodes which we could not explain, but performance stays pretty consistent after that. 

#### Qualitative Analysis
To test the DQN agent's performance in a more practical setting, we played against it ourselves. While the DQN agent cannot win 100 percent of the time against a random agent, it performs fairly good against human players. In our first game against the agent, the agent won 16-7. In the second game, the agent lost 10-16 but was two turns away from winning. The agent is able to win or at least create close games with human players. Most importantly, we found the agent fun to play against, as it can quickly build up resources and points. While it cannot consistently win against human players, its progress is impressive.

The agent developed a clear strategy that allows it to compete with human players. Near the beginning of the game, the agent prioritizes reserving cards over any other actions. It reserves low level cards that have a low cost but do not contribute much to the point score. It purchases many low level cards to gain a resource advantage. This differs from our strategies in two-player games, which generally skip the lowest level of cards in favor of getting points earlier. When it comes to higher level cards, it prefers to purchase them directly from the board instead of reserving them. It also seems to take into account which gems the other player is gathering for reserved cards, taking those gems from the board. While not perfect, the agent has developed clear strategies that make playing against it interesting.

### Magnetic Mirror Descent Results

#### Quantitative Results

<img src="./mmd_stats.png" alt="MMD statistics for the three different difficulty levels of Splendor" style="width: 100%">

<a style="display: flex; justify-content: center; gap: 8px; "><b>Fig. 4</b>Statistics for the MMD agents</a>

Training MMD yielded the most exciting and consistent results of our project. All our metrics appear to vary mostly monotonically, even after 10,000,000 time steps. Notably, the reward averages and win rates increase faster for the "easy" version of the game; this is expected since the average horizon is significantly shorter than the other two versions. Since our agent continues to improve after 10,000,000 time steps, we likely need better computational resources and a compiled version of Splendor to achieve an AI with super human play. 

#### Qualitative Results


## References
[[1] OpenSpiel](https://github.com/google-deepmind/open_spiel): We prototyped the Splendor game by modifying the `open_spiel/python/games/kuhn_poker.py` file. We made use of the DQN and Q-Learning algorithms provided within OpenSpiel. We also used and modified the `open_spiel/python/examples/tic_tac_toe_qlearner.py` to run Q-learning and DQN learning which we modified `open_spiel/python/examples/breakthrough_dqn.py` and ran against our Splendor implementation. 

[[2] Splendor Rules](https://cdn.1j1ju.com/medias/7f/91/ba-splendor-rulebook.pdf): We used the official rules to inform our action system for the Splendor game. 

[[3] Splendor Card Info Spreadsheet](https://docs.google.com/spreadsheets/d/15ghp8rJ_vdVgxZIVJGawAYQXRMZSVHJYpZRfQUplAhE/edit?usp=sharing): We used this spreadsheet to
initialize the metadata of the card decks to start each Splendor game. 

[[4] OpenSpiel MMD Algorithm](https://github.com/nathanlct/IIG-RL-Benchmark/blob/main/algorithms/mmd/mmd.py) We used a custom multi-agent implementation of MMD provided by Lancetot et. al. designed for use in OpenSpiel. 

[[5] Magnetic Mirror Descent](https://arxiv.org/abs/2206.05825)

## AI Tool Usage
We used ChatGPT for minor debugging purposes and various one-liners relating to libraries
we used such as NumPy and PyPlot. We did not use AI tools to generate a significant blocks of code for our project. 