BEGIN TRANSACTION;
INSERT INTO "users" VALUES ('na','1234','나요한','na@gmail.com');
INSERT INTO "users" VALUES ('yohan','1234','요한나', 'yohan@naver.com');
INSERT INTO "users" VALUES ('john','1234', '존', 'john@daum.net');
INSERT INTO "users" VALUES ('nahyeong','1234', '김나형', 'nahyeong@kakao.com');

INSERT INTO "restaurant" VALUES ('가회동칼국수', '맛있어요', 5, 'songdo', '칼국수');
INSERT INTO "restaurant" VALUES ('타니스', '명란젓 파스타 굿', 4, 'songdo', '파스타');
INSERT INTO "restaurant" VALUES ('피제리아', '맛있는데 대기가 많아요', 4, 'songdo', '피자');
INSERT INTO "restaurant" VALUES ('새마을식당', '열탄불고기 맛있어요', 4, 'songdo', '불고기');
INSERT INTO "restaurant" VALUES ('롤링파스타', '파스타는 여기', 5, 'songdo', '파스타');

INSERT INTO "bookmark" VALUES ('na', '가회동칼국수', 'songdo', '칼국수');
INSERT INTO "bookmark" VALUES ('na', '타니스', 'songdo', '파스타');
INSERT INTO "bookmark" VALUES ('na', '피제리아', 'songdo', '피자');
INSERT INTO "bookmark" VALUES ('yohan', '롤링파스타', 'songdo', '파스타');
INSERT INTO "bookmark" VALUES ('yohan', '새마을식당',  'songdo', '불고기');
INSERT INTO "bookmark" VALUES ('yohan', '가회동칼국수',  'songdo', '칼국수');
INSERT INTO "bookmark" VALUES ('john', '피제리아', 'songdo', '피자');
INSERT INTO "bookmark" VALUES ('nahyeong', '타니스', 'songdo', '파스타');
COMMIT;
