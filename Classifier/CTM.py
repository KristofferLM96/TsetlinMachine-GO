from pyTsetlinMachineParallel.tm import MultiClassConvolutionalTsetlinMachine2D


def init(os, _clauses, _t, _s, _window_x, _window_y, _shape_x, _shape_y, _shape_z, _name, _machine_type, _data_dim,
         _dataset, app_start_date, _epoch, _boost, _weighted, _epoch_results):
    epoch_count = 0
    for i in range(_epoch):
        _epoch_results.append([])

    print("Creating result file in.. ", "Results/" + _name + "/" + _machine_type + "/" + _data_dim
          + _dataset + "/" + str(_window_x) + "x" + str(_window_y) + "/"
          + _data_dim + _dataset + "_" + app_start_date + ".csv", "\n\n")
    os.makedirs(os.path.dirname("Results/" + _name + "/" + _machine_type + "/" + _data_dim + _dataset + "/"
                                + str(_window_x) + "x" + str(_window_y) + "/" + _data_dim + _dataset + "_"
                                + app_start_date + ".csv"), exist_ok=True)
    _results = open("Results/" + _name + "/" + _machine_type + "/" + _data_dim + _dataset + "/"
                    + str(_window_x) + "x" + str(_window_y) + "/" + _data_dim + _dataset + "_"
                    + app_start_date + ".csv", 'a')
    _results.write("MultiClassConvolutionalTsetlinMachine2D,Parallel,")

    while epoch_count < _epoch:
        _results.write("Epoch" + str(epoch_count + 1) + ",")
        epoch_count += 1
    _results.write("\n")

    _results.write("Settings:\nClauses:,%.1f\nThreshold:,%.1f\ns:,%.1f\nboost:,%s\nWindow_X:,%.1f\n"
                   "Window_Y:,%.1f\nShape_X:,%.1f\nShape_Y:,%.1f\nShape_Z:,%.1f\n"
                   % (_clauses, _t, _s, _boost, _window_x, _window_y, _shape_x, _shape_y, _shape_z))

    _results.close()

    print("Settings:", "\n")
    print("Clauses:", _clauses)
    print("Threshold:", _t)
    print("s:", _s)
    print("boost:", _boost)
    print("weighted clauses:", _weighted)
    print("Window X", _window_x)
    print("Window Y", _window_y)
    print("Shape X", _shape_x)
    print("Shape Y", _shape_y)
    print("Shape Z", _shape_z)
    print("\n")

    return _epoch_results


def load_data(train_data, test_data, _shape_x, _shape_y, _shape_z, _window_x, _window_y, _clauses, _t, _s, _boost,
              _weighted, _data_dim, data_name, _dataset, _app_start_date, _name, _machine_type, _numb):
    x_train = train_data[:, 0:-1].reshape(train_data.shape[0], _shape_x, _shape_y, _shape_z)
    y_train = train_data[:, -1]
    x_test = test_data[:, 0:-1].reshape(test_data.shape[0], _shape_x, _shape_y, _shape_z)
    y_test = test_data[:, -1]

    machine = MultiClassConvolutionalTsetlinMachine2D(_clauses, _t, _s, (_window_x, _window_y),
                                                      boost_true_positive_feedback=_boost,
                                                      weighted_clauses=_weighted)
    print("-------------------------------------------------------------------------------------------")
    print("MultiClassConvolutionalTsetlinMachine2D using %s, Draw, %s, written to file %s%s_%s.csv "
          "(%.1f x %.1f x %.1f)""\n"
          % (_data_dim, _dataset, data_name, _dataset, _app_start_date,
             _shape_x, _shape_y, _shape_z))
    print("Settings: Clauses: %.1f Threshold: %.1f S: %.1f Window_X: %.1f Window_Y: %.1f\n" % (
        _clauses, _t, _s, _window_x, _window_y))

    _results = open("Results/" + _name + "/" + _machine_type + "/" + _data_dim + _dataset + "/"
                    + str(_window_x) + "x" + str(_window_y) + "/"
                    + _data_dim + _dataset + "_" + _app_start_date + ".csv", 'a')
    _results.write(_data_dim + _dataset + _numb + ",")
    _results.close()

    return x_train, y_train, x_test, y_test, machine
