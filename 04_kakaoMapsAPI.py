from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello(name=None):
    
    return render_template('kakao.html')

if __name__=='__main__':
    app.debug=True
    app.run(host='192.168.0.8', port=5000)
