![Control Charts For Humans](http://benhughes.org.s3.amazonaws.com/controlcharts/ccfh.png "Control Charts For Humans")

What are control charts?
---

Control charts are really useful tools to help you understand how 'in control your process is'
so you can help make process changes based on evidence, rather than bullshit.

You can read the docs about the library and control charts [here](https://statistical-process-control-charts.readthedocs.org/en/latest/ "Read The Docs").

<!-- HTTP Api Access
---

You can call the webservice service with your data:

``` bash
curl -d 'data=1,2,3,4,5,6,7,8,9,10' -d 'title=I can see now' https://spc.io/new
```
And you'll get a url with your new chart - looking a little like this:
 -->
Installing
==========

To install the latest release from (PyPI)[http://pypi.python.org/pypi/spcchart]

``` console

    $ pip install spcchart
```

To install the latest development version from (GitHub)[https://github.com/bwghughes/spc]

``` console

    $ pip install git+git://github.com/bwghughes/spc.git
```

An example:
---

![Control Chart](http://benhughes.org.s3.amazonaws.com/controlcharts/sample.png "Control Chart")

Command Line Usage
-------------------

``` bash
pip install spcchart
```
and run:
``` bash
spcchart --data=32,45,65,667,767,78,887,879,99,98,98,98 --title="I can see now"
```
and hip hip hooray, an svg will be placed in your current working directory. Open with any browser and you're away.

Python Library Use
------------

### Static SVG Charts (Pygal)

``` python
>>> from spcchart import SpcChart
>>> data = [1,2,3,4,5,6,7,8,9,8,7,6,5,5,5,4,4,3,3,2,2,2,3,4,5,5,5]
>>> c = SpcChart(data, title="Flow Ho")
>>> c.render_to_file()  # Creates SVG file
```

### Interactive Web Charts (Plotly) - NEW!

``` python
>>> from spcchart.plotly_chart import PlotlySpcChart
>>> data = [1,2,3,4,5,6,7,8,9,8,7,6,5,5,5,4,4,3,3,2,2,2,3,4,5,5,5]
>>> chart = PlotlySpcChart(data, title="Interactive Chart")
>>> chart.render_to_file()  # Creates interactive HTML file
>>> # or get HTML string
>>> html = chart.render_to_html()
```

Web Application
---------------

Run the Flask web application for a browser-based interface:

``` bash
python app.py
```

Then open http://localhost:5000 in your browser to:
- Enter data points
- Select chart type
- Generate interactive charts
- View statistics and violations

Development
-----------

This project uses [uv](https://docs.astral.sh/uv/) for package management and [pytest](https://pytest.org/) for testing.

### Setup Development Environment

1. Install uv (if not already installed):
``` bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Create a virtual environment and install dependencies:
``` bash
uv venv
uv pip install -e ".[dev]"
```

3. Run tests:
``` bash
uv run pytest
```

4. Run tests with coverage:
``` bash
uv run pytest --cov=spcchart --cov-report=html
```

### Running Tests

All tests are located in the `tests/` directory. To run specific test files:

``` bash
uv run pytest tests/test_spc.py
uv run pytest tests/test_spcchart.py -v
```

Features
--------

- ✅ **No numpy dependency** - Uses pure Python stdlib (statistics, math)
- ✅ **Interactive charts** - Plotly-based web charts with zooming, panning, and export
- ✅ **Web interface** - Flask app for browser-based chart generation
- ✅ **Multiple chart types** - X-mR, X-bar R, p, c, and more
- ✅ **Violation detection** - Automatic detection of out-of-control points
- ✅ **Modern testing** - Comprehensive pytest test suite (41 tests)
- ✅ **Package management** - Uses uv for fast, reliable dependency management

To do
------

* Add themes to charts
* Add more chart types (EWMA, CUSUM improvements)
* Add export to PDF
* Add multi-chart dashboards