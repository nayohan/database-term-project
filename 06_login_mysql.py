from flask import Flask, render_template, request
import pymysql
from cfg import setting

hashtag_db = pymysql.connect(
    user=setting.DB_CFG['user'],
    passwd=setting.DB_CFG['passwd'],
    host=setting.DB_CFG['host'],
    db=setting.DB_CFG['db'],
    charset=setting.DB_CFG['charset'])
cur = hashtag_db.cursor(pymysql.cursors.DictCursor)

app = Flask(__name__)
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/user', methods=['POST'])
def user():
    _id = request.form['id']
    _pw = request.form['pw']
    _username = request.form['username']
    _email = request.form['email']
    cur.execute('insert into users (id, password,username, email) values (%s, %s, %s, %s)', (_id, _pw, _username, _email))
    hashtag_db.commit()
    return render_template('login_result.html', id=_id, pw=_pw)
if __name__=='__main__':
    app.debug=True
    app.run(host='192.168.0.8', port=5000)
