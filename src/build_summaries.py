import pandas as pd

stats = pd.read_csv("data/processed/neighborhood_stats.csv")

# Recreate the same value_score logic from Power BI (DAX):
# value_score = (avg_reviews_per_month / avg_price) * 100
stats["value_score"] = (stats["avg_reviews_per_month"] / stats["avg_price"] * 100).round(2)

summaries = {}
for _, row in stats.iterrows():
    text = (
        f"{row['neighbourhood']} ({row['borough']}): average price ${row['avg_price']}, "
        f"average {row['avg_reviews_per_month']} reviews per month, "
        f"value score {row['value_score']} (higher = better value for money), "
        f"based on {row['listing_count']} listings."
    )
    summaries[row["neighbourhood"].lower()] = text

with open("data/processed/neighborhood_summaries.txt", "w") as f:
    for text in summaries.values():
        f.write(text + "\n")

print(f"Built {len(summaries)} neighborhood summaries.")