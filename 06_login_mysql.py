from flask import Flask, render_template, request
import pymysql
from cfg import setting

hotplace_db = pymysql.connect(
    user=setting.DB_CFG['user'],
    passwd=setting.DB_CFG['passwd'],
    host=setting.DB_CFG['host'],
    db=setting.DB_CFG['db'],
    charset=setting.DB_CFG['charset'])
cur = hotplace_db.cursor(pymysql.cursors.DictCursor)

app = Flask(__name__)
@app.route('/')
def main(): #로그인 페이지
    return render_template('login.html')

@app.route('/register')
def register(): #회원가입 페이지
    return render_template('register.html')

@app.route('/register/do', methods=['POST'])
def do_register(): #회원가입 로직
    _id = request.form['id']
    _pw = request.form['pw']
    _username = request.form['username']
    _email = request.form['email']
    cur.execute('insert into users (id, password,username, email) values (%s, %s, %s, %s)', (_id, _pw, _username, _email))
    hotplace_db.commit()
    return render_template('register_result.html', id=_id, pw=_pw, username=_username, email=_email)

cur.execute('')
@app.route('/login', methods=['POST'])
def login(): #로그인 로직
    _id = request.form['id']
    _pw = request.form['pw']
    cur.execute('select * from users where id=(%s)',_id)
    rows = cur.fetchall()
    _isId = False
    _isLogin = False

    print(rows)
    if rows:
        if rows[0]['id']:
            _isId = True
            if _pw==rows[0]['password']:
                _isLogin=True
                
    return render_template('login_result.html', isId=_isId, isLogin=_isLogin)

if __name__=='__main__':
    app.debug=True
    app.run(host='192.168.0.8', port=5000)
