import pymysql
import time


#sql1="select point from user_info where uid = %s;"
#cur.execute(sql1)
#yp=cur.fetchall()
#now_point = 0
#for i in yp:
#    for j in i:
#        now_point = j
def consumption(uid,len): #가장 최근의 포인트 불러오고 소비 포인트까지 연산한뒤 새로이 저장
    conn = pymysql.connect(host='34.64.173.250', user='root', password='mococo1$', db='for_prac', charset='utf8')
    cur = conn.cursor()
    sql1 = "SELECT final FROM point WHERE uid = %s ORDER BY DATETIME DESC LIMIT 1;"
    user_info_data=(uid)
    cur.execute(sql1,user_info_data)
    yp = cur.fetchall()
    now_point = 0
    for i in yp:
        for j in i:
            now_point = j
    expense=now_point - len
    sql_point_expense = "insert into point(uid,division,point,final,datetime) values (%s,'사용',%s,%s,%s)"
    sql_point_expense_data = (uid,len,expense,time.strftime('%y/%m/%d - %X'))
    cur.execute(sql_point_expense,sql_point_expense_data)
    conn.commit()
    conn.close()

def save_paidamount(uid,paidamount): #결제 정보 db에 저장 및 무료회원이 충전했을 경우 유료회원으로 바꾸기
    conn = pymysql.connect(host='34.64.173.250', user='root', password='mococo1$', db='for_prac', charset='utf8')
    cur = conn.cursor()
    sql1 = "SELECT final FROM point WHERE uid = %s ORDER BY DATETIME DESC LIMIT 1;"
    user_info_data = (uid)
    cur.execute(sql1, user_info_data)
    yp = cur.fetchall()
    now_point = 0
    for i in yp:
        for j in i:
            now_point = j
    charge=paidamount + now_point
    sql_point_charge = "insert into point(uid,division,point,final,datetime) values (%s,'충전',%s,%s,%s)"
    sql_point_charge_data = (uid, paidamount, charge, time.strftime('%y/%m/%d - %X'))
    cur.execute(sql_point_charge,sql_point_charge_data)
    conn.commit()

    sql_check = "select type from user_info where uid = %s"
    sql_check_data=(uid)
    cur.execute(sql_check,sql_check_data)
    nt=cur.fetchall()
    now_type=""
    for i in nt:
        for j in i:
            now_type = j
    if now_type == '무료회원':
        sql_type_update = "update user_info set type = '유료회원' where uid = %s"
        sql_type_update_data = (uid)
        cur.execute(sql_type_update,sql_type_update_data)
        conn.commit()
        conn.close()
    else:
        print('이미 유료회원 입니다')
        conn.close()

