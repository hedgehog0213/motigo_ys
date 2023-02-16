import pandas as pd
from flask import render_template, url_for,session
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

uid=''

#메인화면


@app.route('/')
def popauth():
    return render_template('popauth.html')

@app.route('/google_demo')
def main():
    return render_template('google_demo.html')


@app.route("/trans")
def trans(tgtresult=tgtresult, result=result, source_len=source_len,uid=uid):
    sourcetxt = request.args.get("sourcetxt")
    if sourcetxt is not None:
        if gap.tr.translate(sourcetxt).src == 'ko':
            targettxt = gap.translate_to_en_text(sourcetxt)
        else:
            targettxt = gap.translate_to_ko_text(sourcetxt)
        whole_result = save_srctgt(sourcetxt, targettxt)
        #uid = session['uid'] #번역 과정에서 이친구가 문제가 생겼다
        result = whole_result[1:3]
        tgtresult = whole_result[2]
        source_len=len(sourcetxt.replace(' ', ''))

        print("/trans까지 완료" + session['uid']) #session['uid']가 존재하는 것 확인
    return render_template("translator.html",result=result,source_len=source_len,uid=uid)

#저장
@app.route("/save", methods=["POST"]) #번역 결과 전과 후 저장 ++여기다가 소비 함수 만든 후 사용하면 될듯
def save_srctgt(sourcetxt, targettxt):
    #database.save(sourcetxt, targettxt)
    #uid=session['uid']
    gcp_mysql_insert.save_pymysql(sourcetxt, targettxt, session['uid']) #session['uid']만 들어가 있어도 세션값이 넘어감
    result = gcp_mysql_insert.load_result_pymysql()
    in_up.consumption(session['uid'], len(sourcetxt.replace(' ','')))
    #print("/save에서의 result : ",result)
    print("/save까지 완료 with" + session['uid'])
    #return redirect(url_for("trans"))
    return result

@app.route("/saveSQL", methods=['POST']) #회원정보 저장
def saveSQL():
    output = request.get_json()
    result = json.loads(output)
    pdinfo = pd.DataFrame(result['info'])
    uid = pdinfo.iloc[0,0]
    name = pdinfo.iloc[1,0]
    email = pdinfo.iloc[2,0]
    gcp_mysql_insert.save_user_pymysql(uid,name,email)
    session['uid']=uid #uid까진 적용이 되었다
    print('saveSQL까지 완료 with'+session['uid'])
    return redirect(url_for('trans'))


@app.route('/kg') # 충전 관련 ++ 여기다가 충전 관련 함수 만든후 사용하면 될듯
def kg_pay():
    save_point = request.args.get('money')
    uid = session['uid']
    #save_point_db(save_point,session['uid'])
    print(save_point)
    print(session['uid'])#로그인하고 넘어오면 나옴, 로그인 안하고 넘어오면 안됨
    print(uid)
    return render_template('kg.html')

@app.route('/kg_save', methods=['POST'])
def save_point_db():
    in_up.save_charge(save_point,uid)
    return redirect(url_for('trans'))





@app.route('/graph_day')
def show_graph_day():
    return render_template('graph.html')

if __name__ == '__main__':
    app.run()
