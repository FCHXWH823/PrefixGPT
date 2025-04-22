import matplotlib.pyplot as plt
import numpy as np
# Data
circuits = ["Brent-Kung8", "BasicPrefixLLM-o1-mini8_4", "BasicPrefixLLM-o1-mini8_5", "BasicPrefixLLM-o1-mini8_6", "BasicPrefixLLM-o1-mini8_7", "BasicPrefixLLM-o1-mini8_8", "Kogge-Stone8", "[11]8_4", "[11]8_5", "[11]8_6", "[11]8_7", "[11]8_8", "SK8"]
areas = [54.26,
56.39,
51.6,
49.48,
47.35,
45.22,
70.22,
62.24,
51.6,
49.48,
47.35,
45.22,
56.39
]
delays = [0.43,
0.36,
0.43,
0.49,
0.52,
0.58,
0.36,
0.36,
0.43,
0.49,
0.52,
0.58,
0.36
]

plt.rcParams.update({
    "font.family": "Times New Roman",  # Try "Times" or "Times New Roman"
    "font.size": 12
})

# Add jitter to overlapping points
jitter = 0.005

jittered_areas = np.array(areas) + np.random.uniform(-jitter, jitter, len(areas))
jittered_delays = np.array(delays) + np.random.uniform(-jitter, jitter, len(delays))

# Assign colors for each group
label_colors = {
    "BasicPrefixLLM-o1-mini": "blue",
    "[11]": "green",
    "Brent-Kung": "red",
    "Kogge-Stone": "purple",
    "Sklansky": "orange"
}

shapes = {
    "BasicPrefixLLM-o1-mini": "o",  # Circle
    "[11]": "s",         # Square
    "Brent-Kung": "^",         # Triangle
    "Kogge-Stone": "D",         # Diamond
    "Sklansky": "P"          # Pentagon
}

plt.rcParams["font.family"] = "Times New Roman"
# Scatter plot with jitter and shapes
plt.figure(figsize=(10, 6))
for label, color in label_colors.items():
    x = [jittered_areas[i] for i in range(len(circuits)) if circuits[i].startswith(label)]
    y = [jittered_delays[i] for i in range(len(circuits)) if circuits[i].startswith(label)]
    plt.scatter(
        x, y, color=color, label=label, s=100, edgecolors='k'
    )

# Adding axis labels with units
plt.title("Scatter Plot of Area vs. Delay (With Jitter)", fontsize=14)
plt.xlabel("Area (µm²)", fontsize=12)
plt.ylabel("Delay (ns)", fontsize=12)
# plt.grid(True)

# Add legend
plt.legend(title="Circuit Types", fontsize=10, loc="best")
plt.show()
plt.savefig('8bit.png')
