# Frequently Asked Questions (FAQ)

### Can I compare players in positions they haven't played in?
**No.** Best.XI is designed to compare players based on their performance when playing the same position. For example, if you select "Left Winger," only players who have actually played as a Left Winger (according to your uploaded data) will be available for comparison. Comparing a player's stats from a different position (e.g., a Center Back's stats while playing CB) would not provide a fair or meaningful comparison for the winger role.

---

### How does Best.XI handle negative metrics (where lower is better)?
Some stats, like Fouls, Yellow Cards, Red Cards, Losses, Conceded Goals, and similar, are considered "negative metrics" — meaning lower values are better. Best.XI automatically inverts the normalization for these metrics, so that a lower value results in a higher normalized score. This ensures that players are rewarded for having fewer negative events, and the scoring remains fair and intuitive.

**Example:**
If Player A has 2 yellow cards and Player B has 5 yellow cards, Player A will receive a higher normalized score for this metric, since fewer yellow cards is better.

---

### Can I use Best.XI for recruiting?
**Yes, but with caution.** You can use Best.XI to compare potential recruits, but remember that players may have faced different levels of competition. For example, a striker in a lower league may have better stats than one in a higher league simply due to the quality of opposition. Best.XI does **not** adjust for strength of schedule or opponent, so always consider the context of the data when making recruiting decisions.

---

### Why do we need this tool?
Best.XI provides an unbiased, data-driven perspective to supplement coaching decisions. While coaches have deep knowledge of their players and systems, unconscious biases or preconceptions can sometimes influence lineup choices. Best.XI helps ensure that lineup decisions are also informed by the **objective** metrics and performance indicators that the coaching staff values most for each position.

---

### What kind of data do I need to use Best.XI?
You need player performance data in Excel format (.xlsx), with each file representing a single player. The data should include player name, position, minutes played, and relevant performance metrics (e.g., goals, assists, passes, tackles, etc.). Only upload data you have the right to use.

---

### Is Best.XI affiliated with Wyscout or any other data provider?
No. Best.XI is not affiliated with, endorsed by, or partnered with any data provider. Users are responsible for ensuring they have the legal right to use any data uploaded to the platform.

---

### How are the scores calculated?
Best.XI normalizes each selected metric for the group of players being compared (0 = lowest, 1 = highest), applies your chosen weights, and combines them into a "Position Score" (0-10 scale). The player with the highest Position Score is the best performer in the selected position based on the selected metrics and weights.

---

### What does it mean if all players are at 0 for a stat on the radar plot?
If all players are at 0 for a stat, it means every player had the same value for that stat in the data provided. There was no difference to compare for that metric among the selected players.

**Example:**
If all compared players have 1 goal, the radar plot will show 0 for this metric for everyone, indicating no difference in this stat.

--- 

### During data processing, do you only factor in the games that the players played in that position?
Yes. Best.XI only includes games where each player played the selected position (or grouped position) for analysis and scoring. This ensures that all comparisons are fair and position-specific.

**Example:**
If you are comparing players for the "Left Winger" position, and a player played 10 games in total but only 4 as a Left Winger, only those 4 games will be used for their stats and scoring in the comparison. The other 6 games (played in different positions) are ignored for this analysis.

---
