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

``` bash
curl -d 'data=1,2,3,4,5,6,7,8,9,10' https://spc.io/new
```
And you'll get a url with your new chart - looking a little like this:

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