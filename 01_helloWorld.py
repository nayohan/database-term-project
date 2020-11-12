from flask import Flask
app = Flask(__name__)

@app.route('/')
@app.route('/hello/<string:name>')
def hello(name=None):
    if (name!=None):
        return 'Hello {}'.format(name)
    return 'Hello World!'

@app.route('/goodbye/<string:name>')
def sumfunction(name=None):
    if (name!=None):
        return 'Goodbye {}'.format(name)
    return 'Goodbye World!'

if __name__=='__main__':
    app.debug=True
    app.run()