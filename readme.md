This is a monorepo containing three implementations of two person Splendor at different difficulty levels in Python. 

# Installation
1. Install Python 3.11
2. `python -m venv .venv`
3. `source .venv/bin/activate`
4. `pip install https://github.com/nathanlct/open_spiel/releases/download/v1.pttt/open_spiel-1.5-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl`
5. `pip install -r requirements.txt`


# RL Training
* DQN
    - Run `python -m rl.rl_dqn.py`
    - Model is saved to `rl/model_dqn.pkl`
    - Stats file is saved to `rl/stats_dqn.pkl`

* MMD
    - 

# Testing
There are unit tests for the "difficult" version of Splendor, which the other three were based after. To run them,
execute `python -m unittest discover -s tests -p "*.py"`. 
