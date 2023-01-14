from flask import Flask

app = Flask(__name__)
# __name__ is the application name

@app.route('/')
def index_page():
    return '''
        <html>
            <head>
                <title>Home page</title>
            </head>
            <body>
                <p>
                    <h1>Advanced Programming project</h1>
                    <ul>
                        <li>ciao </li>
                        <li>ciao come stai</li>
                    </ul>
                </p>
                <p>The slides are available <a href="/slides">here</a>.</p>
            </body>
        </html>'''

@app.route('/slides')
def slide():
    return '''
        <html>
            <head><title>Slides</title></head>
            <body>
                <p>Ciao</p>
                <p>The home is available <a href="/">here</a>.</p>
            </body>
        </html>'''


if __name__=='__main__':
    app.run(port=3000)

