import pandas as pd

df = pd.read_csv("input.txt", sep=" ", header=None)

rolling_sum = df.rolling(window=3).sum()

count_ascending = 0
prev_value = rolling_sum[0][0]
for obs in rolling_sum[0]:
    print(obs)
    next_value = obs
    if next_value > prev_value:
        count_ascending += 1
    prev_value = next_value

print(count_ascending)