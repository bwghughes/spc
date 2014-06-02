import os
import argparse
from .spcchart import SpcChart


__all__ = "SpcChart"

def main():
    parser = argparse.ArgumentParser(description='SPC Chart Generator')
    parser.add_argument('--data', action="store", dest="data",
                        help='Comma seperated list of values.')
    parser.add_argument('--title', action="store", dest="title",
                        help="Title for the chart.")
    options = parser.parse_args()

    if options.data and options.title:
        chart = SpcChart([float(i) for i in options.data.split(",")], title=options.title)
        filename = chart.render_to_file()
        path = 'file://{}/{}'.format(os.path.abspath(os.curdir), filename)
        print "Created file: {}".format(path)
    else:
        print "You need to supply --data and --title"
