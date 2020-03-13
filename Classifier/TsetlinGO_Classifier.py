import sys
import numpy as np
import time
from datetime import datetime
import os
from pyTsetlinMachineParallel.tm import MultiClassTsetlinMachine
from pyTsetlinMachineParallel.tm import MultiClassConvolutionalTsetlinMachine2D

"""
TODO: 
- Fix time left when loading tm-state.
- Comment/Document code.
- Auto push to github after n-minutes/n-epochs.
"""

"""
Settings = [
(0)clauses, 
(1)Threshold, 
(2)s, 
(3)Window_X, 
(4)Window_Y, 
(5)Shape_X, 
(6)Shape_Y, 
(7)Shape_Z, 
(8)epoch, 
(9)k_fold_parts,  # k_fold_parts 1 - 10, how many k-fold parts to go through
(10)boost,  # boost 1 = ON || 0 = OFF
(11)weighted,  # weighted True/False for weighted clauses
(12)machine_type,  # machine_type cTM or TM
(13)completion_percentage, 
(14)moves_completed, 
(15)move_threshold
]
"""
Settings = [320, 80, 40.0,
            7, 7, 9, 9, 2,
            15, 5,
            1, True,
            "TM",
            "0.75", "100", "90"]

"""
data_dims = [
normal,
using completion percentage with current results,
using completion percentage,
using moves completed,
using moves completed with threshold
]
"""
data_dims = ["9x9",
             str(Settings[13]) + "_" + "1" + "_" + "9x9",
             str(Settings[13]) + "_" + "9x9",
             str(Settings[14]) + "_" + "9x9",
             str(Settings[14]) + "_" + str(Settings[15]) + "T_" + "9x9"]
data_dim = data_dims[3]
data_name = "Aya"  # Natsukaze || Aya
dataset = data_name + "_Draw"
Name = "Kristoffer"  # Kristoffer or Trond

"""
date = [
(0)year,
(1)month,
(2)day,
(3)time
]
"""
date = ["20", "03", "10", "1215"]
load_date = str(date[0]) + "-" + str(date[1]) + "-" + str(date[2]) + "_" + str(date[3])
load_folder = "TM-State/" + Name + "/" + data_dim + dataset + "/" + load_date + "/"
load_path = load_folder + "state_"
data_path = "/home/kristoffer/Documents/"

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
last_k_fold = 0
last_epoch = 0


def app(_epoch, _clauses, _t, _s, _dataset, _data_dim, _machine_type, _window_x, _window_y,
        _shape_x, _shape_y, _shape_z, _name, _boost):
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

        while epoch_count < _epoch:
            _results.write("Epoch" + str(epoch_count + 1) + ",")
            epoch_count += 1
        _results.write("\n")

        if _machine_type == "TM":
            _results.write("Settings:\nClauses:,%.1f\nThreshold:,%.1f\ns:,%.1f\nboost:,%s\n"
                           % (_clauses, _t, _s, _boost))
        if _machine_type == "cTM":
            _results.write("Settings:\nClauses:,%.1f\nThreshold:,%.1f\ns:,%.1f\nboost:,%s\nWindow_X:,%.1f\n"
                           "Window_Y:,%.1f\nShape_X:,%.1f\nShape_Y:,%.1f\nShape_Z:,%.1f\n"
                           % (_clauses, _t, _s, _boost, _window_x, _window_y, _shape_x, _shape_y, _shape_z))
        _results.close()

        print("Settings:", "\n")
        print("Clauses:", _clauses)
        print("Threshold:", _t)
        print("s:", _s)
        print("boost:", _boost)
        print("weighted clauses:", Settings[11])
        if _machine_type == "cTM":
            print("Window X", _window_x)
            print("Window Y", _window_y)
            print("Shape X", _shape_x)
            print("Shape Y", _shape_y)
            print("Shape Z", _shape_z)
        print("\n")

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
            train_data = np.loadtxt(data_path + "Data/K-Fold/Draw" + "/" + _data_dim + _dataset + _numb + "train",
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
            test_data = np.loadtxt(data_path + "Data/K-Fold/Draw" + "/" + _data_dim + _dataset + _numb + "test",
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

            machine = MultiClassTsetlinMachine(_clauses, _t, _s, boost_true_positive_feedback=Settings[10],
                                               weighted_clauses=Settings[11])
            print("-------------------------------------------------------------------------------------------")
            print("MultiClassTsetlinMachine using %s, Draw, %s, written to file %s%s_%s.csv\n"
                  % (_data_dim, data_name, _data_dim, _dataset, _app_start_date))
            print("Settings: Clauses: %.1f Threshold: %.1f s: %.1f\n" % (_clauses, _t, _s))

        if _machine_type == "cTM":
            x_train = train_data[:, 0:-1].reshape(train_data.shape[0], _shape_x, _shape_y, _shape_z)
            y_train = train_data[:, -1]
            x_test = test_data[:, 0:-1].reshape(test_data.shape[0], _shape_x, _shape_y, _shape_z)
            y_test = test_data[:, -1]

            machine = MultiClassConvolutionalTsetlinMachine2D(_clauses, _t, _s, (_window_x, _window_y),
                                                              boost_true_positive_feedback=Settings[10],
                                                              weighted_clauses=Settings[11])
            print("-------------------------------------------------------------------------------------------")
            print("MultiClassConvolutionalTsetlinMachine2D using %s, Draw, %s, written to file %s%s_%s.csv "
                  "(%.1f x %.1f x %.1f)""\n"
                  % (data_dim, _dataset, _data_dim, _dataset, _app_start_date,
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
        avg_10_last = np.mean(average_epoch_results[-10:])
        avg_avg = np.mean(average_epoch_results)

        return single_highest_acc, max_acc, avg_avg, avg_10_last, average_epoch_results

    def write_stat(_results, _acc_highest, _acc_max, _acc_avg, _acc_avg_10_last, _acc_epochs):
        _results.write("mean/mean_10-last" + ",")
        for q in range(len(_acc_epochs)):
            _results.write(",%.4f" % _acc_epochs[q])
        _results.write(",%.4f" % _acc_avg + ",%.4f" % _acc_avg_10_last)
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
                if counter + 1 < 10 <= Settings[9]:  # Settings[9] = k_fold_parts
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
                      % (_current_k_fold, Settings[9], _current_i_load, timestamp, loaded_results))
                # Settings[9] = k_fold_parts
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
            _s = float(load_array[4][1][:-2])
            _boost = load_array[5][1][:-2]
            if machine == "cTM":
                _window_x = int(load_array[6][1][:-2])
                _window_y = int(load_array[7][1][:-2])
                _shape_x = int(load_array[8][1][:-2])
                _shape_y = int(load_array[9][1][:-2])
                _shape_z = int(load_array[10][1][:-2])
                k_fold_start = 11
            else:
                k_fold_start = 6
            result_array = []
            if len(load_array) - k_fold_start > 11:
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
    while counter < Settings[9]:  # Settings[9] = k_fold_parts
        print("k-fold ------", str(counter + 1) + " / " + str(Settings[9]))  # Settings[9] = k_fold_parts
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
            if counter + 1 < 10 <= Settings[9]:  # Settings[9] = k_fold_parts
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

            time_elapsed, time_left, estimated_finish = estimate_time(epoch_counter, _epoch, Settings[9])
            # Settings[9] = k_fold_parts
            time_elapsed = round(time_elapsed / 60, 2)
            notation_elapsed = "minutes"
            notation_left = "minutes"
            if time_elapsed > 60:
                time_elapsed = round(time_elapsed / 60, 2)
                notation_elapsed = "hours"
            time_left = round(time_left / 60, 2)
            if time_left > 60:
                time_left = round(time_left / 60, 2)
                notation_left = "hours"

            if load_state:
                print("-- %s / %s -- #%s Time: %s Accuracy: %.2f%% Training: %.2fs Testing: %.2fs "
                      "----- Elapsed time: %s %s, Time left: %s %s"
                      % (current_k_fold, Settings[9], current_i_load, timestamp_epoch, result, stop - start,
                         stop_testing - start_testing, time_elapsed, notation_elapsed, time_left, notation_left))
                # Settings[9] = k_fold_parts
                epoch_results[i + start_epoch - 1].append(round(result, 4))
            else:
                print("-- %s / %s -- #%s Time: %s Accuracy: %.2f%% Training: %.2fs Testing: %.2fs "
                      "----- Elapsed time: %s %s, Time left: %s %s"
                      % (current_k_fold, Settings[9], current_i, timestamp_epoch, result, stop - start,
                         stop_testing - start_testing, time_elapsed, notation_elapsed, time_left, notation_left))
                # Settings[9] = k_fold_parts
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
        acc_highest, acc_max, acc_avg, acc_avg_10_last, acc_epochs = stat_calc(epoch_results, epochs_total, results)
        print("Single-highest Accuracy:", round(acc_highest, 4))
        print("Max Accuracy:", round(acc_max, 4))
        print("Average Accuracy for each epoch:", acc_epochs)
        print("Average Accuracy total:", round(float(acc_avg), 4))
        print("Average Accuracy last 10 epochs:", round(float(acc_avg_10_last), 4), "\n\n")

        results.close()
        last_k_fold = counter + 1
    if _machine_type == "TM":
        results = open("Results/" + _name + "/" + _machine_type + "/" + _data_dim + _dataset + "/"
                       + _data_dim + _dataset + "_" + app_start_date + ".csv", 'a')
    elif _machine_type == "cTM":
        results = open("Results/" + _name + "/" + _machine_type + "/" + _data_dim + _dataset + "/"
                       + str(_window_x) + "x" + str(_window_y) + "/" + _data_dim + _dataset + "_"
                       + app_start_date + ".csv", 'a')
    acc_highest, acc_max, acc_avg, acc_avg_10_last, acc_epochs = stat_calc(epoch_results, epochs_total, results)
    write_stat(results, acc_highest, acc_max, acc_avg, acc_avg_10_last, acc_epochs)
    results.close()
    print("Program stopped at:", time.strftime("%d.%m.%y  %H:%M"))


"""
Settings = [
(0)clauses, 
(1)Threshold, 
(2)s, 
(3)Window_X, 
(4)Window_Y, 
(5)Shape_X, 
(6)Shape_Y, 
(7)Shape_Z, 
(8)epoch, 
(9)k_fold_parts,  # k_fold_parts 1 - 10, how many k-fold parts to go through
(10)boost,  # boost 1 = ON || 0 = OFF
(11)weighted,  # weighted True/False for weighted clauses
(12)machine_type,  # machine_type cTM or TM
(13)completion_percentage, 
(14)moves_completed, 
(15)move_threshold
]
"""
try:
    app_start = time.time()
    app(Settings[8], Settings[0], Settings[1], Settings[2], dataset, data_dim, Settings[12], Settings[3], Settings[4],
        Settings[5], Settings[6], Settings[7], Name, Settings[10])
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
    print("Last k-fold ran:", last_k_fold, " ", "Last epoch ran:", last_epoch)
    print("Last epochs saved to.. ", data_dim + dataset + "_" + app_start_date + ".csv")
    sys.exit(0)
