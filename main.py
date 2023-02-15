import pandas as pd
from flask import render_template, url_for,session
from flask import Flask, request
from werkzeug.utils import redirect
#import Gtrans
#import database
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

uid=''

#메인화면

@app.route('/')
def main():
    return render_template('popauth.html')

@app.route("/trans")
def trans(tgtresult=tgtresult, result=result, source_len=source_len):
    sourcetxt = request.args.get("sourcetxt")
    if sourcetxt is not None:
        if gap.tr.translate(sourcetxt).src == 'ko':
            targettxt = gap.translate_to_en_text(sourcetxt)
        else:
            targettxt = gap.translate_to_ko_text(sourcetxt)
        whole_result = save_srctgt(sourcetxt, targettxt)
        result = whole_result[1:3]
        tgtresult = whole_result[2]
        source_len=len(sourcetxt.replace(' ', ''))

        #print("/trans에서의 result : ",tgtresult)
        #print(source_len)
        #print(session['uid'])
    return render_template("translator.html",result=result,source_len=source_len)

#저장
@app.route("/save", methods=["POST"]) #번역 결과 전과 후 저장 ++여기다가 소비 함수 만든 후 사용하면 될듯
def save_srctgt(sourcetxt, targettxt):
    #database.save(sourcetxt, targettxt)
    uid=session['uid']
    gcp_mysql_insert.save_pymysql(sourcetxt, targettxt,uid)
    result = gcp_mysql_insert.load_result_pymysql()
    in_up.consumption(uid, len(sourcetxt.replace(' ','')))
    #print("/save에서의 result : ",result)
    #print(session['uid'])
    # return redirect(url_for("trans"))
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
    return redirect(url_for('trans'))


@app.route('/kg') # 충전 관련 ++ 여기다가 충전 관련 함수 만든후 사용하면 될듯
def kg_pay():
    print(session['uid'])
    return render_template('kg.html')

@app.route('/graph_day')
def show_graph_day():
    return render_template('graph.html')

if __name__ == '__main__':
    app.run()
