import matplotlib.pyplot as plt
import numpy as np

# Data
circuits = ["BK", "PrefixLLM8_4", "PrefixLLM8_5", "PrefixLLM8_6", "PrefixLLM8_7", "PrefixLLM8_8", "KS", "ML8_4", "ML8_5", "ML8_6", "ML8_7", "ML8_8", "SK"]
areas = [70.756, 65.968, 60.648, 57.988, 55.328, 52.668, 79.268, 71.288, 60.648, 57.988, 55.328, 52.668, 65.968]
delays = [0.41, 0.38, 0.44, 0.51, 0.51, 0.57, 0.38, 0.37, 0.44, 0.51, 0.51, 0.57, 0.38]

# Add jitter to overlapping points
jitter = 0.005
jittered_areas = np.array(areas) + np.random.uniform(-jitter, jitter, len(areas))
jittered_delays = np.array(delays) + np.random.uniform(-jitter, jitter, len(delays))

# Assign colors for each group
label_colors = {
    "PrefixLLM": "blue",
    "ML": "green",
    "BK": "red",
    "KS": "purple",
    "SK": "orange"
}

# Scatter plot with jitter
plt.figure(figsize=(10, 6))
for label, color in label_colors.items():
    x = [jittered_areas[i] for i in range(len(circuits)) if circuits[i].startswith(label)]
    y = [jittered_delays[i] for i in range(len(circuits)) if circuits[i].startswith(label)]
    plt.scatter(x, y, color=color, label=label, s=100, edgecolors='k')

# Adding axis labels with units
plt.title("Scatter Plot of Area vs. Delay (With Jitter)", fontsize=14)
plt.xlabel("Area (µm²)", fontsize=12)
plt.ylabel("Delay (ns)", fontsize=12)
plt.grid(True)

# Add legend
plt.legend(title="Circuit Types", fontsize=10, loc="best")

# Display the plot
plt.show()
