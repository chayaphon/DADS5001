## DADS5001: Assignment 3 (Plotly)


## Dataset Overview
The dataset come from kaggle - english premier league football tournament during 2021-2022.
https://www.kaggle.com/datasets/saife245/english-premier-league/data?select=2021-2022.csv
The dataset has many collections of metrics happend during the match for each team but in this assignment we will focus only one matrics which is FTR.
FTR and Res = Full-Time Result (H=Home Win, D=Draw, A=Away Win)
We would like to study on team performace by using wining rate metrics of each team record during this tournament.
To see the leader of the tournament and its acordance.

### [Code](https://github.com/chayaphon/DADS5001/tree/main/Assignment_3/code.ipynb)

![Image](https://raw.githubusercontent.com/chayaphon/DADS5001/main/Assignment_3/plotly_output.png)

## Why selecting this chart
Comparative Analysis: This data involves comparing two related aspects of performance between home and away win rates for football teams, enabling viewers to quickly see how teams fare in different settings.

Identification of Patterns: By plotting each team as a distinct point, it's easier to identify patterns or trends within the league, such as whether teams generally perform better at home or away, or if there's a wide variance in performance across the league.

Annotations for Clarity: Adding annotations with team names directly on the plot addresses one of the common challenges with scatter plots—identifying what each point represents. This is crucial when the specific identity of each point (in this case, each team) is important for the analysis or discussion.

Use of Median Lines: Including median lines for home and away win rates helps in understanding the distribution of the data. It highlights teams that are above or below the median, allowing for a quick assessment of which teams are performing better or worse than average in both home and away games. This can also indicate a general trend of home advantage if many teams have higher win rates at home.


