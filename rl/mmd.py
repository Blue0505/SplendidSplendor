import pyspiel
from rl.algorithms.mmd.run_mmd import RunMMD
import hydra 
import numpy as np
import torch
import random
from omegaconf import OmegaConf, DictConfig
import os

from splendor_medium import splendor_game
from splendor_hard import splendor_game

"""Train an MMD agent."""

def set_seed(seed):
    # set the random seed for torch, numpy, and python
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
    np.random.seed(seed)
    random.seed(seed)

@hydra.main(version_base=None, config_path="configs", config_name="experiment")
def main(cfg: DictConfig):
    print(os.getcwd())
    set_seed(cfg.seed)
    game = pyspiel.load_game(cfg.game)
    runner = RunMMD(cfg, game, expl_callback=False)
    runner.run()

if __name__ == "__main__":
    main()