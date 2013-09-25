.. Control Charts documentation master file, created by
   sphinx-quickstart on Mon Nov 19 13:39:01 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==================================================
Control Charts for people who need them
==================================================

Release v\ |version|. (:ref:`Installation <install>`)

Controlchart is an :ref:`ISC Licensed <isc>` Control Chart library, written in Python, for normal people.

Control charts are really useful tools to help you understand how 'in control your process is'
so you can help make management changes based on real information.

Here's a quick demo:

Say I have a process that churns out widgets, and the quality (% of customers where the widget
has met or exceeded the customer's expectation)
is distributed as below:

    >>> widgets_quality = [56, 75, 82, 12, 34, 18, 22, 81, 88, 91, 76, 85, 100, 88, 43, 44]

Control charts are really easy to create - read the code - but reading a control chart, and doing
the right thing is more important than writing the code.

This is people's lives we're messing with :)


    >>> data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> c = ControlChart(data)
    >>> c.mean = 5
    >>> c.lower_control_level = 2.339999999999999857891452848
    >>> c.upper_control_level = 7.660000000000000142108547152
    >>> c.to_json() # JSON
    >>> # TODO
    >>> c.to_python() # Python data structure
    >>> # TODO
    >>> c.to_flot() # For Flot JSON
    >>> # TODO
    >>> c.to_excel() # Excel Worksheet
    >>> # TODO
    >>> c.to_png('control_chart.png')
    >>> # TODO
    >>> c.to_pdf('control_chart.pdf')


Understanding Control Charts
-----------------------------

# TODO


Thanks
-------
**Kenneth Reitz**
    For inspiring great software, wirting great Python, and most of all for the outstanding
    libraries he writes including tablib - on which controlchart is based.

**John Chaimberlain**
    All round firebrand and lecturer at the University of Derby.

**John Seddon**
    For applying uncommon sense to common practice.

User Guide
----------

This part of the documentation is about building control charts using different
view components - Excel, PDF, JSON, Yaml, ODF.......

Contents:

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

