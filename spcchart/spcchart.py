import os
import argparse

import pygal
import shortuuid
from pygal.style import BlueStyle


from spc import *


class SpcChart(object):
    def __init__(self, data, title=None, filename=None):
        self.data = data
        self.title = title
        self.filename = "{}.svg".format(shortuuid.uuid())

    def render(self):
        line_chart = pygal.Line(style=BlueStyle)
        line_chart.title = self.title
        mean, lcl, ucl = Spc(self.data, CHART_X_MR_X).get_stats()

        #line_chart.x_labels = map(str, range(2002, 2013))
        line_chart.add('UCL', [ucl for d in self.data])
        line_chart.add('LCL', [lcl for d in self.data])
        line_chart.add('Mean', [mean for d in self.data])
        line_chart.add('Data', [d for d in self.data])
        line_chart.render_to_file(self.filename)

def main():
    parser = argparse.ArgumentParser(description='SPC Chart Generator')
    parser.add_argument('--data', action="store", dest="data",
                        help='Comma seperated list of values.')
    parser.add_argument('--title', action="store", dest="title",
                        help="Title for the chart.")
    options = parser.parse_args()

    if options.data and options.title:
        chart = SpcChart([float(i) for i in options.data.split(",")], title=options.title)
        chart.render()
    else:
        print "You need to supply --data and --title"
