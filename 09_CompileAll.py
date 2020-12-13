from flask import Flask, render_template, redirect, request, flash, url_for, session
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
app.secret_key = 'ThisIsSomethingSpecial'

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
    cur.execute('SELECT * FROM users WHERE id=(%s)',_id)
    _isAlreadyUse = cur.fetchall()
    #print(_isAlreadyUse)
    if (_isAlreadyUse):
        print(1)
        flash('id is alreday in use.')
        return render_template('register.html')
    
    cur.execute('INSERT INTO users (id, password,username, email) VALUES (%s, %s, %s, %s)', (_id, _pw, _username, _email))
    hotplace_db.commit()
    return render_template('register_result.html', id=_id, pw=_pw, username=_username, email=_email)

@app.route('/login', methods=['POST'])
def login(): #로그인
    _id = request.form['id']
    _pw = request.form['pw']
    cur.execute('SELECT * FROM users WHERE id=%s AND password = %s', (_id, _pw))
    account = cur.fetchone()
    print(account)

    if account:
        session['loggedin'] = True
        session['id'] = account['id']
        session['username'] = account['username']
        flash('login Success')
        return redirect(url_for('show_restaurant'))
    else:
        flash('login Failed, Check id and passwrod')
        return render_template('login.html')

@app.route('/logout')
def logout(): #로그아웃
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    print(session)
    return render_template('login.html')

@app.route('/restaurant', methods=['GET'])
def show_restaurant(): # 음식점 검색
    if 'loggedin' in session:
        print(session)
        _toSearch = request.args.get('toSearch', "")
        cur.execute("SELECT * FROM restaurant WHERE location LIKE %s ORDER BY avg_rating DESC, restaurant_name", ('%%%s%%' % _toSearch))
        rows = cur.fetchall()
        return render_template('show_restaurant.html', rows=rows)
    else:
        flash('You need login first.')
        return render_template('login.html')


@app.route('/mypage')
def show_mypage(): # 즐겨찾기,리뷰삭제,회원탈퇴
    if 'loggedin' in session:
        return render_template('show_mypage.html')


@app.route('/review')
def show_review(): # 리뷰보기
    if 'loggedin' in session:
        return render_template('show_review.html')


@app.route('/add_review')
def  add_review(): # 리뷰
    if 'loggedin' in session:
        return render_template('add_review.html')


if __name__=='__main__':
    app.debug=True
    app.run(host='192.168.0.8', port=5000)
