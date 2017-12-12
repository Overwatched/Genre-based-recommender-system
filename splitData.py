import pandas as pd
from sklearn.model_selection import train_test_split

# Splitting the data set using scikit 
movie_rating_data = 'ml-100k/u.data'
dataset = pd.read_csv(movie_rating_data, sep="\t",
                      usecols=range(0, 3), header=None)
dataset.columns = ["userId", "movieId", "rating"]

dataset_train = []
dataset_test = []

for user in range(1, 944):
    ratingsForUser = dataset[(dataset.userId == user)]
    train, test = train_test_split(ratingsForUser,
                                   test_size=0.3, train_size=0.7)
    i = 0
    for u in train.iterrows():
        dataset_train.append([train.values[i, 0],
                              train.values[i, 1], train.values[i, 2]])
        i += 1
    i = 0
    for u in test.iterrows():
        dataset_test.append([test.values[i, 0],
                             test.values[i, 1], test.values[i, 2]])
        i += 1

random_frame = pd.DataFrame(dataset_train)
random_frame.to_csv('Split/train.csv', sep='\t', index=False)

random_frame2 = pd.DataFrame(dataset_test)
random_frame2.to_csv('Split/test.csv', sep='\t', index=False)
