import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from scipy.interpolate import make_interp_spline

# Define the data
data = {
    'Year': ['2020', '2021', '2022', '2023', '2024'],
    'Skills': [
        'Flask, Basic Authentication, DBMS',
        'Django, REST API, PostgreSQL, Vue, XAI, HCI, JavaScript',
        'Node.js, Web Scraping, Pandas, NumPy, Kubernetes, Golang',
        'Django Channels & Signals, API Security, System Design, MVP Documentation',
        'Prompt Engineering, ETL, Shell Scripting, Claude API Integration'
    ]
}

# Convert data to DataFrame
df = pd.DataFrame(data)
df['Year'] = pd.to_datetime(df['Year'])

# Define y_positions to reflect the growth and stagnation pattern
y_positions = [1, 2, 2, 3, 3]  # Growth from 2020 to 2021, same level 2021-2022, growth 2022-2023, same level 2023-2024

# Create smooth curves using Bezier-style interpolation
x_vals = mdates.date2num(df['Year'])  # Convert dates to numerical format for interpolation
spl = make_interp_spline(x_vals, y_positions, k=2)  # Smooth curve (k=2 for smoothness)
x_smooth = np.linspace(x_vals.min(), x_vals.max(), 500)
y_smooth = spl(x_smooth)

# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the smooth curve with color gradient
ax.plot(x_smooth, y_smooth, color='teal', lw=3)

# Add circular markers for each year
ax.scatter(df['Year'], y_positions, s=100, color='teal', edgecolor='darkblue', zorder=5)

# Annotate each point with skills and stagger positions to prevent overlap
offsets = [0.1, -0.15, 0.1, -0.15, 0.1]  # Alternating offset positions
colors = plt.cm.viridis(np.linspace(0, 1, len(df)))
for i, row in df.iterrows():
    # Set the color to darkgreen for 2024
    skill_color = 'darkgreen' if row['Year'].year == 2024 else colors[i]
    ax.text(row['Year'], y_positions[i] + offsets[i], row['Skills'], ha='center', fontsize=9, color=skill_color)
    ax.text(row['Year'], y_positions[i] - 0.3, row['Year'].year, ha='center', fontsize=11, fontweight='bold')

# Set x-axis to display years only
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

# Remove y-axis (not needed for timeline)
ax.get_yaxis().set_visible(False)

# Add light grid and title
plt.grid(axis='x', linestyle='--', alpha=0.5)
ax.set_xlabel("Year", fontsize=12)
ax.set_title("Skills Progression Timeline (2020 - 2024)", fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig("skills_progression_timeline.png", dpi=300, bbox_inches="tight")

plt.show()
