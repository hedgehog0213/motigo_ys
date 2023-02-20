import pymysql
from datetime import datetime
import time

# db 저장소 : warm-melody-377101:asia-northeast3:translation-db
# ip : 34.64.173.250
def save_pymysql(sourcetxt, targettxt,uid): #번역 전과 번역 후를 인덱스를 포함하여 mysql에 저장
    conn = pymysql.connect(host='34.64.173.250',user='root', password='mococo1$', db='for_prac', charset='utf8')
    cur = conn.cursor()
    sql2 = 'insert into translationsource values (%s,%s,%s,%s,%s);'
    data = ( uid,sourcetxt, targettxt, len(sourcetxt.replace(' ', '')), time.strftime('%y/%m/%d - %X'))
    cur.execute(sql2, data)
    conn.commit()
    conn.close()
    return None

def load_result_pymysql(): #마지막으로 저장된 인덱스를 값으로 하여 번역 정보를 불러 온다.
    result_list=[]
    #df = pd.read_csv("database.csv")
    #result_list.append(df.iloc[-1].tolist())

    conn = pymysql.connect(host='34.64.173.250',user='root', password='mococo1$', db='for_prac', charset='utf8')
    cur = conn.cursor()
    sql1='SELECT * FROM translationsource ORDER BY DATETIME DESC LIMIT 1;;'
    cur.execute(sql1)
    all_fetch=cur.fetchall()
    conn.commit()
    conn.close()
    for i in all_fetch:
        for j in i:
            result_list.append(i)
    print(result_list[0])
    return result_list[0]



def save_user_pymysql(uid,name,email): #유저 정보를 입력받아 보자,현재 테이블이 uid와 signup_date 두개로만 있어서 이정도
    now=datetime.now()

    conn = pymysql.connect(host='34.64.173.250',user='root', password='mococo1$', db='for_prac', charset='utf8')
    cur = conn.cursor()
    sql1='select uid from user_info;'
    cur.execute(sql1)
    user_list=cur.fetchall()
    u_l=[]
    for i in user_list:
        for j in i:
            u_l.append(j)
    if uid not in u_l:
        sql_user_info = "insert into user_info(uid,name,email,type,datetime) values (%s,%s,%s,'무료회원',%s)" #만약 컬럼이 추가된다면 이부분을 바꾸자
        data = (uid,name,email,time.strftime('%y/%m/%d - %X'))                                     #이부분도 추가 시켜줘야 한다
        cur.execute(sql_user_info, data)
        conn.commit()
        sql_point_basic = "insert into point(uid,division,point,final,datetime) values (%s,'무료충전',1000,1000,%s)"
        data_sql_point_basic = (uid,time.strftime('%y/%m/%d - %X'))
        cur.execute(sql_point_basic,data_sql_point_basic)
        conn.commit()
        conn.close()
        print(uid+'의 회원가입을 완료하였습니다')
        print(uid + '는 무료회원입니다')
        print(uid+'에게 기본포인트 1000을 증정했습니다')
    else:
        print('회원 정보가 이미 있습니다')



def load_user_list(): #마지막으로 저장된 인덱스를 값으로 하여 번역 정보를 불러 온다.

    #df = pd.read_csv("database.csv")
    #result_list.append(df.iloc[-1].tolist())

    conn = pymysql.connect(host='34.64.173.250',user='root', password='mococo1$', db='for_prac', charset='utf8')
    cur = conn.cursor()
    sql1="SELECT email,NAME,TYPE,SUBSTR(DATETIME,1,10) AS '가입일자' FROM user_info;"
    cur.execute(sql1)
    bd=cur.fetchall()
    conn.commit()
    conn.close()
    user_DataFrame=pd.DataFrame(bd)
    print(user_DataFrame)
    return user_DataFrame

