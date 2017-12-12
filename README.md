# Genre-based-recommendations

This is a project that attempts to use Genres as a basis for recommendations, it uses the KNeighborsClassifier algorithm provided from the [scikit-learn](http://scikit-learn.org) library.
Since the project uses the algorithm in, a bit of an un-orthodox fashion, some of the work (quite alot) has to done by hand. Testing the system using precision and recall metrics is also done by hand. 

## Getting Started
If you are interested in continuing to work on this system (maybe using some other, more complex algorithm) feel free to do so. You can read more about the system in this [paper](www.example.com).

### Prerequisites
Currently the system is divided in two sub systems, namely **system 1 and 2**.

Running system 1 requires
* [Pandas](https://pandas.pydata.org/) (version 0.17.1)
* [numpy](http://www.numpy.org/) (version 1.13.1)
* [movielens_ml-100k](https://grouplens.org/datasets/movielens/) (released 1998)

Running system 2 requires
* [Pandas](https://pandas.pydata.org/) (version 0.17.1)
* [numpy](http://www.numpy.org/) (version 1.13.1)
* [scikit-learn](http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html)
* [itertools](https://docs.python.org/3/library/itertools.html)
* Output files from system 1

### Installing

Installing the requirements can be done in multiple ways, one simple way would be through pip.

Installing pandas and numpy through pip 
```
sudo apt-get install python-pip
sudo pip install numpy
sudo pip install pandas
```

### Files
* **splitData.py** Because of the un-orthodox usage of KNearestNeighbor the data has to be "manually" split
* **System 1** Calculate genre based weights for each user, outputs the result numpy encoded in *testResult/system1_result* 
* **System 2** Using the KnearestNeighbor, find X users that have the most similar genre preferences as you have, and give recommendations from them, based on most seen + highest rated combinations. Outputs a csv file *testResult/system2_result.csv* containing test results, how these where aquired can most easily be seen in the previously mentioned [paper](www.example.com), under the result chapter.
## Authors

* **Ludwig Kamras** - *Cool guy* - [LinkedIn](https://github.com/PurpleBooth)
* **William Matslova** - *Cooler guy* - [LinkedIn](https://github.com/PurpleBooth)

