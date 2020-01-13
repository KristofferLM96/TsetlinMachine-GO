from pyTsetlinMachineParallel.tm import MultiClassTsetlinMachine
import numpy as np
from time import time

# Parameters
split_ratio = 0.9
epochs = 50
clauses = 10000
T = 80
s = 27

print("epochs = ", epochs)
print("clauses = ", clauses)
print("T = ", T)
print("s = ", s, "\n")

X_train = np.array([])
Y_train = np.array([])
X_test = np.array([])
Y_test = np.array([])

path = "Data/Binary/9x9Natsukaze_binary.txt"


def loading_data(_data, _clauses, _T, _s, _epochs):
    global X_train
    global Y_train
    X_train = _data[int(len(_data)):, 0:-1]
    Y_train = _data[int(len(_data)):, -1]

    global X_test
    global Y_test
    X_test = _data[int(len(_data)):, 0:-1]
    Y_test = _data[int(len(_data)):, -1]

    return TM(_clauses, _T, _s, epochs)


def TM(_clauses, _T, _s, _epochs):
    print("Creating MultiClass Tsetlin Machine.")
    tm = MultiClassTsetlinMachine(_clauses, _T, _s, boost_true_positive_feedback=0, weighted_clauses=True)
    print("Starting TM with weighted clauses..")
    print("\nAccuracy over ", _epochs, " epochs:\n")
    for i in range(_epochs):
        start = time()
        tm.fit(X_train, Y_train, epochs=1, incremental=True)
        stop = time()
        result = 100 * (tm.predict(X_test) == Y_test).mean()
        print("#%d Accuracy: %.2f%% (%.2fs)" % (i + 1, result, stop - start))

    mean_accuracy = 100 * (tm.predict(X_test) == Y_test).mean()
    print("Mean Accuracy:", mean_accuracy)
    print("Finished running.. \n")

    return mean_accuracy


data = np.loadtxt(path, delimiter=",")
score = loading_data(data, clauses, T, s, epochs)
print(score)
