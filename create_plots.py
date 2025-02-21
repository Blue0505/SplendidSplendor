import numpy as np
import matplotlib.pyplot as plt
import pickle
import seaborn as sns

sns.set(style="whitegrid")

# Load input array. 
with open("qlearning_stats.pkl", "rb") as fin:
    a = pickle.load(fin)
a = np.array(a)
x = np.linspace(0, 99, 100)

# Plot win rates. 
p0_winrates = a[:, 1]
p1_winrates = a[:, 2]
plt.plot(x, p0_winrates, label='Player 0 winrates', color='blue')
plt.plot(x, p1_winrates, label='Player 1 winrates', color='red')
plt.title('Win rates')
plt.xlabel('Episodes (5e4 scale)')
plt.ylabel('Win rate %')
plt.legend(loc='upper left')
plt.savefig('win_rates.png', dpi=300, bbox_inches='tight')  # Save as PNG
plt.close()

# Plot game length.
p0_gamelength = a[:, 3]
p1_gamelength = a[:, 4]
plt.plot(x, p0_gamelength, label='Player 0 gamelength', color='blue')
plt.plot(x, p1_gamelength, label='Player 1 gamelength', color='red')
plt.title('Average game length')
plt.xlabel('Episodes (5e4 scale)')
plt.ylabel('Average game length')
plt.legend(loc='upper left')
plt.savefig('game_length.png', dpi=300, bbox_inches='tight')  # Save as PNG
plt.close()

# Losses. 
p0_loss = a[:, 5]
p1_loss = a[:, 6]
plt.plot(x, p0_loss, label='Player 0 loss', color='blue')
plt.plot(x, p1_loss, label='Player 1 loss', color='red')
plt.title('Loss')
plt.xlabel('Episodes (5e4 scale)')
plt.ylabel('Loss')
plt.legend(loc='upper left')
plt.savefig('game_loss.png', dpi=300, bbox_inches='tight')  # Save as PNG
plt.close()

# TODO: Plot average rewards.