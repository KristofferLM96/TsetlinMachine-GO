import sys
import numpy as np
import time
from datetime import datetime
import os
from pyTsetlinMachineParallel.tm import MultiClassTsetlinMachine
from pyTsetlinMachineParallel.tm import MultiClassConvolutionalTsetlinMachine2D

"""
TODO: 
- Comment/Document code.
- Auto push to github after n-minutes/n-epochs.
"""

# Settings
clauses = 32000
Threshold = 16000
s = 150.0
epoch = 15
k_fold_parts = 1  # 1 - 10, how many k-fold parts to go through
machine_type = "cTM"  # cTM or TM
data_status = "Draw"  # Draw or No-Draw
completion_percentage = "0.75"
data_dims = ["9x9", completion_percentage + "_" + "1" + "_" + "9x9", completion_percentage + "_" + "9x9"]
data_dim = data_dims[2]
data_name = "Aya"  # Natsukaze_ || Aya_
dataset = data_name + "_" + data_status
Window_X = 7
Window_Y = 7
Shape_X = Shape_Y = 9  # Depending on data_dim
Shape_Z = 2  # 3D board
Name = "Kristoffer"  # Kristoffer or Trond
Write_Clauses = False
# Clauses_to_write = 1  # 1-10 which k-Fold to write clauses for.
year = "20"
month = "02"
day = "25"
time_point = "0911"
load_date = year + "-" + month + "-" + day + "_" + time_point
load_folder = "TM-State/" + Name + "/" + data_dim + dataset + "/" + load_date + "/"
load_path = load_folder + "state_"
load_state = False
save_state = True

x_train = []
y_train = []
x_test = []
y_test = []
epoch_results = []
average_epoch_results = []
epochs_total = []
app_start_date = ""
app_start_date_formatted = ""
data_train_load = 0
data_test_load = 0
app_start = 0
app_stop = 0
offset_y = 0
offset_x = 0
last_k_fold = 0
last_epoch = 0


def app(_epoch, _clauses, _t, _s, _dataset, _data_dim, _machine_type, _window_x, _window_y,
        _shape_x, _shape_y, _shape_z, _name, _write_clauses):
    global app_start_date
    global app_start_date_formatted
    print("#################################################################################################")
    print("#                                                                                               #")
    print("#           (っ◔◡◔)っ ♥  Ｔｓｅｔｌｉｎ Ｍａｃｈｉｎｅ Ｃｌａｓｓｉｆｉｃａｔｉｏｎ  ♥ と(◔◡◔と)         #")
    print("#                                            －－ －－ －－                                       #")
    print("#                                        ＧＯ Ｂｏａｒｄ Ｇａｍｅ                                  #")
    print("#                                                                                               #")
    print("#################################################################################################")
    print("\n\n")
    app_start_date = time.strftime("%y-%m-%d_%H%M")
    app_start_date_formatted = time.strftime("%d.%m.%Y  %H:%M")
    print("Program started at:", app_start_date_formatted, "\n\n")

    def init(_epoch_results):
        global offset_x
        global offset_y
        epoch_count = 0
        for i in range(_epoch):
            _epoch_results.append([])
        if _machine_type == "TM":
            print("Creating result file in.. ", "Results/" + _name + "/" + _machine_type + "/"
                  + _data_dim + _dataset + "/" + _data_dim + _dataset + "_" + app_start_date + ".csv", "\n\n")
            os.makedirs(os.path.dirname("Results/" + _name + "/" + _machine_type + "/" + _data_dim + _dataset + "/"
                                        + _data_dim + _dataset + "_" + app_start_date + ".csv"), exist_ok=True)
            _results = open("Results/" + _name + "/" + _machine_type + "/" + _data_dim + _dataset + "/"
                            + _data_dim + _dataset + "_" + app_start_date + ".csv", 'a')
            _results.write("MultiClassTsetlinMachineParallel,Parallel,")
        elif _machine_type == "cTM":
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

        offset_y = _shape_y - _window_y
        offset_x = _shape_x - _window_x
        while epoch_count < _epoch:
            _results.write("Epoch" + str(epoch_count + 1) + ",")
            epoch_count += 1
        _results.write("\n")

        if _machine_type == "TM":
            _results.write("Settings:\nClauses:,%.1f\nThreshold:,%.1f\ns:,%.1f\n" % (_clauses, _t, _s))
        if _machine_type == "cTM":
            _results.write("Settings:\nClauses:,%.1f\nThreshold:,%.1f\ns:,%.1f\nWindow_X:,%.1f\nWindow_Y:,%.1f\n" 
                           "Shape_X:,%.1f\nShape_Y:,%.1f\nShape_Z:,%.1f\n"
                           % (_clauses, _t, _s, _window_x, _window_y, _shape_x, _shape_y, _shape_z))
        _results.close()

    def load_data(_numb, _app_start_date):
        global x_train
        global y_train
        global x_test
        global y_test
        global data_test_load
        global data_train_load

        checkpoint_start = time.time()
        try:
            print("Loading training dataset..")
            train_data = np.loadtxt("Data/K-Fold/" + data_status + "/" + _data_dim + _dataset + _numb + "train",
                                    delimiter=",")
        except FileNotFoundError:
            print("Error. File not found, could not load training dataset.")
            sys.exit(0)
        checkpoint_stop = time.time()
        data_train_load = checkpoint_stop - checkpoint_start
        print("Training dataset loaded.          It took:", round(data_train_load, 2), "seconds.")
        checkpoint_start = time.time()
        try:
            print("Loading testing dataset..")
            test_data = np.loadtxt("Data/K-Fold/" + data_status + "/" + _data_dim + _dataset + _numb + "test",
                                   delimiter=",")
        except FileNotFoundError:
            print("Error. File not found, could not load testing dataset.")
            sys.exit(0)
        checkpoint_stop = time.time()
        data_test_load = checkpoint_stop - checkpoint_start
        print("Testing dataset loaded.           It took:", round(data_test_load, 2), "seconds.")

        if _machine_type == "TM":
            x_train = train_data[:, 0:-1]
            y_train = train_data[:, -1]
            x_test = test_data[:, 0:-1]
            y_test = test_data[:, -1]

            machine = MultiClassTsetlinMachine(_clauses, _t, _s, boost_true_positive_feedback=0, weighted_clauses=True)
            print("-------------------------------------------------------------------------------------------")
            print("MultiClassTsetlinMachine using %s, %s, %s, written to file %s%s_%s.csv\n"
                  % (_data_dim, data_status, data_name, _data_dim, _dataset, _app_start_date))
            print("Settings: Clauses: %.1f Threshold: %.1f s: %.1f\n" % (_clauses, _t, _s))

        if _machine_type == "cTM":
            x_train = train_data[:, 0:-1].reshape(train_data.shape[0], _shape_x, _shape_y, _shape_z)
            y_train = train_data[:, -1]
            x_test = test_data[:, 0:-1].reshape(test_data.shape[0], _shape_x, _shape_y, _shape_z)
            y_test = test_data[:, -1]

            machine = MultiClassConvolutionalTsetlinMachine2D(_clauses, _t, _s, (_window_x, _window_y),
                                                              boost_true_positive_feedback=0, weighted_clauses=True)
            print("-------------------------------------------------------------------------------------------")
            print("MultiClassConvolutionalTsetlinMachine2D using %s, %s, %s, written to file %s%s_%s.csv "
                  "(%.1f x %.1f x %.1f)""\n"
                  % (data_dim, data_status, _dataset, _data_dim, _dataset, _app_start_date,
                     _shape_x, _shape_y, _shape_z))
            print("Settings: Clauses: %.1f Threshold: %.1f S: %.1f Window_X: %.1f Window_Y: %.1f\n" % (
                _clauses, _t, _s, _window_x, _window_y))
        if _machine_type == "TM":
            _results = open("Results/" + _name + "/" + _machine_type + "/" + _data_dim + _dataset + "/"
                            + _data_dim + _dataset + "_" + _app_start_date + ".csv", 'a')
            _results.write(_data_dim + _dataset + _numb + ",")
            _results.close()
        elif _machine_type == "cTM":
            _results = open("Results/" + _name + "/" + _machine_type + "/" + _data_dim + _dataset + "/"
                            + str(_window_x) + "x" + str(_window_y) + "/"
                            + _data_dim + _dataset + "_" + _app_start_date + ".csv", 'a')
            _results.write(_data_dim + _dataset + _numb + ",")
            _results.close()

        return machine

    def stat_calc(_epoch_results, _epochs_total, _results):
        global average_epoch_results
        average_epoch_results = []
        for j in range(_epoch):
            epoch_mean = np.mean(_epoch_results[j])
            average_epoch_results.append(round(float(epoch_mean), 4))
        single_highest_acc = max(_epochs_total)
        max_acc = max(average_epoch_results)
        avg_avg = np.mean(average_epoch_results)

        return single_highest_acc, max_acc, avg_avg, average_epoch_results

    def write_stat(_results, _acc_highest, _acc_max, _acc_avg, _acc_epochs):
        _results.write("mean" + ",")
        for q in range(len(_acc_epochs)):
            _results.write(",%.4f" % _acc_epochs[q])
        _results.write(",%.4f" % _acc_avg)
        _results.write("\n")
        _results.write("single-highest/max" + "," + ",%.4f" % _acc_highest + ",%.4f" % _acc_max + ",")

    def save_tm_state(_m, _x_train, _y_train):
        try:
            _m.fit(_x_train, _y_train, epochs=0, incremental=True)
            os.makedirs("TM-State/" + Name + "/" + _data_dim + _dataset + "/" + app_start_date + "/",
                        exist_ok=True)
            np.save("TM-State/" + Name + "/" + _data_dim + _dataset + "/" + app_start_date + "/"
                    + "state_" + str(counter), _m.get_state())
        except FileNotFoundError:
            print("Could not save file. File or directory not found.")
            sys.exit(0)

    def load_tm_state(_m, _x_train, _y_train, _start_epoch, _clauses, _t, _s, _window_x, _window_y, _shape_x, _shape_y,
                      _shape_z):
        global load_state
        _start_epoch = 1
        try:
            _tm_state = np.load(load_path + str(counter) + ".npy", allow_pickle=True)
        except FileNotFoundError:
            print("Could not load TM state. File or directory not found.")
            load_state = False
            return _start_epoch
        _m.fit(_x_train, _y_train, epochs=0, incremental=True)
        _m.set_state(_tm_state)
        loaded_results_list = load_results(_clauses, _t, _s, _window_x, _window_y, _shape_x, _shape_y, _shape_z)
        _start_epoch = set_results(_start_epoch, loaded_results_list)

        return _start_epoch

    def set_results(_start_epoch, _loaded_results_list):
        global last_epoch
        if len(_loaded_results_list) >= counter + 1:
            for i in range(len(_loaded_results_list[counter])):
                loaded_results = float(_loaded_results_list[counter][i])
                timestamp = time.strftime("%H:%M:%S")
                if counter + 1 < 10 <= k_fold_parts:
                    _current_k_fold = "0" + str(counter + 1)
                else:
                    _current_k_fold = str(counter + 1)
                if _epoch < 10:
                    _current_i_load = str(i + start_epoch + 1)
                elif 10 <= _epoch < 100:
                    if (i + 1) < 10:
                        _current_i_load = "0" + str(i + start_epoch + 1)
                    else:
                        _current_i_load = str(i + start_epoch + 1)
                elif 100 <= _epoch:
                    if (i + 1) < 10:
                        _current_i_load = "00" + str(i + start_epoch + 1)
                    elif 10 < (i + 1) < 100:
                        _current_i_load = "0" + str(i + start_epoch + 1)
                    else:
                        _current_i_load = str(i + start_epoch + 1)
                print("-- %s / %s -- #%s Time: %s Accuracy: %.2f%% --loaded--"
                      % (_current_k_fold, k_fold_parts, _current_i_load, timestamp, loaded_results))
                results.write(",%.4f" % loaded_results)
                _start_epoch += 1
                last_epoch += 1
                result_total.append(loaded_results)
                epoch_results[i].append(loaded_results)
                epochs_total.append(loaded_results)

        return _start_epoch

    def load_results(_clauses, _t, _s, _window_x, _window_y, _shape_x, _shape_y, _shape_z):
        if _machine_type == "TM":
            path = "Results/" + _name + "/" + _machine_type + "/" + _data_dim + _dataset + "/" \
                   + _data_dim + _dataset + "_" + load_date + ".csv"
        elif _machine_type == "cTM":
            path = "Results/" + _name + "/" + _machine_type + "/" + _data_dim + _dataset + "/" + str(_window_x) + "x" \
                   + str(_window_y) + "/" + _data_dim + _dataset + "_" + load_date + ".csv"
        with open(path, "r") as file_load:
            load_array = []
            for line in file_load.readlines():
                line_stripped = [str(x) for x in line.strip().split(",")]
                if line_stripped[-1] == "":
                    load_array.append(line_stripped[:-1])
                else:
                    load_array.append(line_stripped)
            if load_array[0][0][10] == "T":
                machine = "TM"
            else:
                machine = "cTM"
            _clauses = int(load_array[2][1][:-2])
            _t = int(load_array[3][1][:-2])
            _s = int(load_array[4][1][:-2])
            if machine == "cTM":
                _window_x = int(load_array[5][1][:-2])
                _window_y = int(load_array[6][1][:-2])
                _shape_x = int(load_array[7][1][:-2])
                _shape_y = int(load_array[8][1][:-2])
                _shape_z = int(load_array[9][1][:-2])
                k_fold_start = 10
            else:
                k_fold_start = 5
            result_array = []
            if len(load_array) - k_fold_start > 10:
                for i in range(len(load_array) - k_fold_start - 2):
                    result_array.append(load_array[i + k_fold_start][2:])
            else:
                for i in range(len(load_array) - k_fold_start):
                    result_array.append(load_array[i + k_fold_start][2:])
            return result_array

    def estimate_time(_epoch_counter, _epoch, _k_fold_parts):
        global app_start
        global data_train_load
        global data_test_load

        current_time = time.time()
        elapsed_time = current_time - app_start
        est_time = (elapsed_time / _epoch_counter) * (_epoch * _k_fold_parts)
        # finish_time = app_start + est_time
        time_left = est_time - elapsed_time
        finish_time = time.time() + time_left
        est_timestamp = datetime.fromtimestamp(finish_time).strftime("%d.%m.%Y  %H:%M")
        return elapsed_time, time_left, est_timestamp

    global epoch_results
    global average_epoch_results
    global epochs_total
    global offset_x
    global offset_y
    global last_k_fold
    global last_epoch
    global time_taken
    epoch_results = []
    average_epoch_results = []
    epochs_total = []
    counter = 0
    init(epoch_results)
    result_total = []
    epoch_counter = 0
    while counter < k_fold_parts:
        print("k-fold ------", str(counter + 1) + " / " + str(k_fold_parts))
        global x_train
        global y_train
        global x_test
        global y_test
        numb = str(counter)
        start_epoch = 0
        last_epoch = 0
        m = load_data(numb, app_start_date)
        epoch_range = _epoch
        if load_state:
            if _machine_type == "TM":
                results = open("Results/" + _name + "/" + _machine_type + "/" + _data_dim + _dataset + "/"
                               + _data_dim + _dataset + "_" + app_start_date + ".csv", 'a')
            elif _machine_type == "cTM":
                results = open("Results/" + _name + "/" + _machine_type + "/" + _data_dim + _dataset + "/"
                               + str(_window_x) + "x" + str(_window_y) + "/" + _data_dim + _dataset + "_"
                               + app_start_date + ".csv", 'a')
            start_epoch = load_tm_state(m, x_train, y_train, start_epoch, _clauses, _t, _s, _window_x, _window_y,
                                        _shape_x, _shape_y, _shape_z)
            epoch_range = _epoch - start_epoch + 1
            results.close()
            if save_state:
                save_tm_state(m, x_train, y_train)
        for i in range(epoch_range):
            epoch_counter += 1
            if _machine_type == "TM":
                results = open("Results/" + _name + "/" + _machine_type + "/" + _data_dim + _dataset + "/"
                               + _data_dim + _dataset + "_" + app_start_date + ".csv", 'a')
            elif _machine_type == "cTM":
                results = open("Results/" + _name + "/" + _machine_type + "/" + _data_dim + _dataset + "/"
                               + str(_window_x) + "x" + str(_window_y) + "/" + _data_dim + _dataset + "_"
                               + app_start_date + ".csv", 'a')
            start = time.time()
            m.fit(x_train, y_train, epochs=1, incremental=True)
            stop = time.time()
            timestamp_epoch = time.strftime("%H:%M:%S")
            start_testing = time.time()
            result = 100 * (m.predict(x_test) == y_test).mean()
            stop_testing = time.time()
            if counter + 1 < 10 <= k_fold_parts:
                current_k_fold = "0" + str(counter + 1)
            else:
                current_k_fold = str(counter + 1)
            if _epoch < 10:
                current_i_load = str(i + start_epoch + 1)
                current_i = str(i + 1)
            elif 10 <= _epoch < 100:
                if (i + 1) < 10:
                    current_i_load = "0" + str(i + start_epoch + 1)
                    current_i = "0" + str(i + 1)
                else:
                    current_i_load = str(i + start_epoch + 1)
                    current_i = str(i + 1)
            elif 100 <= _epoch:
                if (i + 1) < 10:
                    current_i_load = "00" + str(i + start_epoch + 1)
                    current_i = "00" + str(i + 1)
                elif 10 < (i + 1) < 100:
                    current_i_load = "0" + str(i + start_epoch + 1)
                    current_i = "0" + str(i + 1)
                else:
                    current_i_load = str(i + start_epoch + 1)
                    current_i = str(i + 1)

            time_elapsed, time_left, estimated_finish = estimate_time(epoch_counter, _epoch, k_fold_parts)
            time_elapsed = round(time_elapsed / 60, 2)
            notation = "minutes"
            if time_elapsed > 60:
                time_elapsed = round(time_elapsed / 60, 2)
                notation = "hours"
            time_left = round(time_left / 60, 2)
            if time_left > 60:
                time_left = round(time_left / 60, 2)

            if load_state:
                print("-- %s / %s -- #%s Time: %s Accuracy: %.2f%% Training: %.2fs Testing: %.2fs "
                      "----- Elapsed time: %s %s, Time left: %s %s"
                      % (current_k_fold, k_fold_parts, current_i_load, timestamp_epoch, result, stop - start,
                         stop_testing - start_testing, time_elapsed, notation, time_left, notation))
                epoch_results[i + start_epoch - 1].append(round(result, 4))
            else:
                print("-- %s / %s -- #%s Time: %s Accuracy: %.2f%% Training: %.2fs Testing: %.2fs "
                      "----- Elapsed time: %s %s, Time left: %s %s"
                      % (current_k_fold, k_fold_parts, current_i, timestamp_epoch, result, stop - start,
                         stop_testing - start_testing, time_elapsed, notation, time_left, notation))
                epoch_results[i].append(round(result, 4))

            result_total.append(round(result, 4))
            epochs_total.append(round(result, 4))
            results.write("," + str(round(result, 4)))
            if save_state:
                save_tm_state(m, x_train, y_train)
            last_epoch = i + 1
            results.close()
        if _machine_type == "TM":
            results = open("Results/" + _name + "/" + _machine_type + "/" + _data_dim + _dataset + "/"
                           + _data_dim + _dataset + "_" + app_start_date + ".csv", 'a')
        elif _machine_type == "cTM":
            results = open("Results/" + _name + "/" + _machine_type + "/" + _data_dim + _dataset + "/"
                           + str(_window_x) + "x" + str(_window_y) + "/" + _data_dim + _dataset + "_"
                           + app_start_date + ".csv", 'a')
        results.write("\n")
        mean_accuracy = np.mean(result_total)
        print("Mean Accuracy for k-fold -", counter + 1, ":", round(float(mean_accuracy), 4), "\n")
        counter += 1
        if _write_clauses:
            write_clauses(_shape_x, _shape_y, _shape_z, _window_x, _window_y, _name, _machine_type, _data_dim,
                          _dataset, app_start_date, m)
        acc_highest, acc_max, acc_avg, acc_epochs = stat_calc(epoch_results, epochs_total, results)
        print("Single-highest Accuracy:", round(acc_highest, 4))
        print("Max Accuracy:", round(acc_max, 4))
        print("Average Accuracy for each epoch:", acc_epochs)
        print("Average Accuracy total:", round(float(acc_avg), 4), "\n\n")

        results.close()
        last_k_fold = counter + 1
    if _machine_type == "TM":
        results = open("Results/" + _name + "/" + _machine_type + "/" + _data_dim + _dataset + "/"
                       + _data_dim + _dataset + "_" + app_start_date + ".csv", 'a')
    elif _machine_type == "cTM":
        results = open("Results/" + _name + "/" + _machine_type + "/" + _data_dim + _dataset + "/"
                       + str(_window_x) + "x" + str(_window_y) + "/" + _data_dim + _dataset + "_"
                       + app_start_date + ".csv", 'a')
    acc_highest, acc_max, acc_avg, acc_epochs = stat_calc(epoch_results, epochs_total, results)
    write_stat(results, acc_highest, acc_max, acc_avg, acc_epochs)
    results.close()
    print("Program stopped at:", time.strftime("%d.%m.%y  %H:%M"))


def write_clauses(_shape_x, _shape_y, _shape_z, _window_x, _window_y, _name, _machine_type, _data_dim, _dataset,
                  _app_start_date, _m):
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

        result_clauses = open("Results/" + _name + "/" + _machine_type + "/" + _data_dim + _dataset + _app_start_date
                              + "clauses1.csv", 'a')
        print_class(_m, 1, _clauses, result_clauses)
        result_clauses.close()
        result_clauses = open("Results/" + _name + "/" + _machine_type + "/" + _data_dim + _dataset + _app_start_date
                              + "clauses0.csv", 'a')
        print_class(_m, 0, _clauses, result_clauses)
        result_clauses.close()
        if data_status == "Draw":
            result_clauses = open("Results/" + _name + "/" + _machine_type + "/" + _data_dim + _dataset
                                  + _app_start_date + "clauses2.csv", 'a')
            print_class(_m, 2, _clauses, result_clauses)
            result_clauses.close()


try:
    app_start = time.time()
    app(epoch, clauses, Threshold, s, dataset, data_dim, machine_type, Window_X, Window_Y,
        Shape_X, Shape_Y, Shape_Z, Name, Write_Clauses)
    app_stop = time.time()
    time_taken = app_stop - app_start
    if 3600 > time_taken > 60:
        time_taken = time_taken / 60
        print("It took", round(time_taken, 2), "minutes to finish the program.")
    elif time_taken > 3600:
        time_taken = time_taken / (60 * 60)
        print("It took", round(time_taken, 2), "hours to finish the program.")
    else:
        print("It took", round(time_taken, 2), "seconds to finish the program.")
except KeyboardInterrupt:
    print("\n\n")
    print("Aborted.. stopped by force.", "\n")
    if not last_k_fold == 0:
        print("Last k-fold ran:", last_k_fold, " ", "Last epoch ran:", last_epoch)
        print("Last epochs saved to.. ", data_dim + dataset + "_" + app_start_date + ".csv")
    sys.exit(0)
