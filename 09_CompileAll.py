from flask import Flask, render_template, request, flash, url_for
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
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
_isLogin = False

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
    cur.execute('select * from users where id=(%s)',_id)
    _isAlreadyUse = cur.fetchall()
    #print(_isAlreadyUse)
    if (_isAlreadyUse):
        print(1)
        flash('id is alreday in use.')
        return render_template('register.html')
    
    cur.execute('insert into users (id, password,username, email) values (%s, %s, %s, %s)', (_id, _pw, _username, _email))
    hotplace_db.commit()
    return render_template('register_result.html', id=_id, pw=_pw, username=_username, email=_email)

@app.route('/login', methods=['POST'])
def login(): #로그인 로직
    _id = request.form['id']
    _pw = request.form['pw']
    cur.execute('select * from users where id=(%s)',_id)
    rows = cur.fetchall()
    #print(rows)

    if rows:
        if rows[0]['id']:
            if _pw==rows[0]['password']:
                flash('login Success')
                _isLogin = True
                return url_for('/restaurant')
            else:
                flash('login Failed, password wrong.')
        else:
            flash('login Failed, id is not available')
    return render_template('login.html')


@app.route('/restaurant', methods=['GET'])
def show_restaurant(): # 음식점 검색
    _toSearch = request.args.get('toSearch', "")
    cur.execute("select * from restaurant where location like %s", ('%%%s%%' % _toSearch))
    rows = cur.fetchall()
    print(rows)

    if rows:
        return render_template('show_restaurant.html', rows=rows)
    return render_template('show_restaurant.html')

@app.route('/mypage')
def show_mypage(): # 즐겨찾기,리뷰삭제,회원탈퇴
    return render_template('show_mypage.html')


@app.route('/review')
def show_review(): # 리뷰보기
    return render_template('show_review.html')

@app.route('/add_review')
def  add_review(): # 리뷰
    return render_template('add_review.html')

if __name__=='__main__':
    app.debug=True
    app.run(host='192.168.0.8', port=5000)
    