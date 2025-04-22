import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MaxNLocator
# Data from the table (parsed manually)
data_8 = {
    "Delay": [4, 5, 6, 7, 8],
    "Sklansky": [20, None, None, None, None],
    "KoggeStone": [25, None, None, None, None],
    "BrentKung": [None, 19, None, None, None],
    "[11]": [22, 18, 17, 16, 15],
    "BasicPrefixLLM-o1-mini": [20, 18, 17, 16, 15],
    "BasicPrefixLLM-DeepSeek": [23, 21, 21, 21, 21],
    "EnhancedPrefixLLM-DeepSeek": [20, 18, 17, 16, 15]
}

data_16 = {
    "Delay": [5, 6, 7, 8, 9],
    "Sklansky": [48, None, None, None, None],
    "KoggeStone": [65, None, None, None, None],
    "BrentKung": [None, None, 42, None, None],
    "[11]": [58, 41, 40, 39, 38],
    "BasicPrefixLLM-o1-mini": [47, 44, 40, 39, 38],
    "BasicPrefixLLM-DeepSeek": [65, 57, 57, 65, 45],
    "EnhancedPrefixLLM-DeepSeek": [47, 41, 40, 39, 38]
}

data_32 = {
    "Delay": [6, 7, 8, 9, 10],
    "Sklansky": [112, None, None, None, None],
    "KoggeStone": [161, None, None, None, None],
    "BrentKung": [None, None, None, 89, None],
    "[11]": [146, 90, 87, 86, 85],
    "BasicPrefixLLM-DeepSeek": [161, 161, 161, 161, 161],
    "EnhancedPrefixLLM-DeepSeek": [107, 90, 87, 86, 85]
}

# Convert into pandas DataFrames
df_8 = pd.DataFrame(data_8)
df_16 = pd.DataFrame(data_16)
df_32 = pd.DataFrame(data_32)

plt.rcParams.update({
    "font.family": "Times New Roman",  # Try "Times" or "Times New Roman"
    "font.size": 12
})

# Plotting function
def plot_bitwidth(df, bitwidth):
    plt.figure(figsize=(8, 5))
    for method in df.columns[1:]:
        plt.plot(df["Delay"], df[method], marker='o', label=method)
    plt.title(f"Area vs Delay for {bitwidth}-bit Prefix Circuits")
    plt.xlabel("Delay")
    plt.ylabel("Area")
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.legend(loc="best", fontsize=8)
    
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Generate plots
plot_bitwidth(df_8, 8)
plot_bitwidth(df_16, 16)
plot_bitwidth(df_32, 32)
