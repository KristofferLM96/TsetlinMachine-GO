from pyTsetlinMachineParallel.tm import MultiClassTsetlinMachine


def init(os, _clauses, _t, _s, _name, _machine_type, _data_dim, _dataset, app_start_date, _epoch, _boost,
         _weighted, _epoch_results):
    epoch_count = 0
    for i in range(_epoch):
        _epoch_results.append([])

    print("Creating result file in.. ", "Results/" + _name + "/" + _machine_type + "/"
          + _data_dim + _dataset + "/" + _data_dim + _dataset + "_" + app_start_date + ".csv", "\n\n")
    os.makedirs(os.path.dirname("Results/" + _name + "/" + _machine_type + "/" + _data_dim + _dataset + "/"
                                + _data_dim + _dataset + "_" + app_start_date + ".csv"), exist_ok=True)
    _results = open("Results/" + _name + "/" + _machine_type + "/" + _data_dim + _dataset + "/"
                    + _data_dim + _dataset + "_" + app_start_date + ".csv", 'a')
    _results.write("MultiClassTsetlinMachineParallel,Parallel,")

    while epoch_count < _epoch:
        _results.write("Epoch" + str(epoch_count + 1) + ",")
        epoch_count += 1
    _results.write("\n")

    _results.write("Settings:\nClauses:,%.1f\nThreshold:,%.1f\ns:,%.1f\nboost:,%s\n"
                   % (_clauses, _t, _s, _boost))

    _results.close()

    print("Settings:", "\n")
    print("Clauses:", _clauses)
    print("Threshold:", _t)
    print("s:", _s)
    print("boost:", _boost)
    print("weighted clauses:", _weighted)
    print("\n")

    return _epoch_results


def load_data(train_data, test_data, _clauses, _t, _s, _boost, _weighted, _data_dim, data_name, _dataset,
              _app_start_date, _name, _machine_type, _numb):
    x_train = train_data[:, 0:-1]
    y_train = train_data[:, -1]
    x_test = test_data[:, 0:-1]
    y_test = test_data[:, -1]

    machine = MultiClassTsetlinMachine(_clauses, _t, _s, boost_true_positive_feedback=_boost,
                                       weighted_clauses=_weighted)
    print("-------------------------------------------------------------------------------------------")
    print("MultiClassTsetlinMachine using %s, Draw, %s, written to file %s%s_%s.csv\n"
          % (_data_dim, data_name, _data_dim, _dataset, _app_start_date))
    print("Settings: Clauses: %.1f Threshold: %.1f s: %.1f\n" % (_clauses, _t, _s))

    _results = open("Results/" + _name + "/" + _machine_type + "/" + _data_dim + _dataset + "/"
                    + _data_dim + _dataset + "_" + _app_start_date + ".csv", 'a')
    _results.write(_data_dim + _dataset + _numb + ",")
    _results.close()

    return x_train, y_train, x_test, y_test, machine
