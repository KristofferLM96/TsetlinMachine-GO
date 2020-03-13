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
