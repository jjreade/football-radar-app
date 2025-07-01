import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Load data ---
@st.cache_data
def load_data():
    # Replace with your file path
    df = pd.read_csv("all-player-seasons-metrics.csv")
    return df

data = load_data()

# --- Player selection ---
player_options = data['player_name'].dropna().unique()
selected_players = st.multiselect("Select up to two players", player_options, max_selections=2)

if len(selected_players) == 0:
    st.warning("Please select at least one player to show radar plots.")
    st.stop()

# --- Radar plotting function ---
def plot_radar(players, columns, title, data):
    num_vars = len(columns)
    if num_vars < 3:
        st.warning("Need at least 3 variables to make a radar chart.")
        return

    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Complete the loop

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    for player in players:
        player_data = data[data['player_name'] == player]
        if player_data.empty:
            continue  # Skip if no data
        row = player_data.iloc[0]
        values = [row[col] for col in columns]
        values += values[:1]
        ax.plot(angles, values, label=player, linewidth=2)
        ax.fill(angles, values, alpha=0.25)

    ax.set_title(title, size=16, y=1.08)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(columns, color='grey', size=12)

    ax.set_rlabel_position(30)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(["20", "40", "60", "80", "100"], color="grey", size=10)
    ax.set_ylim(0, 100)

    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

    st.pyplot(fig)

# --- Category radar chart ---
st.header("📊 Radar: Category Scores")

category_cols = [col for col in data.columns if col.startswith('cat.')]
if category_cols:
    plot_radar(selected_players, category_cols, "Category Scores", data)
else:
    st.info("No columns found starting with 'cat.'")

# --- Custom metric radar chart ---
st.header("🎯 Radar: Custom Metrics")

metric_cols = [col for col in data.columns if col.startswith('player_season_')]
selected_metrics = st.multiselect("Select metrics to show (3 to 15)", metric_cols, max_selections=15)

if selected_metrics:
    if len(selected_metrics) < 3:
        st.warning("Please select at least 3 metrics for the radar chart.")
    else:
        # Create a copy to avoid modifying original data
        data_percentiled = data.copy()

        # Convert each selected metric to 0-100 percentile across all players
        for col in selected_metrics:
            # Use rank percentile, then scale to 0–100
            data_percentiled[col] = data_percentiled[col].rank(pct=True) * 100

        plot_radar(selected_players, selected_metrics, "User-Defined Metrics (0–100 percentiles)", data_percentiled)
else:
    st.info("Select individual metrics to build a custom radar.")
