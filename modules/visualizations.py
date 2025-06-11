import plotly.graph_objects as go

def create_radar_chart(df, selected_players, metrics):
    fig = go.Figure()
    for player in selected_players:
        player_data = df[df["Player Name"] == player][metrics].values.flatten()
        fig.add_trace(go.Scatterpolar(
            r=player_data,
            theta=metrics,
            fill='toself',
            name=player
        ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=True
    )
    return fig
