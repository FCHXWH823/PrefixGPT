import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os

if not os.path.exists('./Figures'):
    os.makedirs("./Figures")

# Define the SPCR content
spcr_text = """
0: connectedNodes=(None, None), range=[0:0], left_bound=0, right_bound=0.
1: connectedNodes=(None, None), range=[1:1], left_bound=1, right_bound=1.
2: connectedNodes=(None, None), range=[2:2], left_bound=2, right_bound=2.
3: connectedNodes=(None, None), range=[3:3], left_bound=3, right_bound=3.
4: connectedNodes=(0, 1), range=[0:1], left_bound=0, right_bound=1.
5: connectedNodes=(2, 3), range=[2:3], left_bound=2, right_bound=3.
6: connectedNodes=(4, 5), range=[0:3], left_bound=0, right_bound=3.
"""

# Create a figure and axis
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Add a rounded rectangle
rect = FancyBboxPatch((1, 1), 8, 8, boxstyle="round,pad=0.2,rounding_size=0.2", edgecolor="black", facecolor="lightblue")
ax.add_patch(rect)

# Add the SPCR text
ax.text(1.5, 8.5, spcr_text, fontsize=10, verticalalignment='top', family='monospace', color='black')

# Show the plot
plt.savefig('./Figures/SPCR.png')
# plt.show()
