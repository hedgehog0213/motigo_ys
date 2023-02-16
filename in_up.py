import pymysql
import time


#sql1="select point from user_info where uid = %s;"
#cur.execute(sql1)
#yp=cur.fetchall()
#now_point = 0
#for i in yp:
#    for j in i:
#        now_point = j
def consumption(uid,len): # consumption(소비)에 insert 및 회원정보 update
    conn = pymysql.connect(host='34.64.173.250', user='root', password='mococo1$', db='for_prac', charset='utf8')
    cur = conn.cursor()
    sql1 = "select final from point where uid = %s;"
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

def charge(uid,fee):  # charge(충전)에 insert 및 회원정보 update
    conn = pymysql.connect(host='34.64.173.250', user='root', password='mococo1$', db='for_prac', charset='utf8')
    cur = conn.cursor()
    sql1 = "select point from user_info where uid = %s;"
    user_info_data = (uid)
    cur.execute(sql1, user_info_data)
    yp = cur.fetchall()
    now_point = 0
    for i in yp:
        for j in i:
            now_point = j
    final=now_point + fee
    sql_update = "update user_info set point = %s where uid = %s"
    update_data = (final, uid)
    cur.execute(sql_update, update_data)
    conn.commit()
    sql_insert = "insert into charge values(%s,%s,%s,%s,%s)"
    insert_data = (uid, now_point,fee, final,time.strftime('%y/%m/%d - %X'))
    cur.execute(sql_insert, insert_data)
    conn.commit()
    conn.close()

def save_charge(save_point,uid):
    conn = pymysql.connect(host='34.64.173.250', user='root', password='mococo1$', db='for_prac', charset='utf8')
    cur = conn.cursor()
    sql1 = "select point from user_info where uid = %s;"
    user_info_data = (uid)
    cur.execute(sql1, user_info_data)
    yp = cur.fetchall()
    now_point = 0
    for i in yp:
        for j in i:
            now_point = j
    final=now_point + save_point
    sql_insert = "insert into charge values(%s,%s,%s,%s,%s)"
    insert_data = (uid, now_point, save_point, final,time.strftime('%y/%m/%d - %X'))
    cur.execute(sql_insert, insert_data)
    conn.commit()
    conn.close()



#uid = 'Ey3J7fIq4lbPG8pCvBpUactG57j1'
#fee = 1000
#len = 60
#consumption(uid,len)
#charge(uid,fee)

