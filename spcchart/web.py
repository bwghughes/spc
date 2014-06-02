"""
Provide a web api for easily generting charts.

E.g.

GET:

https://spc.io/chart?data-1,2,3,4,5,6,7,5,4,3,4,5,3,2&title=Test%20Chart\
                     &output=png|svg&style=BlueStyle|DarkSolarizedStyle|\
                     DarkColorizedStyle


POST to https://spc.io/chart/ with 'application/json' returns:

"{'chart': 'https://spc.io/chart/329e8j2dound3un'}



"""

from bottle import run, get



@get('/chart/')
def login():
    return '''
        <form action="/chart/" method="post">
            data: <textarea name="data" type="text" /></textarea>
            title: <input name="title" type="text" /><br/>
            <input value="Login" type="submit" /><br/>
        </form>
    '''

@get('/api/')
def api():
    return [dict(x=y) for x, y in enumerate([1,2,3,4,5])]

s
run(host='localhost', port=8080, debug=True, reloader=True)
