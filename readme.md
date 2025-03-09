This is a monorepo containing three implementations of two person Splendor at different difficulty levels in Python. 

# Installation
1. Install Python 3.11
2. `python -m venv .venv`
3. `source .venv/bin/activate`
4. `pip install openspiel`
5. `pip install -r requirements.txt`


# RL Training
* DQN
    - Run `python -m rl.dqn.py`

* MMD
    - Hard: Run `python -m rl.mmd game=splendor_hard`
    - Medium: Run `python -m rl.mmd game=splendor_medium`
    - Lite: Run `python -m rl.mmd game=splendor_lite`

# Testing
There are unit tests for the "hard" version of Splendor, which the other three were based after. To run them,
execute `python -m unittest discover -s tests -p "*.py"`. 
