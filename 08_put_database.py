from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
import time
import pymysql
from cfg import setting
import smtplib
from email.mime.text import MIMEText
import datetime

# db연결
hotplace_db = pymysql.connect(
    user=setting.DB_CFG['user'],
    passwd=setting.DB_CFG['passwd'],
    host=setting.DB_CFG['host'],
    db=setting.DB_CFG['db'],
    charset=setting.DB_CFG['charset'])
cur = hotplace_db.cursor(pymysql.cursors.DictCursor)

# 크롤링
dr = wd.Chrome(executable_path="./cfg/chromedriver.exe")
dr.get('https://map.kakao.com/')
dr.implicitly_wait(3)
# 검색
dr.find_element_by_id("search.keyword.query").send_keys("연수구 맛집")
dr.find_element_by_id("search.keyword.query").send_keys(Keys.ENTER)
dr.implicitly_wait(5)
try:
    show_more = dr.find_element_by_xpath('//*[@id="info.search.place.more"]').send_keys(Keys.ENTER)
except:
    print('장소 더보기 누를수 없음')
time.sleep(2)

# 중간에 멈춰서 일정 부분 이후부터 돌리고 싶을때
for m in range(0, 0):
    dr.find_element_by_xpath('//*[@id="info.search.page.next"]').send_keys(Keys.ENTER)
    time.sleep(2)

# 5개씩 실행
for q in range(0, 100):
    # 1,2,3,4,5 페이지씩 넘어가기
    for p in range(0, 5):
        dr.find_element_by_xpath('//*[@id="info.search.page.no' + str(p + 1) + '"]').send_keys(Keys.ENTER)
        time.sleep(2)

        # 음식점페이지 개수 불러오기
        place_list = dr.find_elements_by_css_selector("div.info_item > div.contact.clickArea > a.moreview")
        len_place = len(place_list)
        print(place_list)
        print('음식점 갯수: {}'.format(len_place))

        # 음식적페이지 마다 새창을 열고, 작업을 한후 다시 돌아옴.
        for i in range(0, len_place):
            place_list[i].send_keys(Keys.ENTER)
            dr.implicitly_wait(3)
            dr.switch_to.window(dr.window_handles[1])

            # 음식점 정보 불러오기
            _restaurant_name = dr.find_element_by_xpath('//*[@id="mArticle"]/div[1]/div[1]/div[2]/div/h2')
            _avg_rating = dr.find_element_by_xpath('//*[@id="mArticle"]/div[1]/div[1]/div[2]/div/div/a[1]/span[1]')
            _location = dr.find_element_by_xpath('//*[@id="mArticle"]/div[1]/div[2]/div[1]/div/span[1]')
            _category = dr.find_element_by_xpath('//*[@id="mArticle"]/div[1]/div[1]/div[2]/div/div/span[1]')
            cur.execute('replace into restaurant (restaurant_name, avg_rating, location, category) values (%s, %s, %s, %s)',
                        (_restaurant_name.text, _avg_rating.text, _location.text, _category.text))

            print(_restaurant_name.text)
            print(_avg_rating.text)
            print(_location.text)
            print(_category.text)
            dr.implicitly_wait(3)

            # 리뷰 불러오기
            review_list = dr.find_elements_by_css_selector("#mArticle > div.cont_evaluation > div.evaluation_review > ul > li")
            for j in range(0, len(review_list)):
                # element 위치변동이 있어서, css_selector를 이용
                _rating = dr.find_elements_by_css_selector('#mArticle > div.cont_evaluation > div.evaluation_review > ul > li:nth-child('+ str(j+1) + ') > div.star_info > div > em')
                _review = dr.find_elements_by_css_selector('#mArticle > div.cont_evaluation > div.evaluation_review > ul > li:nth-child('+ str(j+1) + ') > div.comment_info > p > span')
                if len(_review) > 175: #VARCHAR 700byte제한인데 utf8mb4를 사용하면 175글자제한
                    continue
                if not _rating: #
                    continue
                if not _review:
                    continue
                cur.execute('replace into review (r_name, rating, content) values (%s, %s, %s)',
                            (_restaurant_name.text, _rating[0].text, _review[0].text))
                print(_rating[0].text)
                print(_review[0].text)

            dr.close()
            dr.switch_to.window(dr.window_handles[0])
            dr.implicitly_wait(3)

            hotplace_db.commit()

    #5개 다음페이지로 
    dr.find_element_by_xpath('//*[@id="info.search.page.next"]').send_keys(Keys.ENTER)
    time.sleep(2)
                
hotplace_db.close()