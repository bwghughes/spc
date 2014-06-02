import os
import argparse

import pygal
import shortuuid
from pygal.style import BlueStyle, DarkSolarizedStyle, DarkColorizedStyle, CleanStyle


from spc import *


class SpcChart(object):
    def __init__(self, data, title=None, filename=None):
        self.data = data
        self.title = title
        self.filename = "{}.svg".format(shortuuid.uuid())

    def render_to_file(self):
        line_chart = pygal.Line(style=CleanStyle)
        line_chart.title = self.title
        mean, lcl, ucl = Spc(self.data, CHART_X_MR_X).get_stats()

        #line_chart.x_labels = map(str, range(2002, 2013))
        line_chart.add('UCL', [ucl for d in self.data])
        line_chart.add('LCL', [lcl for d in self.data])
        line_chart.add('Mean', [mean for d in self.data])
        line_chart.add('Data', [d for d in self.data])
        line_chart.render_to_file(self.filename)
        print "Written to {}".format(self.filename)
        return self.filename

    def render_to_svg(self):
        pass
