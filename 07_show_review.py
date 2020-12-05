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
@app.route('/review', methods=['GET'])
def show_review():
    _toSearch = request.args.get('toSearch', "")

    cur.execute("select * from restaurant where location like %s", ('%%%s%%' % _toSearch))
    rows = cur.fetchall()
    print(rows)
    if rows:
        return render_template('show_review.html', rows=rows)
    
    return render_template('show_review.html')


if __name__=='__main__':
    app.debug=True
    app.run(host='192.168.0.8', port=5000)