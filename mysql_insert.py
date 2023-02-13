import pymysql

#pymysql.connect(host='funcoding-db.ca1fydhpobsc.ap-northeast-2.rds.amazonaws.com', port=3306, user='davelee', passwd='korea123', db='student_mgmt', charset='utf8')



def save_pymysql(sourcetxt, targettxt):
    conn = pymysql.connect(host='localhost', user='root', password='root', db='mococo', charset='utf8')
    cur = conn.cursor()
    sql1='select count(*) from translationsource;'
    cur.execute(sql1)
    last_num=cur.fetchall()
    final=0
    for i in last_num :
        for j in i:
            final = j
    index = final+1
    sql2 = 'insert into translationsource values (%s,%s,%s);'
    data = (int(index), sourcetxt, targettxt)
    cur.execute(sql2, data)
    conn.commit()
    conn.close()
    return None

def load_result_pymysql():
    result_list=[]
    #df = pd.read_csv("database.csv")
    #result_list.append(df.iloc[-1].tolist())

    conn = pymysql.connect(host='localhost', user='root', password='root', db='mococo', charset='utf8')
    cur = conn.cursor()
    sql1='select * from translationsource order by 1 desc limit 1;'
    cur.execute(sql1)
    all_fetch=cur.fetchall()
    conn.commit()
    conn.close()
    for i in all_fetch:
        for j in i:
            result_list.append(i)
    print(result_list[0])
    return result_list[0]