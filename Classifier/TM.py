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
