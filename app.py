from flask import *
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

app = Flask(__name__)

# 今日の日付を読み取り
today = date.today()
global selectYear
selectYear = today.year
global selectMonth
selectMonth = today.month

# テスト用


class reserve:
    def __init__(self):
        # 初期化
        self.year = 0
        self.month = 0
        self.day = 0


reserve = reserve()
reserve.year = 2021
reserve.month = 3
reserve.day = 11

# 指定された年と月をもとにカレンダーを作成


def buildCalender(year, month):
    # 月の最初の日を作成
    firstday = date(year, month, 1)
    # 月の末日を作成
    lastday = firstday + relativedelta(months=1) - timedelta(days=1)
    weeks = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sta"]
    dates = []
    # 日曜日から月の最初の日を詮索、違ったら空白を挿入
    for week in weeks:
        if week == firstday.strftime("%a"):
            break
        else:
            dates.append(Markup('<td></td>'))

    # 月の最初の日から末尾まで日にちを代入していく
    for i in range(1, lastday.day+1):
        # 今日の日付と一致したら、特定のhtmlを代入
        # 当日予約を防ぐために条件分岐をtodayの比較から行っている
        if i == today.day and month == today.month and year == today.year:
            dates.append(
                Markup('<td class="parent"><span class="circle">{}</span></td>'.format(str(i))))
        # 予約日があったら、特定のhtmlを代入
        elif i == reserve.day and month == reserve.month and year == reserve.year:
            dates.append(Markup(
                '<td class="possible"><form><input type="button" name="day" value="{}"></form></td>'.format(str(i))))
        else:
            dates.append('<td>{}</td>'.format(str(i)))

    # datesリストが7の倍数になるように空白を代入
    while len(dates) % 7 != 0:
        dates.append(Markup('<td></td>'))

    calender = []
    week = []
    i = 0
    # dates配列を7列の2次元の配列へと変換
    for day in dates:
        week.append(day)
        if (i+1) % 7 == 0:
            calender.append(week)
            week = list()
        i += 1
    return calender


@app.route('/')
def index():
    global selectYear
    global selectMonth
    # 次の月のカレンダーをGETで得たmonthをもとに作成
    if request.args.get("method") == "next":
        month = request.args.get("month")
        if int(month) >= 12:
            selectYear += 1
            selectMonth = 1
        else:
            selectMonth += 1

        return render_template('test_reserve.html', calender=buildCalender(selectYear, selectMonth), selectYear=selectYear, selectMonth=selectMonth)

    # 前の月のカレンダーをGETで得たmonthをもとに作成
    elif request.args.get("method") == "prev":
        month = request.args.get("month")
        if int(month) <= 1:
            selectYear -= 1
            selectMonth = 12
        else:
            selectMonth -= 1

        return render_template('test_reserve.html', calender=buildCalender(selectYear, selectMonth), selectYear=selectYear, selectMonth=selectMonth)

    # 初めてこのページに訪れた場合はrequest.args.get("method")は何もないので今日の年と月をもとにカレンダーを作成する
    else:
        return render_template('test_reserve.html', calender=buildCalender(selectYear, selectMonth), selectYear=selectYear, selectMonth=selectMonth)


@app.route('/enter')
def enter():
    return render_template('enter.html')


@app.route("/kakunin", methods=["GET", "POST"])
def kakunin():
    number_to_str = {"1": "一人必要です", "2": "二人必要です",
                     "3": "三人必要です", "4": "四人以上の助っ人が必要です"}
    if request.method == "POST":
        # 何も入力がないとNoneが代入される
        helper = request.form.get("assistant")
        judge = request.form.get("judge")
        # 入力がなかったときにメッセージを代入
        if (helper is None) or (judge is None):
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


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/check", methods=["POST"])
def check():
    account = {"team": "まほろば改", "password": "9h49huvh"}  # テスト用
    # html、formタグのname属性をもとにvalueをサーバーサイドに取得している
    enter_team = request.form.get("team")
    enter_pass = request.form.get("password")
    # チーム名とそのチームのパスワードが一致していたら、完了画面を表示
    if (enter_team == account["team"]) and (enter_pass == account["password"]):
        return render_template("loginComplete.html")
    # 一致していなかったら、もしくは空入力が送られてきた場合に警告を表示
    else:
        return render_template("login.html", warring="チーム名とパスワードを正しく入力して下さい")


@app.route("/create", methods=["GET", "POST"])
def createAccount():
    # POSTがあった場合に条件を比べる
    if request.method == "POST":
        # html、formタグのname属性をもとにvalueをサーバーサイドに取得している
        team = request.form.get("team")
        leader = request.form.get("leader")
        mail = request.form.get("mail")
        password = request.form.get("password")
        # 4つの項目どれか一つでも空の入力があった場合に警告を表示
        if (team == "") or (leader == "") or (mail == "") or (password == ""):
            return render_template("newInform.html", warring="各項目の入力をお願いします")
        # 全て入力されていたら、完了画面を表示
        else:
            return render_template("newInformComplete.html", team=team)

    # 初めて/createを訪れた場合はPOSTは送られてこないので入力画面を表示
    else:
        return render_template("newInform.html")


# 関数を引数にトップページに返している


@app.route("/redirects")
def redirects():
    return redirect(url_for('index'))


# for imitaton python app.py
if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=4000)
