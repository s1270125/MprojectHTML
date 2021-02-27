from flask import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('test_reserve.html')


@app.route('/enter')
def enter():
    return render_template('enter.html')


@app.route("/kakunin", methods=["GET", "POST"])
def kakunin():
    number_to_str = {"1": "一人必要です", "2": "二人必要です",
                     "3": "三人必要です", "4": "四人以上の助っ人が必要です"}
    hazard = "DIDNOT CHECKED"
    if request.method == "POST":
        # 何も入力がないとhazardが代入される
        helper = request.form.get("assistant", hazard)
        judge = request.form.get("judge", hazard)
        # 入力がなかったときにメッセージを代入
        if (helper == hazard) or (judge == hazard):
            return render_template("enter.html", warring="選択をしてください")
        # 助っ人が必要な時は「必要」を選択リストで選択された「必要な人数」で上書きしている
        elif helper == "必要":
            helper = number_to_str[request.form.get("number")]
    # 必要ないと思うけど一応
    else:
        return render_template("enter.html", warring="選択をしてください")

    return render_template("kakunin.html", assistant=helper, judge=judge)


@app.route("/kanryou")
def kanryou():
    return render_template("kanryou.html")

# 関数を引数にトップページに返している


@app.route("/redirects")
def redirects():
    return redirect(url_for('index'))


# for imitaton python app.py
if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=4000)
