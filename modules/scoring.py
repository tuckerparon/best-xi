def calculate_position_scores(df, metrics_weights):
    """Calculate position scores for players based on selected metrics and weights."""
    df['Position Score'] = df.apply(
        lambda row: sum(row[metric] * weight for metric, weight in metrics_weights.items()), axis=1
    )
    return df
