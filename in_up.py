import pymysql
import time

conn = pymysql.connect(host='34.64.173.250',user='root', password='mococo1$', db='for_prac', charset='utf8')
cur = conn.cursor()
sql1="select point from user_info where uid = 'Ey3J7fIq4lbPG8pCvBpUactG57j1';"
cur.execute(sql1)
yp=cur.fetchall()
now_point = 0
for i in yp:
    for j in i:
        now_point = j
def consumption(uid,len): # consumption(소비)에 insert 및 회원정보 update
    final=now_point - len
    sql_update = "update user_info set point = %s where uid = %s"
    update_data=(final,uid)
    cur.execute(sql_update,update_data)
    conn.commit()
    sql_insert = "insert into consumption values(%s,%s,%s,%s,%s)"
    insert_data = (uid,now_point,len,final,time.strftime('%y/%m/%d'))
    cur.execute(sql_insert,insert_data)
    conn.commit()
    conn.close()

def charge(uid,fee):  # charge(충전)에 insert 및 회원정보 update
    final=now_point + fee
    sql_update = "update user_info set point = %s where uid = %s"
    update_data = (final, uid)
    cur.execute(sql_update, update_data)
    conn.commit()
    sql_insert = "insert into charge values(%s,%s,%s,%s)"
    insert_data = (uid, now_point,fee, final)
    cur.execute(sql_insert, insert_data)
    conn.commit()
    conn.close()





#uid = 'Ey3J7fIq4lbPG8pCvBpUactG57j1'
#fee = 1000
#len = 60
#consumption(uid,len)
#charge(uid,fee)

