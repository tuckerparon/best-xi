import plotly.graph_objects as go

def create_radar_chart(df, selected_players, metrics):
    """
    Create a radar chart comparing players across selected metrics.
    
    The radar chart shows:
    - Each metric is normalized to a 0-1 scale relative to the best performer
    - The area covered by each player's line represents their overall performance
    - A score of 0 means the player performed worst in that metric among the compared players
    - A score of 1 means the player performed best in that metric among the compared players
    - The metrics shown are per 90 minutes where applicable
    
    Args:
        df (pd.DataFrame): DataFrame containing player metrics
        selected_players (list): List of player names to compare
        metrics (list): List of metrics to display
    
    Returns:
        plotly.graph_objects.Figure: Radar chart figure
    """
    # Normalize metrics to 0-1 scale
    normalized_data = df.copy()
    for metric in metrics:
        min_val = df[metric].min()
        max_val = df[metric].max()
        if max_val > min_val:
            normalized_data[metric] = (df[metric] - min_val) / (max_val - min_val)
        else:
            normalized_data[metric] = 0
    
    # Colorblind-friendly palette
    color_palette = [
        '#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e',
        '#e6ab02', '#a6761d', '#666666', '#377eb8', '#ff7f00'
    ]
    
    fig = go.Figure()
    for idx, player in enumerate(selected_players):
        player_data = normalized_data[normalized_data["Player Name"] == player][metrics].values.flatten()
        fig.add_trace(go.Scatterpolar(
            r=player_data,
            theta=metrics,
            fill='toself',
            name=player,
            line=dict(color=color_palette[idx % len(color_palette)], width=3),
            marker=dict(color=color_palette[idx % len(color_palette)])
        ))
    
    fig.update_layout(
        polar=dict(
            bgcolor='#f8f8f8',
            radialaxis=dict(
                visible=True,
                gridcolor='#cccccc',
                linecolor='#888888',
                tickfont=dict(color='#222'),
                range=[0, 1],  # Set range to 0-1 for normalized values
                ticktext=['0', '0.25', '0.5', '0.75', '1'],
                tickvals=[0, 0.25, 0.5, 0.75, 1]
            ),
            angularaxis=dict(
                gridcolor='#cccccc',
                linecolor='#888888',
                tickfont=dict(color='#222')
            )
        ),
        plot_bgcolor='#f8f8f8',
        paper_bgcolor='#f8f8f8',
        showlegend=True,
        legend=dict(font=dict(color='#222')),
        title=dict(
            text="Player Comparison (Normalized Metrics)",
            font=dict(color='#222', size=16)
        )
    )
    
    return fig
