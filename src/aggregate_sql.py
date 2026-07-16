import pandas as pd
import sqlite3

conn = sqlite3.connect("data/processed/airbnb.db")
listings = pd.read_csv("data/processed/listings_clean.csv")
listings.to_sql("listings", conn, if_exists="replace", index=False)

# Neighborhood-level stats — using review activity instead of star rating
# since this dataset doesn't include review scores
query = """
SELECT
    neighbourhood_group AS borough,
    neighbourhood,
    COUNT(*) AS listing_count,
    ROUND(AVG(price), 2) AS avg_price,
    ROUND(AVG(reviews_per_month), 2) AS avg_reviews_per_month,
    SUM(number_of_reviews) AS total_reviews
FROM listings
GROUP BY neighbourhood_group, neighbourhood
HAVING listing_count >= 10
ORDER BY avg_price DESC
"""

neighborhood_stats = pd.read_sql(query, conn)
neighborhood_stats.to_csv("data/processed/neighborhood_stats.csv", index=False)

print(neighborhood_stats.head(10))
conn.close()