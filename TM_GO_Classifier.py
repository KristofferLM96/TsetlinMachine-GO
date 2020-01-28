import numpy as np
import time
import os

# Settings
clauses = 4000
Threshold = 64000
s = 27.0
epoch = 7
k_fold_parts = 1  # 1 - 10, how many k-fold parts to go through
machine_type = "TM"  # cTM or TM
parallel = True  # Running with/without parallel Tsetlin Machine
data_status = "Draw"  # Draw or No-Draw
data_dim = "9x9"  # 9x9, 13x13, 19x19 ..
data_name = "Aya_" + data_status  # Natsukaze_ || Aya_
Window_X = 9
Window_Y = 9
Shape_X = Shape_Y = 9  # Depending on data_dim
Shape_Z = 2  # 3D board
Name = "Kristoffer"  # Kristoffer or Trond
Write_Clauses = 0  # 0 = don't print clauses, 1-10 which k-Fold to write clauses for.
state_date = "20-01-28_1225"
state_path = "TM-State/" + data_dim + data_name + "_" + state_date + "/" + "state_"
load_state = False

if parallel:
    from pyTsetlinMachineParallel.tm import MultiClassTsetlinMachine
    from pyTsetlinMachineParallel.tm import MultiClassConvolutionalTsetlinMachine2D
else:
    from pyTsetlinMachine.tm import MultiClassTsetlinMachine
    from pyTsetlinMachine.tm import MultiClassConvolutionalTsetlinMachine2D

x_train = []
y_train = []
x_test = []
y_test = []
epoch_results = []
average_epoch_results = []
epochs_total = []
for i in range(epoch):
    epoch_results.append([])
timestamp_save = ""
offset_y = 0
offset_x = 0


def app(_epoch, _clauses, _t, _s, _data_name, _data_dim, _machine_type, _window_x, _window_y,
        _shape_x, _shape_y, _shape_z, _name, _write_clauses):

    def init(_machine_type, _name, _data_dim, _data_name, _epoch, _clauses, _t, _s, _window_x, _window_y,
             _shape_x, _shape_y, _shape_z, _epoch_results, _average_epoch_results,
             _epochs_total, _offset_x, _offset_y):
        epoch_count = 0
        for i in range(_epoch):
            _epoch_results.append([])

        if _machine_type == "TM":
            os.makedirs(os.path.dirname("Results/" + _name + "/" + _machine_type + "/" + _data_dim + _data_name + "/"
                                        + _data_dim + _data_name + "_" + timestamp_save + ".csv"), exist_ok=True)
            _results = open("Results/" + _name + "/" + _machine_type + "/" + _data_dim + _data_name + "/"
                            + _data_dim + _data_name + "_" + timestamp_save + ".csv", 'a')
        elif _machine_type == "cTM":
            os.makedirs(os.path.dirname("Results/" + _name + "/" + _machine_type + "/" + _data_dim + _data_name + "/"
                                        + str(_window_x) + "x" + str(_window_y) + "/" + _data_dim + _data_name + "_"
                                        + timestamp_save + ".csv"), exist_ok=True)
            _results = open("Results/" + _name + "/" + _machine_type + "/" + _data_dim + _data_name + "/"
                            + str(_window_x) + "x" + str(_window_y) + "/" + _data_dim + _data_name + "_"
                            + timestamp_save + ".csv", 'a')

        _offset_y = _shape_y - _window_y
        _offset_x = _shape_x - _window_x

        if _machine_type == "TM" and parallel:
            _results.write("MultiClassTsetlinMachineParallel,Parallel,")
        elif _machine_type == "TM" and not parallel:
            _results.write("MultiClassTsetlinMachine,")
        if _machine_type == "cTM" and parallel:
            _results.write(
                "MultiClassConvolutionalTsetlinMachine2D,Parallel,")
        elif _machine_type == "TM" and not parallel:
            _results.write("MultiClassConvolutionalTsetlinMachine2D,")
        while epoch_count < _epoch:
            _results.write("Epoch" + str(epoch_count + 1) + ",")
            epoch_count += 1
        _results.write("Average" + ",")
        _results.write("\n")

        if _machine_type == "TM":
            _results.write("Settings:\nClauses:,%.1f\nThreshold:,%.1f\ns:,%.1f\n" % (_clauses, _t, _s))
        if _machine_type == "cTM":
            _results.write("Settings:\nClauses:,%.1f\nThreshold:,%.1f\ns:,%.1f\nWindow_X:,%.1f\nWindow_Y:,%.1f\n" 
                           "Shape_X:,%.1f\nShape_Y:,%.1f\nShape_Z:,%.1f\n"
                           % (_clauses, _t, _s, _window_x, _window_y, _shape_x, _shape_y, _shape_z))

        return _results

    def load_data(_numb, _shape_x, _shape_y, _shape_z, _clauses, _t, _s, _window_x, _window_y,
                  _data_dim, _data_name, _timestamp_save):
        global x_train
        global y_train
        global x_test
        global y_test
        train_data = np.loadtxt("Data/K-Fold/" + data_status + "/" + _data_dim + _data_name + _numb + "train",
                                delimiter=",")
        test_data = np.loadtxt("Data/K-Fold/" + data_status + "/" + _data_dim + _data_name + _numb + "test",
                               delimiter=",")
        if _machine_type == "TM":
            x_train = train_data[:, 0:-1]
            y_train = train_data[:, -1]
            x_test = test_data[:, 0:-1]
            y_test = test_data[:, -1]
            machine = MultiClassTsetlinMachine(_clauses, _t, _s, boost_true_positive_feedback=0, weighted_clauses=True)
            print("-------------------------------------------------------------------------------------------")
            print("MultiClassTsetlinMachine using %s, %s, %s written to file %s%s_%s.csv\n"
                  % (_data_dim, data_status, _data_name, _data_dim, _data_name, _timestamp_save))
            print("Settings: Clauses: %.1f Threshold: %.1f s: %.1f\n" % (_clauses, _t, _s))
        if _machine_type == "cTM":
            x_train = train_data[:, 0:-1].reshape(train_data.shape[0], _shape_x, _shape_y, _shape_z)
            y_train = train_data[:, -1]
            x_test = test_data[:, 0:-1].reshape(test_data.shape[0], _shape_x, _shape_y, _shape_z)
            y_test = test_data[:, -1]
            machine = MultiClassConvolutionalTsetlinMachine2D(_clauses, _t, _s, (_window_x, _window_y),
                                                              boost_true_positive_feedback=0, weighted_clauses=True)
            print("-------------------------------------------------------------------------------------------")
            print("MultiClassConvolutionalTsetlinMachine2D using %s, %s, %s written to file %s%s_%s.csv "
                  "(%.1f x %.1f x %.1f)""\n"
                  % (data_dim, data_status, _data_name, _data_dim, _data_name, timestamp_save,
                     _shape_x, _shape_y, _shape_z))
            print("Settings: Clauses: %.1f Threshold: %.1f S: %.1f Window_X: %.1f Window_Y: %.1f\n" % (
                _clauses, _t, _s, _window_x, _window_y))

        results.write(data_dim + data_name + numb + ",")

        return machine

    def tm_get_output(_tm, _tm_class, _clause):
        output = []
        for i in range(_shape_x * _shape_y * 4):
            output_bit = _tm.ta_action(_tm_class, _clause, i)
            output.append(output_bit)
        return output

    def align(_tm, _tm_class, _clause, _result_clauses):
        if machine_type == "TM":
            output = tm_get_output(_tm, _tm_class, _clause)
        else:
            output = ctm_get_output(_tm, _tm_class, _clause)
        non_negated = output[:int(len(output) / 2)]
        negated = output[int(len(output) / 2):]
        w_bit = (non_negated[:int(len(non_negated) / 2)])
        b_bit = (non_negated[int(len(non_negated) / 2):])
        not_w_bit = (negated[:int(len(negated) / 2)])
        not_b_bit = (negated[int(len(negated) / 2):])
        for i in range(_shape_x * _shape_y):
            _result_clauses.write(str(w_bit[i]) + str(b_bit[i]) + str(not_w_bit[i]) + str(not_b_bit[i]))
            if i < _shape_x * _shape_y - 1:
                _result_clauses.write(",")
            else:
                _result_clauses.write("\n")

    def ctm_get_output(_tm, _tm_class, _clause):
        output = []
        xyz_id_old = 0
        for y in range(_window_y):
            for x in range(_window_x):
                for z in range(_shape_z):
                    xyz_id = offset_y + offset_x + y * _shape_x * 2 + x * 2 + z
                    output_bit = _tm.ta_action(_tm_class, _clause, xyz_id)
                    output.append(output_bit)
                    xyz_id_old = xyz_id + 1
        output = ctm_get_output_negated(_tm, _tm_class, _clause, xyz_id_old, output)
        return output

    def ctm_get_output_negated(_tm, _tm_class, _clause, _xyz_id_old, _output):
        for y in range(_window_y):
            for x in range(_window_x):
                for z in range(_shape_z):
                    xyz_id = _xyz_id_old + offset_y + offset_x + y * _shape_x * 2 + x * 2 + z
                    output_bit = _tm.ta_action(_tm_class, _clause, xyz_id)
                    _output.append(output_bit)
        return _output

    def print_class(_t, _class, _clauses, _result_clauses):
        for i in range(_clauses):
            align(_t, _class, i, _result_clauses)

    def write_clauses(_m, _clauses, _name, _machine_type, _data_dim, _data_name):
        result_clauses = open("Results/" + _name + "/" + _machine_type + "/" + _data_dim + _data_name + timestamp_save
                              + "clauses1.csv", 'a')
        print_class(_m, 1, _clauses, result_clauses)
        result_clauses.close()
        result_clauses = open("Results/" + _name + "/" + _machine_type + "/" + _data_dim + _data_name + timestamp_save
                              + "clauses0.csv", 'a')
        print_class(_m, 0, _clauses, result_clauses)
        result_clauses.close()
        if data_status == "Draw":
            result_clauses = open("Results/" + _name + "/" + _machine_type + "/" + _data_dim + _data_name
                                  + timestamp_save + "clauses2.csv", 'a')
            print_class(_m, 2, _clauses, result_clauses)
            result_clauses.close()

    def stat_calc(_epoch, _epoch_results, _epochs_total, _results, _result_total):
        mean_accuracy = np.mean(_result_total)
        print("Mean Accuracy:", round(float(mean_accuracy), 4), "\n\n")
        _results.write(",%.4f" % mean_accuracy)
        _results.write("\n")
        for j in range(_epoch):
            epoch_mean = np.mean(_epoch_results[j])
            average_epoch_results.append(round(float(epoch_mean), 2))
        single_highest_acc = max(_epochs_total)
        print("Single-highest Accuracy:", round(single_highest_acc, 2))
        max_acc = max(average_epoch_results)
        print("Max Accuracy:", round(max_acc, 2))
        avg_avg = np.mean(average_epoch_results)
        print("Average Accuracy for each epoch:", average_epoch_results)
        print("Average Accuracy total:", round(float(avg_avg), 2), "\n\n")
        _results.write("mean" + ",")
        for q in range(len(average_epoch_results)):
            _results.write(",%.4f" % average_epoch_results[q])
        _results.write(",%.4f" % avg_avg)
        _results.write(",")
        _results.write("\n")
        _results.write("singel-highest/max" + "," + ",%.4f" % single_highest_acc + ",%.4f" % max_acc + ",")

    global timestamp_save
    global epoch_results
    global average_epoch_results
    global epochs_total
    global offset_x
    global offset_y
    timestamp_save = time.strftime("%y-%m-%d_%H%M")
    epoch_results = []
    average_epoch_results = []
    epochs_total = []
    counter = 0
    results = init(_machine_type, _name, _data_dim, _data_name, _epoch, _clauses, _t, _s, _window_x,
                   _window_y, _shape_x, _shape_y, _shape_z, epoch_results, average_epoch_results,
                   epochs_total, offset_x, offset_y)
    result_total = []
    while counter < k_fold_parts:
        print("k-fold ------", str(counter) + "(" + str(counter + 1) + ")")
        global x_train
        global y_train
        global x_test
        global y_test
        numb = str(counter)
        m = load_data(numb, _shape_x, _shape_y, _shape_z,
                      _clauses, _t, _s, _window_x, _window_y, _data_dim, _data_name, timestamp_save)
        if load_state:
            m.fit(x_train, y_train, epochs=0, incremental=True)
            m.set_state(np.load(state_path + str(counter) + ".npy", allow_pickle=True))
        for i in range(_epoch):
            start = time.time()
            m.fit(x_train, y_train, epochs=1, incremental=True)
            stop = time.time()
            timestamp_epoch = time.strftime("%H:%M:%S")
            start_testing = time.time()
            result = 100 * (m.predict(x_test) == y_test).mean()
            stop_testing = time.time()
            print("#%d Time: %s Accuracy: %.2f%% Training: %.2fs Testing: %.2fs" % (
                i + 1, timestamp_epoch, result, stop - start, stop_testing - start_testing))
            result_total.append(result)
            results.write(",%.4f" % (np.mean(result)))
            epoch_results[i].append(result)
            epochs_total.append(result)
        counter += 1
        np.save("TM-State/" + _data_dim + _data_name + "_" + timestamp_save + "/"
                + "state_" + str(counter), m.get_state())
        if counter == _write_clauses and _write_clauses != 0:
            write_clauses(m, _clauses, _name, _machine_type, _data_dim, _data_name)
    stat_calc(_epoch, epoch_results, epochs_total, results, result_total)


app(epoch, clauses, Threshold, s, data_name, data_dim, machine_type, Window_X, Window_Y,
    Shape_X, Shape_Y, Shape_Z, Name, Write_Clauses)
