#! /usr/bin/env python
import pandas as pd
import numpy as np

def main(argv):
  numberUsers = 943
  numberGenres = 18

  # Static declarations
  users = [[0 for x in range(numberGenres)] for y in range(numberUsers)]
  userGenreCount = [[0 for x in range(numberGenres)] for y in range(numberUsers)]

  # Read data from files
  movie_item, movie_rating = readData()

  # Iterate over dataset gathering data
  iterateUserRatedMovies(users, userGenreCount, movie_item, movie_rating)

  # Calculate weights for each user
  res = calcResultingWeight(users, userGenreCount)

  # Save data in file, using numpy
  np.savetxt('testResult/system1_result', res, delimiter=',')

# Reads dataset from files
def readData():
  """ Returns the datasets in pandas DataFrame objects"""
  # Static directories#
  movie_genre_data = 'ml-100k/u.genre'
  movie_item_data = 'ml-100k/u.item'
  movie_user_data = 'ml-100k/u.user'
  movie_rating_data = 'split/train.csv'
  
    # Read data using pandas#
  movie_item = pd.read_csv(movie_item_data, sep="|", usecols=range(5, 24), header=None)
  movie_genre_names = pd.read_csv(movie_genre_data, sep="|", usecols=range(1), header=None)
  movie_item.columns = [movie_genre_names]
  movie_rating = pd.read_csv(movie_rating_data, sep="\t", usecols=range(0, 3), header=None)
  movie_rating.columns = ["user id", "item id", "rating"]
  return movie_item, movie_rating

# This version is very slow, about O(N)
def iterateUserRatedMovies(users, userGenreCount, movie_item, movie_rating):
  """If a user has seen a movie
    1. Examine what rating the user gave it
    2. Examine what genres where connected to that movie
    3. Assume the user likes thos genres just as much as the movie
    4. Save the user + rating + genres in a dict """
  global numberUsers
  global numberGenres
  
  for index, column in movie_rating.iterrows():
      for genre in range(0, numberGenres):
          if movie_item.values[column['item id']-1, genre] == 1:
            users[column['user id']-1][genre] += column['rating']
            userGenreCount[column['user id']-1][genre] += 1
  return 

# Calculate weights for each user, this version is slow
# about O(N)
def calcResultingWeight(users,userGenreCount):
  """ For each user
    Calculate genre-weight-userX/number-of-times-genre-was-seen-by-userX
    Save this value """
  global numberUsers
  global numberGenres
  for user in range(0, numberUsers):
    for weight in range(0, numberGenres):
      if userGenreCount[user][weight] != 0:
        users[user][weight] = round(float(users[user][weight]) / userGenreCount[user][weight], 2)
    return users

  if __name__ == "__main__":
    main()
