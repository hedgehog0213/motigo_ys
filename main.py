from flask import render_template, url_for
from flask import Flask, request
from werkzeug.utils import redirect
import Gtrans
import database
import google_api as gap
import gcp_mysql_insert

app = Flask(__name__)
tgtresult = ""
result = ""
source_len=""

#메인화면
@app.route('/')
def to_pop():
    return render_template('front.html')

@app.route('/popauth')
def main():
    return render_template('popauth.html')

@app.route("/trans")
def trans(tgtresult=tgtresult, result=result, source_len=source_len):
    sourcetxt = request.args.get("sourcetxt")
    if sourcetxt is not None:
        if Gtrans.tr.translate(sourcetxt).src == 'ko':
            targettxt = gap.translate_to_en_text(sourcetxt)
        else:
            targettxt = gap.translate_to_ko_text(sourcetxt)
        whole_result = save_srctgt(sourcetxt, targettxt)
        result = whole_result[1:3]
        tgtresult = whole_result[2]
        source_len=str(len(sourcetxt.replace(' ', '')))
        print("/trans에서의 result : ",tgtresult)
        print(source_len)
    return render_template("translator.html",result=result,source_len=source_len)

#저장
@app.route("/save", methods=["POST"])
def save_srctgt(sourcetxt, targettxt):
    #database.save(sourcetxt, targettxt)
    gcp_mysql_insert.save_pymysql(sourcetxt, targettxt)
    #result = database.load_result()
    result = gcp_mysql_insert.load_result_pymysql()
    print("/save에서의 result : ",result)
    # return redirect(url_for("trans"))
    return result

@app.route('/show')
def show_database():

    return render_template('dataframe.html',)


if __name__ == '__main__':
    app.run()
