import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#Firebase database 인증 및 앱 초기화
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://motigo-49f24-default-rtdb.firebaseio.com/'
})

ref = db.reference()
ref.update({'이름' : '김철수'})

#################################

#Firebase database 인증 및 앱 초기화
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://motigo-49f24-default-rtdb.firebaseio.com/'
})

#값 입력
ref = db.reference() #위치지정 - 빈값이면 기본 경로


ref = db.reference('강좌/파이썬')  # 경로가 없으면 생성한다.
ref.update({'파이썬 Flask로 웹 입문': 'complete'})
ref.update({'파이썬 웹 크롤링': 'Proceeding'})
ref.push({'이름': '김영희'})  # >> push는 하나의 hash값으로 패키지가 생기고 그 안에 데이터가 kv 형태로 들어간다.

# 값 조회
ref = db.reference('없는경로')
print(ref.get())

ref2 = db.reference('강좌/파이썬')
print(ref2.get())