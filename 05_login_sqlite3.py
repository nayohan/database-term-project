from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/user', methods=['POST'])
def user():
    db = sqlite3.connect("./hotplace_sql/hotplace.db")
    db.row_factory = sqlite3.Row

    id = request.form['id']
    pw = request.form['pw']
    db.execute(
        'update users'
        ' set id=?'
        ' where id=?',
        (request.form['id'], id)
    )
    db.commit()
    db.close()
    return render_template('login_result.html', id=id, pw=pw)


if __name__=='__main__':
    app.debug=True
    app.run(host='192.168.0.8', port=5000)
