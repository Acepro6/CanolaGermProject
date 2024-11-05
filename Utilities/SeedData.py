import pandas as pd
import numpy as np
from Utilities import Calculator as calc
from whittaker_eilers import WhittakerSmoother


class SeedData:
    def __init__(self, title, hrs, data, config):
        self._title = title
        self._config = config
        self._data = data
        self._hrs = hrs
        self._hrs_shortened = hrs[:-9]
        self._dx = calc.excel_derivative(data, hrs)
        self._flagged = True

        # Smooth Data
        self._smoother = WhittakerSmoother(lmbda=int(self._config['Smoothing Lambda']), order=2, data_length=len(self._dx))
        self._smooth_dx = self._smoother.smooth(self._dx)

        self._crit_idx = calc.get_crit_idx(self._smooth_dx, float(self._config['Critical Threshold']))
        self._starting_index = None

    # METHODS
    def get_baseline_regression(self):
        # Get x,y subset we are interested in analyzing
        baseline_subset = self._smooth_dx[5:self._starting_index]
        bl_hrs_subset = self._hrs_shortened[5:self._starting_index]
        bl_line = np.polyfit(bl_hrs_subset, baseline_subset, 1)

        slope_subset = self._smooth_dx[self._starting_index: self._crit_idx + int(self._config['Past Threshold Reach'])]
        hrs_subset = self._hrs_shortened[self._starting_index: self._crit_idx + int(self._config['Past Threshold Reach'])]

        slope = np.polyfit(hrs_subset, slope_subset, 1)

        if len(bl_hrs_subset) < float(self._config['BL Substitute Size Limit']) or bl_line[0] > 0.000035 or slope[0] < bl_line[0] or bl_line[0] < -0.00002:
            bl_subset = np.poly1d([0, float(self._config['BL Subset Replacement'])])(self._hrs_shortened)
        else:
            bl_subset = np.poly1d(bl_line)(self._hrs_shortened)

        return bl_subset, bl_hrs_subset

    def get_slope_regression(self):
        self._starting_index = self._crit_idx
        for i in range(self._starting_index, -1, -1):
            if self._smooth_dx[i] <= float(self._config['Lower Threshold']):
                self._starting_index = i
                break

        slope_subset = self._smooth_dx[self._starting_index: self._crit_idx + int(self._config['Past Threshold Reach'])]
        hrs_subset = self._hrs_shortened[self._starting_index: self._crit_idx + int(self._config['Past Threshold Reach'])]

        slope_subset = np.poly1d(np.polyfit(hrs_subset, slope_subset, 1))(self._hrs_shortened)

        return slope_subset, hrs_subset, self._starting_index

    def get_intercept(self):
        try:
            slope_fit, _, _ = self.get_slope_regression()
            baseline_fit, _ = self.get_baseline_regression()

            idx = np.argwhere(np.diff(np.sign(slope_fit - baseline_fit))).flatten()
            x_y_int = (self._hrs_shortened[idx].values[0], np.array(self._smooth_dx)[idx][0])
            return x_y_int
        except:
            return 0

    def get_coefficient(self):

        slope_subset = self._smooth_dx[self._starting_index: self._crit_idx + int(self._config['Past Threshold Reach'])]
        hrs_subset = self._hrs_shortened[self._starting_index: self._crit_idx + int(self._config['Past Threshold Reach'])]

        return np.polyfit(hrs_subset, slope_subset, 1)[0]

    def get_OCR_avg(self):
         """
         Returns the average dx value from hours 2.5 -> 15. To get an idea of initial OCR rate before germ
         :return:
         """
         subset_y = np.array(self._dx[5:31])
         mean_y = sum(subset_y) / len(subset_y)

         return mean_y
#         """
#         Takes a regression of the first few points of data and returns the b value of y=mx+b
#         :return:
#         """
#         subset_y = np.array(self._dx[5:30])  # 24 hour period at start of experiment
#         subset_x = np.array(self._hrs[5:30])
#         mean_x = sum(subset_x) / len(subset_x)
#         mean_y = sum(subset_y) / len(subset_y)
#
#         n = 0
#
#         while n < len(subset_y):
#             sum_top = (subset_x[n] - mean_x) * (subset_y[n] - mean_y)
#             sum_bot = (subset_x[n] - mean_x) ** 2
#             n += 1
#
#         b = sum_top / sum_bot
#         b = b * -1
#
#         return b


    ########################################
    # GETTERS / SETTERS
    ########################################
    def get_title(self):
        return self._title

    def get_data(self):
        return self._data

    def get_dx(self):
        return self._dx

    def get_hrs(self):
        return self._hrs_shortened

    def flag(self, status: bool):
        self._flagged = status

    def get_flag_status(self):
        return self._flagged

    def get_crit_idx(self):
        return self._crit_idx

    def get_smooth_dx(self):
        return self._smooth_dx
