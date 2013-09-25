"""
SPC Statistical Process Control provides means to monitor process behaviour
using statistical tools defined by Shewhart and others. The process run is shown
as Quality Control Charts (QCC).

Author: Michal Nowikowski <godfryd@gmail.com>

License: MIT
"""

import numpy

CHART_X_BAR_R_X = "Xbar R - X"
CHART_X_BAR_R_R = "Xbar R - R"
CHART_X_BAR_S_X = "Xbar S - X"
CHART_X_BAR_S_S = "Xbar S - S"
CHART_X_MR_X = "X mR - X"
CHART_X_MR_MR = "X mR - mR"
CHART_P = "p"
CHART_NP = "np"
CHART_C = "c"
CHART_U = "u"
CHART_EWMA = "EWMA"
CHART_CUSUM = "CUSUM"
CHART_THREE_WAY = "three way"
CHART_TIME_SERIES = "time series"

RULES_1_BEYOND_3SIGMA = "1 beyond 3*sigma"
RULES_2_OF_3_BEYOND_2SIGMA = "2 of 3 beyond 2*sigma"
RULES_4_OF_5_BEYOND_1SIGMA = "4 of 5 beyond 1*sigma"
RULES_7_ON_ONE_SIDE = "7 on one side"
RULES_8_ON_ONE_SIDE = "8 on one side"
RULES_9_ON_ONE_SIDE = "9 on one side"
RULES_6_TRENDING = "6 trending"
RULES_14_UP_DOWN = "14 up down"
RULES_15_BELOW_1SIGMA = "15 below 1*sigma"
RULES_8_BEYOND_1SIGMA_BOTH_SIDES = "8 beyond 1*sigma on both sides"

RULES_BASIC = [RULES_1_BEYOND_3SIGMA,
               RULES_7_ON_ONE_SIDE]
RULES_WECO = [RULES_1_BEYOND_3SIGMA,
              RULES_2_OF_3_BEYOND_2SIGMA,
              RULES_4_OF_5_BEYOND_1SIGMA,
              RULES_8_ON_ONE_SIDE,
              RULES_6_TRENDING, RULES_14_UP_DOWN]
RULES_NELSON = [RULES_1_BEYOND_3SIGMA,
                RULES_9_ON_ONE_SIDE,
                RULES_6_TRENDING,
                RULES_14_UP_DOWN,
                RULES_2_OF_3_BEYOND_2SIGMA,
                RULES_4_OF_5_BEYOND_1SIGMA,
                RULES_15_BELOW_1SIGMA,
                RULES_8_BEYOND_1SIGMA_BOTH_SIDES]

RULES_ALL = [RULES_1_BEYOND_3SIGMA,
             RULES_2_OF_3_BEYOND_2SIGMA,
             RULES_4_OF_5_BEYOND_1SIGMA,
             RULES_7_ON_ONE_SIDE,
             RULES_8_ON_ONE_SIDE,
             RULES_6_TRENDING,
             RULES_14_UP_DOWN,
             RULES_15_BELOW_1SIGMA,
             RULES_8_BEYOND_1SIGMA_BOTH_SIDES]

def test_beyond_limits(data, center, lcl, ucl):
    return data[0] > ucl or data[0] < lcl

def test_violating_runs(data, center, lcl, ucl):
    for i in xrange(1, len(data)):
        if (data[i-1] - center)*(data[i] - center) < 0:
            return False
    return True

# n         2      3      4      5      6      7      8      9      10
A2 = [0,0, 1.880, 1.023, 0.729, 0.577, 0.483, 0.419, 0.373, 0.337, 0.308]
D3 = [0,0, 0,     0,     0,     0,     0,     0.076, 0.136, 0.184, 0.223]
D4 = [0,0, 3.267, 2.575, 2.282, 2.115, 2.004, 1.924, 1.864, 1.816, 1.777]
# n   0 1      2      3      4      5      6      7      8      9     10     11     12     13     14     15       20     25
c4 = [0,0,0.7979,0.8862,0.9213,0.9400,0.9515,0.9594,0.9650,0.9693,0.9727,0.9754,0.9776,0.9794,0.9810,0.9823]#,0.9869,0.9896]
B3 = [0,0,     0,     0,     0,     0, 0.030, 0.118, 0.185, 0.239, 0.284, 0.321, 0.354, 0.382, 0.406, 0.428]#, 0.510, 0.565]
B4 = [0,0, 3.267, 2.568, 2.266, 2.089, 1.970, 1.882, 1.815, 1.761, 1.716, 1.679, 1.646, 1.618, 1.594, 1.572]#, 1.490, 1.435]
B5 = [0,0,     0,     0,     0,     0, 0.029, 0.113, 0.179, 0.232, 0.276, 0.313, 0.346, 0.374, 0.399, 0.421]#, 0.504, 0.559]
B6 = [0,0, 2.606, 2.276, 2.088, 1.964, 1.874, 1.806, 1.751, 1.707, 1.669, 1.637, 1.610, 1.585, 1.563, 1.544]#, 1.470, 1.420]
A3 = [0,0, 2.659, 1.954, 1.628, 1.427, 1.287, 1.182, 1.099, 1.032, 0.975, 0.927, 0.886, 0.850, 0.817, 0.789]#, 0.680, 0.606]

def get_stats_x_mr_x(data, size):
    assert size == 1
    center = numpy.mean(data)
    sd = 0
    for i in xrange(len(data)-1):
        sd += abs(data[i] - data[i+1])
    sd /= len(data) - 1
    d2 = 1.128
    lcl = center - 3*sd/d2
    ucl = center + 3*sd/d2
    return center, lcl, ucl

def get_stats_x_mr_mr(data, size):
    assert size == 1
    sd = 0
    for i in xrange(len(data)-1):
        sd += abs(data[i] - data[i+1])
    sd /= len(data) - 1
    d2 = 1.128
    center = sd
    lcl = 0
    ucl = center + 3*sd/d2
    return center, lcl, ucl

def get_stats_x_bar_r_x(data, size):
    n = size
    assert n >= 2
    assert n <= 10

    Rsum = 0
    for xset in data:
        assert len(xset) == n
        Rsum += max(xset) - min(xset)
    Rbar = Rsum / len(data)

    Xbar = numpy.mean(data)

    center = Xbar
    lcl = center - A2[n]*Rbar
    ucl = center + A2[n]*Rbar
    return center, lcl, ucl

def get_stats_x_bar_r_r(data, size):
    n = size
    assert n >= 2
    assert n <= 10

    Rsum = 0
    for xset in data:
        assert len(xset) == n
        Rsum += max(xset) - min(xset)
    Rbar = Rsum / len(data)

    center = Rbar
    lcl = D3[n]*Rbar
    ucl = D4[n]*Rbar
    return center, lcl, ucl

def get_stats_x_bar_s_x(data, size):
    n = size
    assert n >= 2
    assert n <= 10

    Sbar = numpy.mean(numpy.std(data, 1, ddof=1))
    Xbar = numpy.mean(data)

    center = Xbar
    lcl = center - A3[n]*Sbar
    ucl = center + A3[n]*Sbar
    return center, lcl, ucl

def get_stats_x_bar_s_s(data, size):
    n = size
    assert n >= 2
    assert n <= 10

    Sbar = numpy.mean(numpy.std(data, 1, ddof=1))

    center = Sbar
    lcl = B3[n]*Sbar
    ucl = B4[n]*Sbar
    return center, lcl, ucl

def get_stats_p(data, size):
    n = size
    assert n > 1

    pbar = float(sum(data)) / (n * len(data))
    sd = numpy.sqrt(pbar*(1-pbar)/n)

    center = pbar
    lcl = center - 3*sd
    if lcl < 0:
        lcl = 0
    ucl = center + 3*sd
    if ucl > 1:
        ucl = 1.0
    return center, lcl, ucl

def get_stats_np(data, size):
    n = size
    assert n > 1

    pbar = float(sum(data)) / (n * len(data))
    sd = numpy.sqrt(n*pbar*(1-pbar))

    center = n*pbar
    lcl = center - 3*sd
    if lcl < 0:
        lcl = 0
    ucl = center + 3*sd
    if ucl > n:
        ucl = n
    return center, lcl, ucl

def get_stats_c(data, size):
    cbar = numpy.mean(data)

    center = cbar
    lcl = center - 3*numpy.sqrt(cbar)
    if lcl < 0:
        lcl = 0
    ucl = center + 3*numpy.sqrt(cbar)
    return center, lcl, ucl

def get_stats_u(data, size):
    n = size
    assert n > 1

    cbar = float(sum(data))/(len(data)*n)

    center = cbar
    lcl = center - 3*numpy.sqrt(cbar/n)
    if lcl < 0:
        lcl = 0
    ucl = center + 3*numpy.sqrt(cbar/n)
    return center, lcl, ucl

def get_stats_cusum(data, size):
    """
    Find the data for a cusum graph

    Only returns 0 as the center as the data is moved
    its mean and ucl and lcl are not reported
    """
    return 0, None, None

def prepare_data_none(data, size):
    return data

def prepare_data_x_bar_rs_x(data, size):
    data2 = []
    for xset in data:
        data2.append(numpy.mean(xset))
    return data2

def prepare_data_x_bar_r_r(data, size):
    data2 = []
    for xset in data:
        data2.append(max(xset) - min(xset))
    return data2

def prepare_data_x_bar_s_s(data, size):
    data2 = []
    for xset in data:
        data2.append(numpy.std(xset, ddof=1))
    return data2

def prepare_data_x_mr(data, size):
    data2 = [0]
    for i in xrange(len(data)-1):
        data2.append(abs(data[i] - data[i+1]))
    return data2

def prepare_data_p(data, size):
    data2 = [0]
    for d in data:
        data2.append(float(d)/size)
    return data2

def prepare_data_u(data, size):
    data2 = [0]
    for d in data:
        data2.append(float(d)/size)
    return data2

def prepare_data_cusum(data, size, target = None):
    """
    Prepares the data for a CUSUM graph

    subtracts the mean from each data point
    then calculates the culumative sum of each
    $S_m=\sum_{i=1}^m (x_i-\mu)$
    where $x_i$ is the data point
    $\mu$ is the target value

    if $\mu is not provided the mean of the sample is used
    """
    data2 = []
    if target is None:
        target = numpy.mean(data)
    for d in data:
        data2.append(float(d) - target)
    data3 = [sum(data2[:i]) for i in xrange(len(data2)+1)]
    return data3

STATS_FUNCS = {
    CHART_X_BAR_R_X: (get_stats_x_bar_r_x, prepare_data_x_bar_rs_x),
    CHART_X_BAR_R_R: (get_stats_x_bar_r_r, prepare_data_x_bar_r_r),
    CHART_X_BAR_S_X: (get_stats_x_bar_s_x, prepare_data_x_bar_rs_x),
    CHART_X_BAR_S_S: (get_stats_x_bar_s_s, prepare_data_x_bar_s_s),
    CHART_X_MR_X: (get_stats_x_mr_x, prepare_data_none),
    CHART_X_MR_MR: (get_stats_x_mr_mr, prepare_data_x_mr),
    CHART_P: (get_stats_p, prepare_data_p),
    CHART_NP: (get_stats_np, prepare_data_none),
    CHART_C: (get_stats_c, prepare_data_none),
    CHART_U: (get_stats_u, prepare_data_u),
    CHART_EWMA: (None, prepare_data_none),
    CHART_CUSUM: (get_stats_cusum, prepare_data_cusum),
    CHART_THREE_WAY: (None, prepare_data_none),
    CHART_TIME_SERIES: (None, prepare_data_none)}

RULES_FUNCS = {
    RULES_1_BEYOND_3SIGMA: (test_beyond_limits, 1),
    RULES_2_OF_3_BEYOND_2SIGMA: (None, 3),
    RULES_4_OF_5_BEYOND_1SIGMA: (None, 5),
    RULES_7_ON_ONE_SIDE: (test_violating_runs, 7),
    RULES_8_ON_ONE_SIDE: (test_violating_runs, 8),
    RULES_9_ON_ONE_SIDE: (test_violating_runs, 9),
    RULES_6_TRENDING: (None, 6),
    RULES_14_UP_DOWN: (None, 14),
    RULES_15_BELOW_1SIGMA: (None, 15),
    RULES_8_BEYOND_1SIGMA_BOTH_SIDES: (None, 8)}

class Spc(object):
    """
    Main class that provides SPC analysis. It detects SPC rules violations.
    It can draw charts using matplotlib.

    :arguments:
      data
       user data as flat array

    **Usage**

    >>> s = Spc([1, 2, 3, 3, 2, 1, 3, 8], CHART_X_MR_X)
    >>> s.get_stats()
    (2.875, 0.21542553191489322, 5.5345744680851068)
    >>> s.get_violating_points()
    {'1 beyond 3*sigma': [7]}
    >>> s.get_chart()
    >>> s = Spc([1, 2, 3, 3, 2, 1, 3, 8], CHART_CUSUM)
    >>> s.get_stats()
    (0, None, None)
    >>> s.get_violating_points()
    {'7 on one side': [7, 8], '1 beyond 3*sigma': [1, 2, 3, 4, 5, 6, 7, 8]}
    >>> s.get_chart()
    """

    def __init__(self, data, chart_type, rules=RULES_BASIC, newdata=[], sizes=None):
        self.orig_data = data
        self.chart_type = chart_type
        self.rules = rules
        self.stats = []

        sf, pd = STATS_FUNCS[chart_type]
        if sizes == None:
            if isinstance(data[0], (list, tuple)):
                size = len(data[0])
            else:
                size = 1
        else:
            size = sizes
        self.center, self.lcl, self.ucl = sf(data, size)
        self._data = pd(data, size)

        self.violating_points = self._find_violating_points()

    def _find_violating_points(self, rules=[]):
        if len(rules) > 0:
            rs = rules
        else:
            rs = self.rules
        points = {}
        for i in xrange(len(self._data)):
            for r in rs:
                func, points_num = RULES_FUNCS[r]
                if func == None or i <= points_num - 1:
                    continue
                if func(self._data[i-points_num+1:i+1], self.center, self.lcl, self.ucl):
                    points.setdefault(r, []).append(i)
        return points

    def get_violating_points(self, rules=[]):
        """Return points that violates rules of control chart"""
        return self.violating_points

    def get_stats(self):
        """Return basic statistics about data as tuple: (center, LCL, UCL)."""
        return self.center, self.lcl, self.ucl
