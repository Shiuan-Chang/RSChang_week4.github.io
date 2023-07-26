from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(
    # 將靜態檔案放到前端
    __name__,
    static_folder="public",  # 靜態檔案如文字檔、圖檔、CSS檔放在public將檔案送到前端
    static_url_path="/public"
)
app.secret_key = "any string but secret"  # 設定session


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/signin", methods=["POST"])  # 沒有用post網址會顯示出帳密
def signin():
    if request.method == 'POST':
        account = request.form['account']  # 用post接收要用form, get則用args.get
        password = request.form['password']
        if account == str('test') and password == str('test'):
            session["temp"] = "member"
            return redirect('/member')
        else:
            if account == '' or password == '':
                session["error_message"] = '請輸入帳號密碼'
            else:
                session["error_message"] = '帳號、或密碼錯誤'
            session["temp"] = "error"
            return redirect(url_for('error', message="自訂的錯誤訊息"))


@app.route("/member")
def member():
    if session.get("temp") == "member":
        return render_template('success.html')
    else:
        return redirect("/")


@app.route("/error")
def error():
    if session.get("temp") == "error":
        # 等於是標記一個狀態，只有在這個狀態符合時，才會渲染以下畫面。如果沒有符合狀態，會導向主要頁面。
        error_message = session.get("error_message")
        session.pop("temp", None)
        # 沒有刪掉temp，預設會被保留，若使用者導向別的頁面後，直接更改網址依舊能夠進入errors
        session.pop("error_message", None)
        return render_template('error.html', error_message=error_message)
    else:
        return redirect("/")


@app.route("/signout")
def signout():
    session.pop("temp", None)
    return redirect("/")


@app.route("/getnumber", methods=["POST"])
def getnumber():
    number = request.form.get("number", type=int)
    # 第一個number是參數，第二個是前面定義參數的值的來源，這邊會顯示下方網址http://127.0.0.1:3000/square?number=<number的值>
    return redirect(url_for('square', number=number))


@app.route("/square/<int:number>")
def square(number):
    # 寫成int(number*number)是不對的，會變成字串做相乘，要轉換成數字做相乘
    squarenumber = number**2
    # 當 Flask 從 Python 程式碼中傳送變數至模板時，在使用 {{ }} 來取用這些變數的值並將它們插入到 HTML 中。
    return render_template("square.html", result=squarenumber)


if __name__ == "__main__":
    app.run(port=3000)
