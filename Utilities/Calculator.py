import numpy as np


def single_derivative(data_frame, hrs):
    derivative_data = []
    known_x = hrs
    value = 0
    step_size = 10

    while value <= len(data_frame) - step_size:
        subset_x = known_x[value:value + step_size]
        subset_y = data_frame[value:value + step_size]
        sum_top = 0
        sum_bot = 0
        mean_x = sum(subset_x) / len(subset_x)
        mean_y = sum(subset_y) / len(subset_y)
        n = value
        while n < value + 10:
            sum_top = (subset_x[n] - mean_x) * (subset_y[n] - mean_y)
            sum_bot = (subset_x[n] - mean_x) ** 2
            n += 1
        b = sum_top / sum_bot
        b = b * -1
        value += 1
        derivative_data.append(b)

    return derivative_data


def excel_derivative(data_frame, hrs):
    # Parameters
    derivative_data = []
    known_x = hrs
    value = 0
    step_size = 10

    while value <= len(data_frame) - step_size:
        # Get Subset
        subset_x = known_x[value:value + step_size]
        subset_y = data_frame[value:value + step_size]
        # Get Regression
        reg_line = np.poly1d(np.polyfit(subset_x, subset_y, 1))(subset_x)
        reg_line = np.array(reg_line) * -1

        sum_top = 0
        sum_bot = 0
        mean_x = sum(subset_x) / len(subset_x)
        mean_y = sum(reg_line) / len(reg_line)
        n = value

        # Do Calc on Regression
        while n < value + 10:
            x = 0
            sum_top = (subset_x[n] - mean_x) * (reg_line[x] - mean_y)
            sum_bot = (subset_x[n] - mean_x) ** 2
            n += 1
            x += 1
        b = sum_top / sum_bot
        b = b * -1
        value += 1

        # Add to return list
        derivative_data.append(b)

    # Return New DX Data
    return derivative_data


def get_crit_idx(data, threshold):
    # Parameter
    crit_idx = None

    # Start Search
    for idx in range(len(data[15:])):
        sub_set = data[15:]
        if sub_set[idx] > threshold:
            # Add 5 to adjust for offset
            crit_idx = idx + 5
            break

    return crit_idx
