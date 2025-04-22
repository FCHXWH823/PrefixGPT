import matplotlib.pyplot as plt
import numpy as np
# Data
circuits = ["Brent-Kung16", "BasicPrefixLLM-o1-mini16_5", "BasicPrefixLLM-o1-mini16_6", "BasicPrefixLLM-o1-mini16_7", "BasicPrefixLLM-o1-mini16_8", "BasicPrefixLLM-o1-mini16_8", "Kogge-Stone16", "[11]16_5", "[11]16_6", "[11]16_7", "[11]16_8", "[11]16_9", "SK16"]
areas = [137.256,
129.28,
122.36,
112.78,
110.66,
108.53,
178.75,
160.13,
113.85,
111.72,
109.59,
107.46,
131.4
]
delays = [0.6,
0.46,
0.52,
0.58,
0.64,
0.7,
0.44,
0.44,
0.52,
0.56,
0.62,
0.7,
0.46
]

plt.rcParams.update({
    "font.family": "Times New Roman",  # Try "Times" or "Times New Roman"
    "font.size": 12
})

# Add jitter to overlapping points
jitter = 0.005
jittered_areas = np.array(areas) 
jittered_delays = np.array(delays)

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
plt.savefig('16bit.png')
