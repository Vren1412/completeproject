import pandas as pd
import random
num_users = 100
num_movies = 150
ratings_data = []
for user_id in range(1, num_users +1):
    for _ in range(random.randint(5, 20)):
        movie_id = random.randint(1,num_movies)
        rating = round(random.uniform(1,5),1)
        ratings_data.append((user_id, movie_id, rating))
df = pd.DataFrame(ratings_data, columns=["userId","movieId","rating"])
df.to_csv("ratings.csv", index=False)
print("ratings.csv generated!")