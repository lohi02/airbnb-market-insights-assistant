import pandas as pd

# Load raw data
listings = pd.read_csv("data/raw/listings.csv")

# Keep only the columns we actually need for this project
# NOTE: this dataset has no review_scores_rating — we use number_of_reviews
# and reviews_per_month as our "demand/popularity" signal instead
columns_needed = [
    "id", "name", "neighbourhood_group", "neighbourhood", "room_type",
    "price", "number_of_reviews", "reviews_per_month", "availability_365"
]
listings = listings[columns_needed]

# Price is already a clean number in this file — no $ sign to strip.
# Still drop rows with no price, and fill missing reviews_per_month with 0
listings = listings.dropna(subset=["price"])
listings["reviews_per_month"] = listings["reviews_per_month"].fillna(0)

# Remove unrealistic outliers — this dataset's real max is over $30,000/night,
# almost certainly data errors, not real listings
listings = listings[(listings["price"] >= 20) & (listings["price"] <= 1000)]

# Save the cleaned version
listings.to_csv("data/processed/listings_clean.csv", index=False)

print(f"Cleaned data saved. {len(listings)} listings remain after cleaning.")