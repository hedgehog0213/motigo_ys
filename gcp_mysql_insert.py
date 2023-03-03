import pymysql
from datetime import datetime
import time
import pandas as pd

# db 저장소 : warm-melody-377101:asia-northeast3:translation-db
# db 이름 : for_prac
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
    sql1='SELECT * FROM translationsource ORDER BY DATETIME DESC LIMIT 1;'
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



def load_user_list(): #유저 정보 가져오기
    conn = pymysql.connect(host='34.64.173.250',user='root', password='mococo1$', db='for_prac', charset='utf8')
    cur = conn.cursor()
    sql1="SELECT uid,email,NAME,TYPE,SUBSTR(DATETIME,1,10) AS '가입일자' FROM user_info order BY FIELD(type,'admin','유료회원','무료회원'),4,1;"
    cur.execute(sql1)
    bd=cur.fetchall()
    conn.commit()
    conn.close()
    user_DataFrame=pd.DataFrame(bd,columns=['UID','Email','Name','Type','JoinDate'])
    user_DataFrame.index = user_DataFrame.index + 1
    user_html=user_DataFrame.to_html()
    #print(user_DataFrame)
    return user_DataFrame

def check_admin(uid): # 특정 uid의 type(유료,무료,관리자)가져오기
    conn = pymysql.connect(host='34.64.173.250',user='root', password='mococo1$', db='for_prac', charset='utf8')
    cur = conn.cursor()
    sql_check_admin = "SELECT TYPE FROM user_info WHERE uid=%s;"
    check_admin_data=(uid)
    cur.execute(sql_check_admin,check_admin_data)
    bf=cur.fetchall()
    now_type=""
    for i in bf:
        for j in i:
            now_type=j

    return now_type


def load_user_translationsource(uid): #특정 유저의 번역 정보 가져오기
    conn = pymysql.connect(host='34.64.173.250',user='root', password='mococo1$', db='for_prac', charset='utf8')
    cur = conn.cursor()
    sql_user_translationsource="SELECT u.name,t.datetime, t.source, t.target, t.len FROM translationsource t JOIN user_info u ON t.uid=u.uid WHERE t.uid=%s"
    sql_user_translationsource_data=(uid)
    cur.execute(sql_user_translationsource,sql_user_translationsource_data)
    tr_bd=cur.fetchall()
    conn.commit()
    conn.close()
    translation_DataFrame=pd.DataFrame(tr_bd,columns=['Name','Datetime','Source','Target','Point'])
    translation_DataFrame.index = translation_DataFrame.index + 1
    #print(translation_DataFrame)
    return translation_DataFrame

def load_charge_point(): #특정 유저의 결제(충전) 정보 가져오기
    conn = pymysql.connect(host='34.64.173.250',user='root', password='mococo1$', db='for_prac', charset='utf8')
    cur = conn.cursor()
    sql_charge_point="SELECT u.name,u.email, p.point, p.datetime FROM point p JOIN user_info u ON u.uid=p.uid  WHERE p.division='충전';"
    cur.execute(sql_charge_point)
    cp_bd=cur.fetchall()
    conn.commit()
    conn.close()
    charge_point_DataFrame=pd.DataFrame(cp_bd,columns=['Name','Email','Point','Datetime'])
    charge_point_DataFrame.index = charge_point_DataFrame.index + 1
    #print(charge_point_DataFrame)
    return charge_point_DataFrame

def load_distinct_email(): #등록된 고유 이메일 정보 가져오기
    conn = pymysql.connect(host='34.64.173.250', user='root', password='mococo1$', db='for_prac', charset='utf8')
    cur = conn.cursor()
    sql_distinct_email="select distinct(email) from user_info;"
    cur.execute(sql_distinct_email)
    de_bd=cur.fetchall()
    conn.commit()
    conn.close()
    distinct_email=[]
    for i in de_bd:
        for j in i:
            distinct_email.append(j)
    return distinct_email

def load_tr_list(target_email): #관리자가 아닌 특정 사용자의 번역정보 가져오기
    conn = pymysql.connect(host='34.64.173.250', user='root', password='mococo1$', db='for_prac', charset='utf8')
    cur = conn.cursor()
    sql_tr_info="SELECT u.email, t.source, t.target, t.len, t.datetime FROM  translationsource t JOIN user_info u ON u.uid=t.uid WHERE u.email=%s;" # AND u.type != 'admin'"
    sql_tr_info_data=(target_email)
    cur.execute(sql_tr_info,sql_tr_info_data)
    tl_bd=cur.fetchall()
    conn.commit()
    conn.close()
    translatinsource_list_DataFrame = pd.DataFrame(tl_bd, columns=['Email', 'Source', 'Target', 'Point','Datetime'])
    translatinsource_list_DataFrame.index = translatinsource_list_DataFrame.index + 1
    #print(translatinsource_list_DataFrame)
    return translatinsource_list_DataFrame

# 마이페이지 관련
def my_tr_list(target_uid): #내 번역정보 가져오기
    conn = pymysql.connect(host='34.64.173.250', user='root', password='mococo1$', db='for_prac', charset='utf8')
    cur = conn.cursor()
    sql_tr_info= "SELECT source,target,len,datetime from translationsource WHERE uid= %s && SOURCE != '' order by datetime desc;" # AND u.type != 'admin'"
    sql_tr_info_data=(target_uid)
    cur.execute(sql_tr_info,sql_tr_info_data)
    tl_bd=cur.fetchall()
    conn.commit()
    conn.close()
    translatinsource_list_DataFrame = pd.DataFrame(tl_bd, columns=['번역 전', '번역 후', '사용포인트','날짜'])
    translatinsource_list_DataFrame.index = translatinsource_list_DataFrame.index + 1
    #print(translatinsource_list_DataFrame)
    return translatinsource_list_DataFrame

def my_charge_point(target_uid): #나의 결제(충전) 정보 가져오기
    conn = pymysql.connect(host='34.64.173.250',user='root', password='mococo1$', db='for_prac', charset='utf8')
    cur = conn.cursor()
    sql_charge_point= "SELECT point,concat(point,'원'),final,datetime from point WHERE uid=%s && division = '충전' ORDER BY DATETIME desc;"
    sql_charge_data = (target_uid)
    cur.execute(sql_charge_point, target_uid)
    cp_bd=cur.fetchall()
    conn.commit()
    conn.close()
    charge_point_DataFrame=pd.DataFrame(cp_bd,columns=['충전포인트','충전금액','충전 후 포인트','날짜'])
    charge_point_DataFrame.index = charge_point_DataFrame.index + 1
    #print(charge_point_DataFrame)
    return charge_point_DataFrame

def my_page(target_uid): # 내 가입정보 불러오기
    conn = pymysql.connect(host='34.64.173.250', user='root', password='mococo1$', db='for_prac', charset='utf8')
    cur = conn.cursor()
    sql = "SELECT u.email,u.NAME,u.TYPE,concat(p.point, ' 포인트'),u.datetime FROM user_info u JOIN point p ON u.uid=p.uid WHERE u.uid=%s ORDER BY p.datetime DESC LIMIT 1;"
    sql_charge_data = (target_uid)
    cur.execute(sql, target_uid)
    result = cur.fetchone()
    print(result)

    return result


