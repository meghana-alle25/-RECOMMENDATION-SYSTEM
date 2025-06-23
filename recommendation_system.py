# Movie Recommendation System using scikit-learn and MovieLens 100K Dataset

import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics import mean_squared_error

# Step 1: Load MovieLens ratings dataset
ratings = pd.read_csv("ml-100k/u.data", sep="\t", names=["userId", "itemId", "rating", "timestamp"])
ratings.drop("timestamp", axis=1, inplace=True)

# Step 2: Create user-item matrix
user_item_matrix = ratings.pivot_table(index='userId', columns='itemId', values='rating').fillna(0)
matrix = user_item_matrix.values

# Step 3: Apply TruncatedSVD (Matrix Factorization)
svd = TruncatedSVD(n_components=50, random_state=42)
matrix_reduced = svd.fit_transform(matrix)
matrix_reconstructed = np.dot(matrix_reduced, svd.components_)

# Step 4: Evaluate using Mean Squared Error
mse = mean_squared_error(matrix.flatten(), matrix_reconstructed.flatten())
print(f"Mean Squared Error: {mse:.4f}")

# Step 5: Recommend Top-N movies for a user
user_index = 0  # UserId = 1 (0-based index)
user_ratings = matrix_reconstructed[user_index]
unrated_items = np.where(matrix[user_index] == 0)[0]

top_n = sorted([(i, user_ratings[i]) for i in unrated_items], key=lambda x: x[1], reverse=True)[:5]

print(f"\nTop 5 Movie Recommendations for User {user_index + 1}:")
for item_id, score in top_n:
    print(f"Movie ID {user_item_matrix.columns[item_id]} with predicted rating {score:.2f}")

# Step 6 (Optional): Map Movie IDs to Titles
movies = pd.read_csv("ml-100k/u.item", sep="|", encoding="latin-1", header=None, usecols=[0, 1], names=["itemId", "title"])
movie_map = dict(zip(movies.itemId, movies.title))

print("\nRecommended Movie Titles:")
for item_id, score in top_n:
    movie_title = movie_map.get(user_item_matrix.columns[item_id], "Unknown")
    print(f"{movie_title} - Predicted Rating: {score:.2f}")
