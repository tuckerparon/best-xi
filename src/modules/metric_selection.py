import streamlit as st

def render_metric_weights_ui(selected_metrics, selected_position):
    """
    Renders the UI for assigning weights to selected metrics.
    Replaces the static prototype logic with a dynamic function for app.py.
    """
    if not selected_metrics:
        return {}

    st.subheader(f"Step 4: Rank Metrics Importance (1-10) for {selected_position}.")
    weights = {}
    
    # Use columns to make the UI compact
    num_cols = min(3, len(selected_metrics))
    cols = st.columns(num_cols)
    
    for idx, metric in enumerate(selected_metrics):
        with cols[idx % num_cols]:
            weights[metric] = st.number_input(
                f"{metric}", 
                min_value=1, 
                max_value=10, 
                value=5, 
                step=1, 
                key=f"weight_{metric}", 
                format='%d'
            )
            
    return weights