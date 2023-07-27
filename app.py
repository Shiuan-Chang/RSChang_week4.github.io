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
        if account == "test" and password == "test":
            session["temp"] = True
            return redirect('/member')
        else:
            if account == '' or password == '':
                error_message = '請輸入帳號密碼'
            else:
                error_message = '帳號、或密碼錯誤'
            return redirect(url_for('error', message=error_message))


@app.route("/member")
def member():
    if "temp" in session:
        return render_template('success.html')
    else:
        return redirect("/")


@app.route("/error")
def error():
    error_message = request.args.get("message")
    return render_template('error.html', error_message=error_message)


@app.route("/signout")
def signout():
    session.pop("temp", None)
    return redirect("/")


@app.route("/square/<int:number>")
def square(number):
    # 參數 number 會直接從路徑中提取，不需要從查詢參數中獲取
    squarenumber = number**2
    # 當 Flask 從 Python 程式碼中傳送變數至模板時，在使用 {{ }} 來取用這些變數的值並將它們插入到 HTML 中。
    return render_template("square.html", result=squarenumber)


if __name__ == "__main__":
    app.run(port=3000)
