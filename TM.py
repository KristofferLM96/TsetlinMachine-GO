from pyTsetlinMachineParallel.tm import MultiClassTsetlinMachine
# from pyTsetlinMachine.tm import MultiClassTsetlinMachine
import numpy as np
from time import time

# Parameters
split_ratio = 0.9
epochs = 50
clauses = 1000
T = 8000
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


def loading_data(_clauses, _T, _s, _epochs):
    print("Loading data.. ")
    global X_train
    global Y_train
    global X_test
    global Y_test
    data = np.loadtxt(path, delimiter=",")
    X_train = data[int(len(data) * split_ratio):, 0:-1]
    Y_train = data[int(len(data) * split_ratio):, -1]
    X_test = data[:int(len(data) * split_ratio), 0:-1]
    Y_test = data[:int(len(data) * split_ratio), -1]
    print(".. data loaded.", "\n")

    return TM(_clauses, _T, _s, _epochs)


def TM(_clauses, _T, _s, _epochs):
    global X_train
    global Y_train
    global X_test
    global Y_test
    print("Creating MultiClass Tsetlin Machine.")
    tm = MultiClassTsetlinMachine(_clauses, _T, _s, boost_true_positive_feedback=0, weighted_clauses=True)
    print("Starting TM with weighted clauses..")
    print("\nAccuracy over ", _epochs, " epochs:\n")
    results = []
    total_results = 0
    for i in range(_epochs):
        start_training = time()
        tm.fit(X_train, Y_train, epochs=1, incremental=True)
        stop_training = time()

        start_testing = time()
        result = 100 * ((tm.predict(X_test) == Y_test).mean())
        results.append(result)
        stop_testing = time()

        print("#%d Accuracy: %.2f%% Training: %.2fs Testing: %.2fs" % (
            i + 1, result, stop_training - start_training, stop_testing - start_testing))

    for _result in range(len(results)):
        total_results = total_results + _result

    mean_accuracy = total_results / len(results) * 100

    return mean_accuracy


score = loading_data(clauses, T, s, epochs)
print(score)
