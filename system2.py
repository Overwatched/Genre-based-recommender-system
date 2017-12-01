from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import pandas as pd
from itertools import chain

# Read static data-set files
users_weight = np.genfromtxt('testResult/system1_result', delimiter=',')
ub_base = pd.read_csv('train.csv', sep="\t", usecols=range(0, 3), header=None)
ub_base.columns = ["user id", "movie id", "rating"]
ub_test = pd.read_csv('test.csv', sep="\t", usecols=range(0, 3), header=None)
ub_test.columns = ["user id", "movie id", "rating"]

# Define datastructures
user_dic = {}
user_test = {}


def main():
    # Create two helpful for fast access dictionaries
    datastructureForUsers()
    datastructureForTest()

    # Run the classifier algorithm
    X = runKnn()

    # Calculate how accurate the system is
    res = calculateConvergence(X)

    # Write the results to file
    df = pd.DataFrame(res)
    df.to_csv('testResult/system2_result.csv', header=["Precision", "Recall", "Zeroed",
                                        "NmrNeighbors", "NmrRecommendations"])


def calculateConvergence(X):
    """Iterates over a selection of neighbor/recommenation
    combinations and calculates average precision and
    recall metrics for each combination. Used for testing system
    accuracy.
    This is slow and may take a long time."""
    res = []
    for i in range(2, 100, 2):
        print("Iteration:", i)
        for i2 in range(1, 100, 2):
            temp = avgStats(i, i2, X)
            temp.append(i)
            temp.append(i2)
            res.append(temp)
    return res


def avgStats(numberNeighbors, numberRecommendations, dataSet):
    """ Calculates the average precision and recall metrics for a
    combination of neighbors and recommendations.
    This function may be slow, depending on how many neighbors that is used"""
    res = []
    pAvList = []
    rAvList = []
    pN = 0
    rN = 0
    startNeighbors = 1
    endNeighbors = 943
    for i in range(startNeighbors, endNeighbors):
        neighbors = getNeighbors(i, numberNeighbors, False, dataSet)
        retrievedRecommendations = recomendationList(neighbors,
                                                     numberRecommendations, i)
        precisionV, recall = precisionRecall(retrievedRecommendations, i)
        if(precisionV == 0):
            pN += 1
        if(recall == 0):
            rN += 1
        pAvList.append(precisionV)
        rAvList.append(recall)

    res.append(round(np.mean(pAvList), 2))
    res.append(round(sum(rAvList)/len(rAvList), 2))
    res.append(rN)
    return res


def datastructureForUsers():
    """ Helper function in order to create a more easily
    accessible data structure to work with.
    Creates a multi dimensional dict for fast acces  """
    for i, u in ub_base.iterrows():
        if(u['user id'] not in user_dic):
            user_dic[int(u['user id'])] = {}

    user_dic[int(u['user id'])][int(u['movie id'])] = u['rating']
    return


def datastructureForTest():
    """ Helper function in order to create a more easily accessible
    data structure to work with.
    Creates a multi dimensional dict for fast access"""
    for i, u in ub_test.iterrows():
        if(u['user id'] not in user_test):
            user_test[int(u['user id'])] = {}

    user_test[int(u['user id'])][int(u['movie id'])] = u['rating']
    return


def runKnn():
    """ Runs the KNeighborsClassifier where each user genre preferences
    as X and the corresponding user id as Y """
    knn = KNeighborsClassifier()
    X = users_weight
    y = range(0, 943)
    return knn.fit(X, y)


def getNeighbors(element, nrNeighbors, returnDistance, knn):
    """ Retrieves X neighbors, from a point element, and optionally
    the distance to the neighbors, as a list """
    return list(chain.from_iterable(knn.kneighbors([users_weight[element]], nrNeighbors, return_distance=returnDistance).tolist()))


def recomendationList(neighborIds, numberRecommendations, user):
    """ Returns a list of recommended movies for a specific user,
    one can specifiy how many recommendations one wants. A specification
    of what neighbors the recommendations should be retrieved from
    must be provided. """
    neighborMovies = {}
    myself = 0
    for i3, i4 in enumerate(neighborIds):
        if(i4 == user):
            myself = neighborIds[i3]
            del neighborIds[i3]

    for i, nb in enumerate(neighborIds):
        for y, nb2 in enumerate(user_dic[int(nb)]):
            user_rating = user_dic[nb][nb2]
            user_movie = nb2
            if(user_movie not in user_dic[myself]):
                if(user_movie in neighborMovies):
                    neighborMovies[user_movie]['Rating'] = ((neighborMovies[user_movie]['Rating'] + user_rating) / 2)+1
                    neighborMovies[user_movie]['Times'] += 1
                else:
                    neighborMovies[user_movie] = {}
                    neighborMovies[user_movie]['Rating'] = user_rating
                    neighborMovies[user_movie]['Times'] = 1

    list1 = sorted(neighborMovies.items(), key=lambda x: x[1])
    list2 = []
    nmr = len(list1)-int(numberRecommendations)
    for i, np in enumerate(list1[int(nmr):len(neighborMovies)]):
        list2.append(np[0])
    return list2


def precisionRecall(recommendationList, myself):
    """ An implmentation of precision and recall """
    equal = 0
    for i, movie in enumerate(recommendationList):
        if(movie in user_test[myself]):
            equal += 1
    return equal/float(len(recommendationList)), equal/float(len(user_test[myself]))


if __name__ == "__main__":
    main()
