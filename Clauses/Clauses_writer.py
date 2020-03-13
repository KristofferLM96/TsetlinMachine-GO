"""
Add load of tm
Add variables needed.
Add main loop/run
"""


def write_clauses(_shape_x, _shape_y, _shape_z, _window_x, _window_y, _offset_x, _offset_y, _name, _machine_type,
                  _data_dim, _data_status, _dataset, _app_start_date, _m,):
    def tm_get_output(_tm, _tm_class, _clause):
        output = []
        for i in range(_shape_x * _shape_y * 4):
            output_bit = _tm.ta_action(_tm_class, _clause, i)
            output.append(output_bit)
        return output

    def align(_tm, _tm_class, _clause, _result_clauses):
        if _machine_type == "TM":
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
                    xyz_id = _offset_y + _offset_x + y * _shape_x * 2 + x * 2 + z
                    output_bit = _tm.ta_action(_tm_class, _clause, xyz_id)
                    output.append(output_bit)
                    xyz_id_old = xyz_id + 1
        output = ctm_get_output_negated(_tm, _tm_class, _clause, xyz_id_old, output)
        return output

    def ctm_get_output_negated(_tm, _tm_class, _clause, _xyz_id_old, _output):
        for y in range(_window_y):
            for x in range(_window_x):
                for z in range(_shape_z):
                    xyz_id = _xyz_id_old + _offset_y + _offset_x + y * _shape_x * 2 + x * 2 + z
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
        if _data_status == "Draw":
            result_clauses = open("Results/" + _name + "/" + _machine_type + "/" + _data_dim + _dataset
                                  + _app_start_date + "clauses2.csv", 'a')
            print_class(_m, 2, _clauses, result_clauses)
            result_clauses.close()