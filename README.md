![Control Charts For Humans](http://benhughes.org.s3.amazonaws.com/controlcharts/ccfh.png "Control Charts For Humans")

What are control charts?
---

Control charts are really useful tools to help you understand how 'in control your process is'
so you can help make process changes based on evidence, rather than bullshit.

You can read lots more about control charts [here][1].

You can read the docs about the library [here][2].

In progress
---

Or, just call the service URL with your data:

http://spc.io/?data=1,2,3,4,5,6,7,8,9,10&ouput=png and it will send back something like this:

![Control Chart](http://benhughes.org.s3.amazonaws.com/controlcharts/sample.png "Control Chart")

[1]:http://en.wikipedia.org/wiki/Control_chart
[2]:https://statistical-process-control-charts.readthedocs.org/en/latest/

Library Use
------------

``` python
>>> from spcchart import SpcChart
>>> data = [1,2,3,4,5,6,7,8,9,8,7,6,5,5,5,4,4,3,3,2,2,2,3,4,5,5,5]
>>> c = SpcChart(data, title="Flow Ho")
>>> c.render()
```

To do
------

* Factor out numpy - its a bit overkill.
* Add themes to charts