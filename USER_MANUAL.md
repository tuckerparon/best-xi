# User Manual

## 1. Overview

**Best.XI** is a decision-support tool designed to help soccer coaches make more informed lineup selections. By allowing users to upload their own player performance data, Best.XI provides a data-centric perspective to supplement traditional coaching insights. The tool offers clear, visual, and quantitative comparisons between players based on customizable metrics.

> **Disclaimer:**  
> Best.XI is not affiliated with or endorsed by any data provider. Users must upload data they have the legal right to use. Best.XI is a standalone decision-support tool for lineup selection.


## 2. How to Use Best.XI

### Step-by-Step

1. **Upload Player Data:**  
   Drag and drop your player Excel files into the uploader.

2. **Select Position:**  
   Choose a position from the dropdown menu. Only positions present in at least one of the player data files will appear.

3. **Select Metrics:**  
   Pick the performance metrics you want to compare (e.g., goals, assists, passes).

4. **Assign Weights:**  
   Rank the importance of each metric (1-10). Higher numbers mean the metric is more important in the final score.

5. **Select Players:**  
   Choose which players to compare for the selected position.

6. **View Results:**  
   - **Table:** Shows each player's raw per-90 stats for the selected metrics and their overall "Position Score." The player with the highest Position Score is the best performer in the selected position based on the selected metrics (and weights) of the players up for comparison
   - **Radar Plot:** Visualizes how each player compares to the best and worst in the group for each metric. The player that covers the most surface area in the radar is the best performer in the selected position based on the selected metrics (and weights) of the players up for comparison. This player will also have the highest position score — the radar plot is just a different way to visualize the results.


## 3. How to Interpret the Results

### Table
- Shows raw per-90 values for each selected metric for each player.
- **Position Score**
  - Calculated using normalized values for each metric:
    - 0 means that player had the worst output for that metric compared to the other selected players.
    - 1 means that player had the best value for that metric compared to other selected players.
    - A value somewhere in the middle (e.g., 0.5) means the player's output for that metric was between the best and worst among the selected players.
  - Weighted by your chosen importance for each metric.
  - Final score is scaled from **0 to 10**:
    - 10 means this player had the BEST output for ALL selected metrics compared to the other selected players.
    - 0 means this player had the WORST output for ALL selected metrics compared to the other selected players.
    - A value somewhere in the middle (e.g., 5) means the player's overall performance was between the best and worst across all selected metrics.
  - The player with the highest Position Score is the player that Best.XI will recommend.

### Radar Plot
- Each axis represents a selected metric.
- A value closer to **1** means the player is the best in that stat among the selected players; closer to **0** means the lowest.
- If all players are at **0** for a stat, it means every player had the same value for that stat in the data provided.
- The player that covers the most surface area in the radar is the player that Best.XI will recommend. This player will also have the highest position score—the radar is just a different way to visualize the results.

### A Note on Normalization
- For each metric, the lowest value among the compared players is set to 0, the highest to 1, and everyone else is scaled in between. This allows fair comparison across different types of stats, even if they are on different scales (e.g., goals vs. passes).
- "Normalized" means we are comparing players relative to each other, not to an external standard.


## 4. Intended Use

**Best.XI is a decision-support tool.**  
It is designed to provide an additional, data-centric perspective to supplement (not replace) coaching decisions. Use Best.XI as one input among many in your lineup selection process.

## 5. Feedback & Support

As a Best.XI user, your feedback is invaluable! Please share your experience and suggestions to help us improve Best.XI. Please reach out to tucker@controllables.org or call/text me directly at (203) 217-7602.

## 6. Legal

- **Data Responsibility:**  
  Users are solely responsible for ensuring they have the right to use any data uploaded to Best.XI.
- **No Affiliation:**  
  Best.XI is not affiliated with or endorsed by any data provider, including Wyscout or similar services. 