import numpy as np
import time

# Settings
clauses = 5000
Threshold = 9237
s = 127.0
epoch = 25
k_fold_parts = 1
machine_type = "TM"  # cTM or TM
parallel = True
data_status = "Draw"
data_dim = "9x9"
data_name = "Natsukaze_" + data_status
Window_X = Window_Y = 5
Shape_X = 9
Shape_Y = 9
Shape_Z = 2
Name = "Kristoffer"
Write_Clauses = 0  # 0 = don't print clauses, 1-10 which k-Fold to write clauses for.

if parallel:
    if machine_type == "TM":
        from pyTsetlinMachineParallel.tm import MultiClassTsetlinMachine
    else:
        from pyTsetlinMachineParallel.tm import MultiClassConvolutionalTsetlinMachine2D
else:
    if machine_type == "TM":
        from pyTsetlinMachine.tm import MultiClassTsetlinMachine
    else:
        from pyTsetlinMachine.tm import MultiClassConvolutionalTsetlinMachine2D

X_train = []
Y_train = []
X_test = []
Y_test = []


def runner():
    start_machine(epoch, clauses, Threshold, s, data_name, data_dim, machine_type, Window_X, Window_Y,
                  Shape_X, Shape_Y, Shape_Z, Name, Write_Clauses)


def start_machine(_epoch, _clauses, _t, _s, _data_name, _data_dim, _machine_type, _window_x, _window_y,
                  _shape_x, _shape_y, _shape_z, name, write_clauses):
    timestamp = time.strftime("%y-%m-%d_%H%M")
    results = open("Results/" + Name + "/" + machine_type + "/" + data_dim + data_name + "_" + timestamp + ".csv", 'a')

    def tm_get_output(_tm, _tm_class, _clause):
        output = []
        for i in range(_shape_x * _shape_y * 4):
            output_bit = _tm.ta_action(_tm_class, _clause, i)
            output.append(output_bit)
        return output

    def align(_tm, _tm_class, _clause):
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
        board = []
        for i in range(_shape_x * _shape_y):
            result_clauses.write(str(w_bit[i]) + str(b_bit[i]) + str(not_w_bit[i]) + str(not_b_bit[i]))
            if i < _shape_x * _shape_y - 1:
                result_clauses.write(",")
            else:
                result_clauses.write("\n")

    offset_y = Shape_Y - Window_Y
    offset_x = Shape_X - Window_X

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

    def print_class(_t, _class, _clauses):
        for i in range(_clauses):
            align(_t, _class, i)

    epoch_count = 0
    counter = 0
    if _machine_type == "TM":
        results.write("MultiClassTsetlinMachineParallel,Parallel,")
    if _machine_type == "cTM":
        results.write(
            "MultiClassConvolutionalTsetlinMachine2D,Parallel,")
    while epoch_count < _epoch:
        results.write("Epoch" + str(epoch_count + 1) + ",")
        epoch_count += 1
    results.write("\n")

    if _machine_type == "TM":
        results.write("Settings:\nClauses:,%.1f\nThreshold:,%.1f\ns:,%.1f\n" % (_clauses, _t, _s))
    if _machine_type == "cTM":
        results.write("Settings:\nClauses:,%.1f\nThreshold:,%.1f\ns:,%.1f\nWindow_X:,%.1f\nWindow_Y:,%.1f\n"
                      "Shape_X:,%.1f\nShape_Y:,%.1f\nShape_Z:,%.1f\n"
                      % (_clauses, _t, _s, _window_x, _window_y, _shape_x, _shape_y, _shape_z))

    while counter < k_fold_parts:
        global X_train
        global Y_train
        global X_test
        global Y_test
        numb = str(counter)
        train_data = np.loadtxt("Data/K-Fold/" + data_status + "/" + _data_dim + _data_name + numb + "train",
                                delimiter=",")
        test_data = np.loadtxt("Data/K-Fold/" + data_status + "/" + _data_dim + _data_name + numb + "test",
                               delimiter=",")
        if _machine_type == "TM":
            X_train = train_data[:, 0:-1]
            Y_train = train_data[:, -1]
            X_test = test_data[:, 0:-1]
            Y_test = test_data[:, -1]
            m = MultiClassTsetlinMachine(_clauses, _t, _s, boost_true_positive_feedback=0, weighted_clauses=True)
            print("-------------------------------------------------------------------------------------------")
            print("MultiClassTsetlinMachine using %s, %s written to file %s%s%s.csv\n"
                  % (_data_dim, _data_name, _data_dim, _data_name, timestamp))
            print("Settings: Clauses: %.1f Threshold: %.1f S: %.1f\n" % (_clauses, _t, _s))
        if _machine_type == "cTM":
            X_train = train_data[:, 0:-1].reshape(train_data.shape[0], _shape_x, _shape_y, _shape_z)
            Y_train = train_data[:, -1]
            X_test = test_data[:, 0:-1].reshape(test_data.shape[0], _shape_x, _shape_y, _shape_z)
            Y_test = test_data[:, -1]
            m = MultiClassConvolutionalTsetlinMachine2D(_clauses, _t, _s, (_window_x, _window_y),
                                                        boost_true_positive_feedback=0, weighted_clauses=True)
            print("-------------------------------------------------------------------------------------------")
            print("MultiClassConvolutionalTsetlinMachine2D using %s, %s written to file %s%s%s.csv "
                  "(%.1f x %.1f x %.1f)""\n"
                  % (data_dim, _data_name, _data_dim, _data_name, timestamp, _shape_x, _shape_y, _shape_z))
            print("Settings: Clauses: %.1f Threshold: %.1f S: %.1f Window_X: %.1f Window_Y: %.1f\n" % (
                _clauses, _t, _s, _window_x, _window_y))

        results.write(data_dim + data_name + numb + ",")
        for i in range(_epoch):
            start = time.time()
            m.fit(X_train, Y_train, epochs=1, incremental=True)
            stop = time.time()
            timestamp_epoch = time.strftime("%H:%M:%S")
            start_testing = time.time()
            result = 100 * (m.predict(X_test) == Y_test).mean()
            stop_testing = time.time()
            print("#%d Time: %s Accuracy: %.2f%% Training: %.2fs Testing: %.2fs" % (
                i + 1, timestamp_epoch, result, stop - start, stop_testing - start_testing))
            results.write(",%.4f" % (np.mean(result)))
        results.write("\n")
        counter += 1
        if counter == Write_Clauses:
            result_clauses = open("Results/" + Name + "/" + machine_type + "/" + data_dim + data_name + timestamp +
                                  "clauses1.csv", 'a')
            print_class(m, 1, _clauses)
            result_clauses.close()
            result_clauses = open("Results/" + Name + "/" + machine_type + "/" + data_dim + data_name + timestamp +
                                  "clauses0.csv", 'a')
            print_class(m, 0, _clauses)
            result_clauses.close()
            if data_status == "Draw":
                result_clauses = open("Results/" + Name + "/" + machine_type + "/" + data_dim + data_name + timestamp +
                                      "clauses2.csv", 'a')
                print_class(m, 2, _clauses)
                result_clauses.close()
    print("Prediction: x1 = 1, x2 = 0, ... -> y = %d" % (m.predict(np.array([[1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0]]))))
    print("Prediction: x1 = 0, x2 = 1, ... -> y = %d" % (m.predict(np.array([[0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0]]))))
    print("Prediction: x1 = 0, x2 = 0, ... -> y = %d" % (m.predict(np.array([[0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0]]))))
    print("Prediction: x1 = 1, x2 = 1, ... -> y = %d" % (m.predict(np.array([[1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0]]))))
    results.close()


runner()