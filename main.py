import pandas as pd
from flask import render_template, url_for,session,flash
from flask import Flask, request
from werkzeug.utils import redirect
import google_api as gap
import gcp_mysql_insert
import json
import os
import in_up
#합치기 전

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'

tgtresult = ""
result = ""
source_len=""
save_point=''
paidamount=""
uid=''
point=0

# 메인화면(로그인)
@app.route('/')
def popauth():
    return render_template('popauth.html')

#번역창
@app.route("/trans", methods=['GET', 'POST'],)
def trans(tgtresult=tgtresult, result=result, source_len=source_len,uid=uid,point=point):
    print(session['uid'])
    point = in_up.select_point(session['uid']) # 사용 전 포인트 조회
    print("trans 포인트:", point)
    sourcetxt = request.args.get("sourcetxt")
    usrType = move_page()
    print(usrType)
    if sourcetxt is not None:
        if gap.tr.translate(sourcetxt).src == 'ko':
            targettxt = gap.translate_to_en_text(sourcetxt)
        else:
            targettxt = gap.translate_to_ko_text(sourcetxt)
        print("/trans까지 완료" + session['uid']) #session['uid']가 존재하는 것 확인
        whole_result = save_srctgt(sourcetxt, targettxt)
        result = whole_result[1:3] #번역에 관한 모든 정보
        tgtresult = whole_result[2] #딱 번역된 결과만
        source_len=len(sourcetxt.replace(' ', ''))
        point = in_up.select_point(session['uid']) # 사용 전 포인트 조회
    return render_template("translator.html", usrType=usrType, len=source_len,sourcetxt=sourcetxt, result=tgtresult,source_len=source_len,uid=uid, point=point)#딱 번역된 결과만

# 유저타입 식별(어드민 || 유저)
@app.route("/move_page")
def move_page():
    now_type = gcp_mysql_insert.check_admin(session['uid'])
    # print(now_type)
    if now_type != "admin":
        return 'user'
    else:
        return 'admin'

#마이페이지
@app.route('/mypage')
def my_main():
    target_uid = session['uid']
    myinfo = gcp_mysql_insert.my_page(target_uid)
    email = myinfo[0]
    uname = myinfo[1]
    type = myinfo[2]
    point = myinfo[3]
    joindate = myinfo[4]
    print(result)
    usrType = move_page()
    print(usrType)
    return render_template('mypage.html', usrType=usrType, email=email,uname=uname,type=type,point=point,joindate=joindate)

@app.route('/my_charge') #충전 정보
def my_charge():
    target_uid = session['uid']
    charge_list = gcp_mysql_insert.my_charge_point(target_uid)
    usrType = move_page()
    print(usrType)
    return render_template('myCharge.html', usrType=usrType, tables=[charge_list.to_html(classes='data')],titles=charge_list.columns.values)

@app.route('/my_tr') # 나의 번역정보
def my_tr():
    target_uid = session['uid']
    print(target_uid)
    translatinsource_list_DataFrame = gcp_mysql_insert.my_tr_list(target_uid)
    usrType = move_page()
    print(usrType)
    return render_template('myTrlist.html', usrType=usrType,
                               tables=[translatinsource_list_DataFrame.to_html(classes='data')],
                               titles=translatinsource_list_DataFrame.columns.values)

#관리자페이지
@app.route('/dash_board') #시각화 대시보드
def dash_board():
    now_type = gcp_mysql_insert.check_admin(session['uid'])
    # print(now_type)
    if now_type != "admin":
        distinct_email = tr_select()
        return redirect(url_for('trans'))
    else:
        return render_template('graph.html')


@app.route('/user_list') # 회원 정보
def user_list():
    now_type=gcp_mysql_insert.check_admin(session['uid'])
    #print(now_type)
    if now_type == "admin":
        user_list = gcp_mysql_insert.load_user_list()
        return render_template('user_list.html', tables=[user_list.to_html(classes='data')],
                               titles=user_list.columns.values)
    else:
        return redirect(url_for('trans'))

@app.route('/charge_list') #충전 정보
def charge_point():
    now_type = gcp_mysql_insert.check_admin(session['uid'])
    if now_type == "admin":
        charge_list = gcp_mysql_insert.load_charge_point()
        return render_template('charge_list.html', tables=[charge_list.to_html(classes='data')],titles=charge_list.columns.values)
    else:
        return redirect(url_for('trans'))

@app.route('/tr_select') #email아이디 리스트 만들기
def tr_select():
    now_type = gcp_mysql_insert.check_admin(session['uid'])
    if now_type == "admin":
        distinct_email = gcp_mysql_insert.load_distinct_email()
        return render_template('tr_select2.html', distinct_email=distinct_email)
    else:
        return redirect(url_for('trans'))

@app.route('/tr_list',methods=['POST']) #이메일 리스트에서 선택된 이메일관련 내역을 표로 출력
def tr_info():
    now_type = gcp_mysql_insert.check_admin(session['uid'])
    if now_type == "admin":
        target_email = request.form['selected_value']
        translatinsource_list_DataFrame = gcp_mysql_insert.load_tr_list(target_email)
        return render_template('translation_list.html',
                               tables=[translatinsource_list_DataFrame.to_html(classes='data')],
                               titles=translatinsource_list_DataFrame.columns.values)
    else:
        return redirect(url_for('trans'))

#저장
@app.route("/save", methods=["POST"]) #번역 결과 전과 후 저장 ++여기다가 소비 함수 만든 후 사용하면 될듯
def save_srctgt(sourcetxt, targettxt,uid=uid):
    session['uid']
    gcp_mysql_insert.save_pymysql(sourcetxt, targettxt, session['uid']) #session['uid']만 들어가 있어도 세션값이 넘어감
    uid=session['uid']
    print("/save까지 완료 with" + session['uid'])
    result = gcp_mysql_insert.load_result_pymysql()
    in_up.consumption(session['uid'], len(sourcetxt.replace(' ','')))
    #print("/save에서의 result : ",result)
    #return redirect(url_for("trans"))
    return result


@app.route("/saveSQL", methods=['POST']) #회원정보 저장
def saveSQL():
    output = request.get_json()
    result = json.loads(output)
    pdinfo = pd.DataFrame(result['info'])
    uid = pdinfo.iloc[0, 0]
    name = pdinfo.iloc[1, 0]
    email = pdinfo.iloc[2, 0]
    gcp_mysql_insert.save_user_pymysql(uid,name,email)
    session['uid']=uid #uid까진 적용이 되었다
    print('saveSQL까지 완료 with'+session['uid'])
    return redirect(url_for('trans'))

#결제관련
@app.route("/paidamount",methods=["GET","POST"]) #결제금액을 충전하기 위한 부분
def save_paidamount():
    paidamount = request.args.get("paidamount")
    uid=session['uid']
    print("결제완료금액입니다"+paidamount)
    print("paidamout에서의 "+session['uid'])
    in_up.save_paidamount(uid,int(paidamount))
    return redirect(url_for('trans'))


if __name__ == '__main__':
    app.run()