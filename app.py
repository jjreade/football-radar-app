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
selected_players = st.multiselect("Select up to three players", player_options, max_selections=3)

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

# --- Position template chart ---

position_templates = {
    "CB (Centre Back)": [
        'Games Played', 'Aerial Ratio', 'Defensive Actions', 'Recoveries', 'Interceptions', 'Blocks per Shot', 'Dribbled Past', 'Fouls', 'Deep Progressions', 'Deep Completions', 'Long Ball Ratio', 'Passing Ratio', 'Pressured Passing Ratio', 'nPK xG', 'nPK Shots'
    ],
    "FB (Full Back)": [
        'Games Played', 'Interceptions', 'Recoveries', 'Blocks per Shot', 'Tackles', 'Tackle Ratio', 'Dribbled Past', 'Fouls', 'Aerial Ratio', 'Deep Progressions', 'Deep Completions', 'Crosses', 'Crossing Ratio', 'Key Passes', 'xA', 'Dribble Ratio', 'OP Passes into Final Third'
    ],
    "WM (Wide Midfielder)": [
        'Games Played', 'Tackles', 'Tackle Ratio', 'Pressures', 'Pressure Regains', 'Deep Progressions', 'Crosses', 'Crossing Ratio', 'OP Passes into Final Third', 'Key Passes', 'xA', 'Dribbles', 'Dribble Ratio', 'Touches Inside Box', 'Fouls Won', 'nPK Shots', 'Shots on Target Ratio', 'Goal Conversion Ratio', 'nPK xG', 'nPK xG + xA'
    ],
    "CMD (Central Mid Defensive)": [
        'Games Played', 'Aerial Ratio', 'Defensive Actions', 'Recoveries', 'Interceptions', 'Tackles', 'Tackle Ratio', 'Fouls', 'Dribble Ratio', 'Deep Progressions', 'Deep Completions', 'Long Ball Ratio', 'Passing Ratio', 'Pressured Passing Ratio', 'OP Passes into Final Third', 'Key Passes', 'xA', 'Set Piece xA'
    ],
    "CMA (Central Mid Attacking)": [
        'Games Played', 'Aerial Ratio', 'Defensive Actions', 'Interceptions', 'Tackles', 'Tackle Ratio', 'Deep Progressions', 'OP Passes into Final Third', 'Key Passes', 'xA', 'Fouls Won', 'Dribbles', 'Dribble Ratio', 'nPK Shots', 'Shots on Target Ratio', 'Goal Conversion Ratio', 'nPK xG + xA', 'Set Piece xA'
    ],
    "CF (Centre Forward)": [
        "nPK xG", "nPK Goals", "Shots on Target Ratio", "Aerial Duels Won"
    ],
    "ST (Striker)": [
        'Games Played', 'nPK Shots', 'Shots on Target Ratio', 'nPK Goals', 'nPK xG', 'Goal Conversion Ratio', 'Dribble Ratio', 'Touches Inside Box', 'Turnovers', 'Fouls Won', 'OP Passes into Box', 'xA', 'Aerial Duels Won', 'Aerial Ratio', 'Tackles', 'Pressures', 'Pressure Regains'
    ],
    "GK (Goalkeeper)": [
        'Games Played', 'Shots Against on Target Ratio', 'Goals Saved Above Average Ratio', 'Save Ratio', 'Ideal Distance from Goal Line', 'Claimables Collected Above Average', 'Pressured Passing Ratio', 'Passing Ratio', 'Deep Progressions', 'Long Balls', 'Long Ball Ratio'
    ]
}

# Rename only for template radar
rename_dict = {
    'player_season_appearances': 'Games Played',
    'player_season_ot_shots_faced_ratio': 'Shots Against on Target Ratio',
    'player_season_gsaa_ratio': 'Goals Saved Above Average Ratio',
    'player_season_save_ratio': 'Save Ratio',
    'player_season_np_optimal_gk_dlength': 'Ideal Distance from Goal Line',
    'player_season_clcaa': 'Claimables Collected Above Average',
    'player_season_aerial_ratio': 'Aerial Ratio',
    'player_season_defensive_actions_90': 'Defensive Actions',
    'player_season_ball_recoveries_90': 'Recoveries',
    'player_season_padj_interceptions_90': 'Interceptions',
    'player_season_blocks_per_shot': 'Blocks per Shot',
    'player_season_dribbled_past_90_inverse': 'Dribbled Past',
    'player_season_fouls_90_inverse': 'Fouls',
    'player_season_deep_progressions_90': 'Deep Progressions',
    'player_season_deep_completions_90': 'Deep Completions',
    'player_season_long_ball_ratio': 'Long Ball Ratio',
    'player_season_pressured_passing_ratio': 'Pressured Passing Ratio',
    'player_season_passing_ratio': 'Passing Ratio',
    'player_season_np_xg_90': 'nPK xG',
    'player_season_np_shots_90': 'nPK Shots',
    'player_season_padj_tackles_90': 'Tackles',
    'player_season_challenge_ratio': 'Tackle Ratio',
    'player_season_crosses_90': 'Crosses',
    'player_season_crossing_ratio': 'Crossing Ratio',
    'player_season_key_passes_90': 'Key Passes',
    'player_season_xa_90': 'xA',
    'player_season_dribble_ratio': 'Dribble Ratio',
    'player_season_op_f3_passes_90': 'OP Passes into Final Third',
    'player_season_sp_xa_90': 'Set Piece xA',
    'player_season_padj_pressures_90': 'Pressures',
    'player_season_pressure_regains_90': 'Pressure Regains',
    'player_season_shot_on_target_ratio': 'Shots on Target Ratio',
    'player_season_conversion_ratio': 'Goal Conversion Ratio',
    'player_season_npxgxa_90': 'nPK xG + xA',
    'player_season_dribbles_90': 'Dribbles',
    'player_season_fouls_won_90': 'Fouls Won',
    'player_season_touches_inside_box_90': 'Touches Inside Box',
    'player_season_npg_90': 'nPK Goals',
    'player_season_turnovers_90_inverse': 'Turnovers',
    'player_season_op_passes_into_box_90': 'OP Passes into Box',
    'player_season_aerial_wins_90': 'Aerial Duels Won'
}

# Renamed copy just for the third radar
template_data = data.rename(columns=rename_dict)


st.header("⚽ Radar: Template by Position Role")

selected_role = st.selectbox("Choose a position role", list(position_templates.keys()))
template_metrics = position_templates[selected_role]

# Percentile scaling
template_percentiled = template_data.copy()
for col in template_metrics:
    template_percentiled[col] = template_percentiled[col].rank(pct=True) * 100

plot_radar(selected_players, template_metrics, f"{selected_role} Template Metrics", template_percentiled)

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

