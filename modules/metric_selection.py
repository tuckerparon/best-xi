import streamlit as st

# Define available metrics
ALL_METRICS = [
    'Goals', 'Assists', 'Shots', 'Pass Accuracy (%)', 'Tackles',
    'Aerial Duels Won', 'Interceptions', 'Key Passes', 'Clean Sheets', 'Saves'
]

# Allow coaches to define metrics and weights for each position
st.title("Define Metrics and Weights for Each Position")

positions = ['FW', 'CB', 'CM', 'FB', 'WG', 'GK']
weights = {}

for position in positions:
    st.subheader(f"Metrics for {position}")
    selected_metrics = st.multiselect(
        f"Select 10 metrics for {position}",
        options=ALL_METRICS,
        default=ALL_METRICS[:10],  # Pre-fill with default metrics
        key=f"{position}_metrics"
    )
    
    # Ensure exactly 10 metrics are selected
    if len(selected_metrics) != 10:
        st.warning(f"Please select exactly 10 metrics for {position}.")
        continue
    
    # Weight each selected metric
    st.write(f"Assign weights to metrics for {position} (higher = more important)")
    metric_weights = {}
    for metric in selected_metrics:
        weight = st.slider(f"Weight for {metric} ({position})", min_value=1, max_value=10, value=5)
        metric_weights[metric] = weight

    # Store weights for the position
    weights[position] = metric_weights

st.write("Metric weights defined:", weights)
