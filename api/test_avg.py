
import pandas as pd

data = {
    "feed1": [
        {
            "cat_1": 1,
            "cat_2": 5,
            "cat_3": 3,
            "cat_4": 5,
            "cat_5": 3,
            "cat_6": 1,
            "cat_7": 1,
            "cat_8": 1,
            "cat_9": 3,
            "cat_10": 1
        }
    ]
}
df = pd.DataFrame(data)
# Filter for categories with values 5, 3, or 1
filtered_df = df[(df == 5) | (df == 3) | (df == 1)]
print(f'filter df : {filtered_df}')
# Calculate the average for the filtered categories
avg_filtered = filtered_df.mean()
print(f' avg : avg_filtered')